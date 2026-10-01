import csv
import io
import re

from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.models import Lead
from app.schemas import LeadCreate, LeadUpdate


LEAD_FIELDS = {
    "name",
    "company",
    "role",
    "email",
    "website",
    "industry",
    "company_size",
    "source",
    "notes",
}
MAX_CSV_BYTES = 5 * 1024 * 1024
MAX_CSV_ROWS = 5000


class CSVImportError(ValueError):
    pass


def parse_leads_csv(content: bytes) -> list[LeadCreate]:
    if len(content) > MAX_CSV_BYTES:
        raise CSVImportError("CSV file exceeds the 5 MB limit")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise CSVImportError("CSV file must use UTF-8 encoding") from error

    try:
        reader = csv.DictReader(io.StringIO(text), strict=True)
        headers = reader.fieldnames
        if not headers:
            raise CSVImportError("CSV file must include a header row")

        normalized_headers = [
            re.sub(r"[\s-]+", "_", header.strip().lower()) for header in headers
        ]
        if len(normalized_headers) != len(set(normalized_headers)):
            raise CSVImportError("CSV file contains duplicate columns")
        unknown_headers = set(normalized_headers) - LEAD_FIELDS
        if unknown_headers:
            raise CSVImportError(
                f"Unsupported CSV columns: {', '.join(sorted(unknown_headers))}"
            )
        if "name" not in normalized_headers:
            raise CSVImportError("CSV file must include a name column")

        leads: list[LeadCreate] = []
        for row_number, row in enumerate(reader, start=2):
            if row_number > MAX_CSV_ROWS + 1:
                raise CSVImportError(f"CSV file exceeds the {MAX_CSV_ROWS} row limit")
            if None in row:
                raise CSVImportError(f"CSV row {row_number} has extra values")
            values = {
                normalized_headers[index]: value
                for index, value in enumerate(row.values())
            }
            try:
                leads.append(LeadCreate.model_validate(values))
            except ValidationError as error:
                raise CSVImportError(
                    f"CSV row {row_number} contains invalid lead data"
                ) from error
    except csv.Error as error:
        raise CSVImportError("CSV file is malformed") from error

    return leads


def create_lead(session: Session, values: LeadCreate) -> Lead:
    lead = Lead(**values.model_dump())
    session.add(lead)
    session.commit()

    session.refresh(lead)
    return lead


def import_leads(session: Session, leads: list[LeadCreate]) -> list[Lead]:
    records = [Lead(**lead.model_dump()) for lead in leads]
    session.add_all(records)
    session.commit()
    for record in records:
        session.refresh(record)
    return records


def list_leads(
    session: Session,
    *,
    query: str | None,
    company: str | None,
    industry: str | None,
    sort_by: str,
    sort_order: str,
    limit: int,
    offset: int,
) -> list[Lead]:
    statement = select(Lead)
    if query:
        pattern = f"%{query.strip()}%"
        statement = statement.where(
            or_(
                Lead.name.ilike(pattern),
                Lead.company.ilike(pattern),
                Lead.role.ilike(pattern),
                Lead.email.ilike(pattern),
            )
        )
    if company:
        statement = statement.where(Lead.company.ilike(f"%{company.strip()}%"))
    if industry:
        statement = statement.where(Lead.industry.ilike(f"%{industry.strip()}%"))

    sort_column = getattr(Lead, sort_by)
    statement = statement.order_by(
        sort_column.asc() if sort_order == "asc" else sort_column.desc(), Lead.id
    )
    statement = statement.offset(offset).limit(limit)
    return list(session.scalars(statement).all())


def get_lead(session: Session, lead_id: int) -> Lead | None:
    return session.get(Lead, lead_id)


def update_lead(session: Session, lead: Lead, values: LeadUpdate) -> Lead:
    for field, value in values.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    session.commit()
    session.refresh(lead)
    return lead


def delete_lead(session: Session, lead: Lead) -> None:
    session.delete(lead)
    session.commit()
