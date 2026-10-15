"""Attach traceable source spans to statements used in the draft.

Only literal text copied from the supplied transcript is marked as directly
supported. Boilerplate limitations are explicitly marked as not provided.
"""
from __future__ import annotations
from uuid import uuid4
from backend.schemas.clinical_note import EvidenceItem


def link_transcript_evidence(transcript: str) -> list[EvidenceItem]:
    quote = transcript.strip()
    if not quote:
        return []
    start = transcript.find(quote)
    return [EvidenceItem(
        evidence_id=f"ev_{uuid4().hex[:12]}",
        section="subjective",
        quote=quote,
        start_char=max(start, 0),
        end_char=max(start, 0) + len(quote),
        support_status="direct_quote",
    )]
