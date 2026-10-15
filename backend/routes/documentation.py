"""Consent-gated documentation endpoints.

Drafts live only in process memory in this hackathon baseline. They disappear on
restart and are not sent to an EHR. Use a secured persistent store before real use.
"""
from __future__ import annotations
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4
from fastapi import APIRouter, HTTPException

from backend.schemas.clinical_note import (
    ApprovalRequest, ApprovalResponse, DocumentationRequest,
    DocumentationResponse, utc_now,
)
from backend.safety.approval import validate_clinician_approval
from backend.safety.consent import validate_consent
from backend.services.evidence_linker import link_transcript_evidence
from backend.services.note_generator import generate_soap_note
from backend.services.transcription import normalize_transcript

router = APIRouter(prefix="/documentation", tags=["Clinical Documentation"])
_store: dict[str, dict[str, object]] = {}
_store_lock = RLock()


@router.post("/", response_model=DocumentationResponse, summary="Generate a consent-gated SOAP draft")
def create_documentation(request: DocumentationRequest) -> DocumentationResponse:
    consent = validate_consent(request.consent_given)
    if not consent["allowed"]:
        return DocumentationResponse(status="blocked", message=str(consent["message"]))

    try:
        transcript = normalize_transcript(request.transcript)
        generated = generate_soap_note(transcript)
    except (TypeError, ValueError) as exc:
        return DocumentationResponse(status="error", message=str(exc))

    note_id = f"note_{uuid4().hex}"
    created_at = utc_now()
    evidence = link_transcript_evidence(transcript)
    response = DocumentationResponse(
        status="success",
        message=str(generated["message"]),
        note_id=note_id,
        draft_note=generated["draft_note"],
        evidence=evidence,
        clinician_approval_required=True,
        created_at=created_at,
    )
    with _store_lock:
        _store[note_id] = {
            "response": response,
            "state": "draft",
            "encounter_id": request.encounter_id,
            "created_at": created_at,
            "approved_by": None,
            "approved_at": None,
        }
    return response


@router.post("/approve", response_model=ApprovalResponse, summary="Record clinician review decision")
def approve_documentation(request: ApprovalRequest) -> ApprovalResponse:
    decision = validate_clinician_approval(request.approved)
    if not request.approved:
        if request.note_id:
            with _store_lock:
                record = _store.get(request.note_id)
                if record is not None:
                    record["state"] = "rejected"
        return ApprovalResponse(
            status="rejected" if request.note_id else "pending_approval",
            message=str(decision["message"]),
            note_id=request.note_id,
            note_saved=False,
        )

    # An approval without a note ID is kept for backwards compatibility with
    # the original demo endpoint, but it cannot finalize or save any note.
    if not request.note_id:
        return ApprovalResponse(
            status="approved",
            message="Approval signal received, but no note was identified; no note was finalized or saved.",
            note_saved=False,
            approved_by=request.clinician_id,
            approved_at=utc_now(),
        )

    with _store_lock:
        record = _store.get(request.note_id)
        if record is None:
            return ApprovalResponse(
                status="not_found",
                message="Draft note was not found. It may have expired after a server restart.",
                note_id=request.note_id,
                note_saved=False,
            )
        record["state"] = "approved"
        record["approved_by"] = request.clinician_id or "unspecified_clinician"
        record["approved_at"] = utc_now()
        approved_at = record["approved_at"]

    return ApprovalResponse(
        status="approved",
        message="Clinician approval recorded for this in-memory draft. It has not been saved to an EHR.",
        note_id=request.note_id,
        note_saved=False,
        approved_by=str(record["approved_by"]),
        approved_at=approved_at if isinstance(approved_at, datetime) else None,
    )


@router.get("/{note_id}", summary="Retrieve a draft from the current server process")
def get_documentation(note_id: str) -> dict[str, object]:
    with _store_lock:
        record = _store.get(note_id)
        if record is None:
            raise HTTPException(status_code=404, detail="Draft note not found or server restarted.")
        response = record["response"]
        return {
            "note": response,
            "state": record["state"],
            "approved_by": record["approved_by"],
            "approved_at": record["approved_at"],
            "persistence": "in_memory_only",
        }
