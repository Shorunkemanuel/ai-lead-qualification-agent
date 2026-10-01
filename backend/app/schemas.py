import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class LeadFields(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: str | None = Field(default=None, max_length=200)
    role: str | None = Field(default=None, max_length=200)
    email: str | None = Field(default=None, max_length=320)
    website: str | None = Field(default=None, max_length=500)
    industry: str | None = Field(default=None, max_length=200)
    company_size: str | None = Field(default=None, max_length=100)
    source: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=10000)

    @field_validator("company", "role", "email", "website", "industry", "company_size", "source", "notes", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        if isinstance(value, str):
            normalized = value.strip()
            return normalized or None
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s.]+(?:\.[^@\s.]+)+", normalized):
            raise ValueError("must be a valid email address")
        return normalized


class LeadCreate(LeadFields):
    name: str = Field(min_length=1, max_length=200)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value


class LeadUpdate(LeadFields):
    name: str | None = Field(default=None, min_length=1, max_length=200)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @model_validator(mode="after")
    def require_nonempty_name_when_present(self) -> "LeadUpdate":
        if "name" in self.model_fields_set and not self.name:
            raise ValueError("name cannot be empty or null")
        return self


class LeadScoreInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    icp_fit: int = Field(ge=0, le=100)
    company_potential: int = Field(ge=0, le=100)
    role_relevance: int = Field(ge=0, le=100)
    buying_signal: int = Field(ge=0, le=100)
    data_quality: int = Field(ge=0, le=100)
    rationale: str = Field(default="", max_length=10000)


class LeadScoreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    icp_fit: int
    company_potential: int
    role_relevance: int
    buying_signal: int
    data_quality: int
    overall_score: int
    rationale: str
    created_at: datetime


class LeadScoreResponse(LeadScoreRead):
    tier: Literal["HIGH", "MEDIUM", "LOW", "NOT QUALIFIED"]


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    company: str | None
    role: str | None
    email: str | None
    website: str | None
    industry: str | None
    company_size: str | None
    source: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    scores: list[LeadScoreRead] = Field(default_factory=list)


class CSVImportSummary(BaseModel):
    imported_count: int
    lead_ids: list[int]
