"""
Simple in-memory storage for parsed resumes.
"""

from typing import Dict, Optional
from app.models import ResumeResponse
from app.utils.logger import logger


class ResumeStorage:
    """In-memory storage for resume data."""

    def __init__(self):
        self._storage: Dict[str, ResumeResponse] = {}

    def save(self, document_id: str, resume_response: ResumeResponse) -> None:
        """
        Save resume data.

        Args:
            document_id: Unique document identifier
            resume_response: Resume response object
        """
        self._storage[document_id] = resume_response
        logger.info(f"Saved resume with ID: {document_id}")

    def get(self, document_id: str) -> Optional[ResumeResponse]:
        """
        Retrieve resume data by ID.

        Args:
            document_id: Unique document identifier

        Returns:
            ResumeResponse if found, None otherwise
        """
        return self._storage.get(document_id)

    def exists(self, document_id: str) -> bool:
        """
        Check if document exists.

        Args:
            document_id: Unique document identifier

        Returns:
            True if exists, False otherwise
        """
        return document_id in self._storage


# Global storage instance
resume_storage = ResumeStorage()
