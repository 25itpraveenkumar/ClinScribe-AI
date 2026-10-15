"""Clinician approval guard. Drafts must never silently become final notes."""


def validate_clinician_approval(approved: bool) -> dict[str, object]:
    if approved is not True:
        return {"approved": False, "message": "Clinician review and approval are required before finalization."}
    return {"approved": True, "message": "Clinician approval received."}
