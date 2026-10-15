
import pytest

from backend.safety.consent import ConsentRecord, validate_consent
from backend.safety.approval import ClinicalDraft, approve_note


def test_consent_is_required():
    assert validate_consent(ConsentRecord(consent_given=True)) is True
    assert validate_consent(ConsentRecord(consent_given=False)) is False


def test_wrong_consent_purpose_is_rejected():
    consent = ConsentRecord(
        consent_given=True,
        purpose="marketing",
    )
    assert validate_consent(consent) is False


def test_draft_is_unapproved_by_default():
    draft = ClinicalDraft(content="Fictional consultation note")
    assert draft.approved is False


def test_clinician_can_approve_nonempty_draft():
    draft = ClinicalDraft(content="Fictional consultation note")
    result = approve_note(draft, "clinician-demo-01")

    assert result.approved is True
    assert result.approved_by == "clinician-demo-01"


def test_blank_clinician_cannot_approve():
    draft = ClinicalDraft(content="Fictional consultation note")

    with pytest.raises(ValueError):
        approve_note(draft, " ")


def test_empty_note_cannot_be_approved():
    draft = ClinicalDraft(content="")

    with pytest.raises(ValueError):
        approve_note(draft, "clinician-demo-01")
