"""Validated API schemas for consent-first clinical documentation.

The API deliberately models a draft, not a final clinical record. It does not
claim to diagnose, prescribe, or save records to an EHR.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DocumentationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    transcript: str = Field(min_length=1, max_length=50_000, description="Text transcript supplied by an authorized user")
    consent_given: bool = Field(default=False, description="Explicit confirmation that required patient consent was obtained")
    encounter_id: str | None = Field(default=None, max_length=128, description="Optional local encounter reference; do not send direct identifiers unnecessarily")

    @field_validator("transcript")
    @classmethod
    def transcript_must_contain_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Transcript cannot be empty or whitespace only.")
        return value.strip()


class EvidenceItem(BaseModel):
    evidence_id: str
    section: Literal["subjective", "objective", "assessment", "plan"]
    quote: str
    start_char: int
    end_char: int
    support_status: Literal["direct_quote", "not_provided"]


class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str
    limitations: list[str] = Field(default_factory=list)


class DocumentationResponse(BaseModel):
    status: Literal["success", "blocked", "error"]
    message: str
    note_id: str | None = None
    draft_note: SOAPNote | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list)
    clinician_approval_required: bool = True
    created_at: datetime | None = None


class ApprovalRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    approved: bool = False
    note_id: str | None = Field(default=None, max_length=128)
    clinician_id: str | None = Field(default=None, max_length=128)
    comments: str | None = Field(default=None, max_length=2_000)


class ApprovalResponse(BaseModel):
    status: Literal["approved", "pending_approval", "rejected", "not_found"]
    message: str
    note_id: str | None = None
    note_saved: bool = False
    approved_by: str | None = None
    approved_at: datetime | None = None


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)
