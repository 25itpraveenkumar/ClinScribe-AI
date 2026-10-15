"""Transcript normalization utilities.

This module does not pretend to perform speech recognition. Integrate a vetted,
consent-aware speech-to-text provider here if audio transcription is added later.
"""
from __future__ import annotations


def normalize_transcript(transcript: str) -> str:
    """Normalize line endings and surrounding whitespace without rewriting meaning."""
    if not isinstance(transcript, str):
        raise TypeError("transcript must be a string")
    normalized = transcript.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        raise ValueError("Transcript cannot be empty.")
    return normalized
