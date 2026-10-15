
from dataclasses import dataclass


@dataclass
class ClinicalDraft:
    content: str
    approved: bool = False
    approved_by: str | None = None


def approve_note(draft: ClinicalDraft, clinician_id: str) -> ClinicalDraft:
    """Approve a draft only after an identified clinician explicitly reviews it."""
    if not clinician_id or not clinician_id.strip():
        raise ValueError("A clinician identifier is required.")

    if not draft.content.strip():
        raise ValueError("Cannot approve an empty clinical note.")

    draft.approved = True
    draft.approved_by = clinician_id.strip()
    return draft
