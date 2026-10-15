"""Clinician approval guard. Drafts must never silently become final notes."""


def validate_clinician_approval(approved: bool) -> dict[str, object]:
    if approved is not True:
        return {"approved": False, "message": "Clinician review and approval are required before finalization."}
    return {"approved": True, "message": "Clinician approval received."}

from dataclasses import dataclass


@dataclass
class ClinicalDraft:
    content: str
    approved: bool = False
    approved_by: str | None = None


def approve_note(draft: ClinicalDraft, clinician_id: str) -> ClinicalDraft:
    """Approve a non-empty draft after clinician review."""
    if not clinician_id or not clinician_id.strip():
        raise ValueError("A clinician identifier is required.")

    if not draft.content or not draft.content.strip():
        raise ValueError("Cannot approve an empty clinical note.")

    draft.approved = True
    draft.approved_by = clinician_id.strip()
    return draft


def finalize_note(draft: ClinicalDraft) -> str:
    """Return a note only after approval."""
    if not draft.approved:
        raise PermissionError(
            "Clinical note cannot be finalized before clinician approval."
        )

    return draft.content
