from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    CSVImportSummary,
    LeadCreate,
    LeadRead,
    LeadScoreRead,
    LeadScoreInput,
    LeadScoreResponse,
    LeadUpdate,
)
from app.services import leads as lead_service
from app.services.scoring import save_score, score_tier


router = APIRouter(prefix="/api/leads", tags=["leads"])
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("/import", response_model=CSVImportSummary, status_code=201)
async def import_leads(file: Annotated[UploadFile, File()], session: DatabaseSession):
    content = await file.read(lead_service.MAX_CSV_BYTES + 1)
    try:
        parsed_leads = lead_service.parse_leads_csv(content)
    except lead_service.CSVImportError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    imported = lead_service.import_leads(session, parsed_leads)
    return CSVImportSummary(
        imported_count=len(imported), lead_ids=[lead.id for lead in imported]
    )



@router.get("", response_model=list[LeadRead])
def get_leads(
    session: DatabaseSession,
    q: Annotated[str | None, Query(max_length=200)] = None,
    company: Annotated[str | None, Query(max_length=200)] = None,
    industry: Annotated[str | None, Query(max_length=200)] = None,
    sort_by: Literal["name", "company", "created_at"] = "created_at",
    sort_order: Literal["asc", "desc"] = "desc",
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return lead_service.list_leads(
        session,
        query=q,
        company=company,
        industry=industry,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=LeadRead, status_code=201)
def create_lead(values: LeadCreate, session: DatabaseSession):
    return lead_service.create_lead(session, values)


@router.get("/{lead_id}", response_model=LeadRead)
def get_lead(lead_id: int, session: DatabaseSession):
    lead = lead_service.get_lead(session, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.patch("/{lead_id}", response_model=LeadRead)
def update_lead(lead_id: int, values: LeadUpdate, session: DatabaseSession):
    lead = lead_service.get_lead(session, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead_service.update_lead(session, lead, values)


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(lead_id: int, session: DatabaseSession) -> None:
    lead = lead_service.get_lead(session, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    lead_service.delete_lead(session, lead)


@router.post("/{lead_id}/score", response_model=LeadScoreResponse)
def score_lead(lead_id: int, values: LeadScoreInput, session: DatabaseSession):
    lead = lead_service.get_lead(session, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    score = save_score(session, lead, values)
    response = LeadScoreRead.model_validate(score).model_dump()
    return LeadScoreResponse(
        **response, tier=score_tier(score.overall_score)
    )
