import os
import uuid
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from app.models import ResumeResponse
from app.services.parser import parse_resume
from app.storage import resume_storage
from app.utils.logger import logger

app = FastAPI(
    title="Resume Parser API",
    description="AI-powered resume parsing using LLMs",
    version="1.0.0",
)

UPLOAD_DIR = "data/uploads"
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Resume Parser API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "POST /api/upload",
            "retrieve": "GET /api/resume/{document_id}",
        },
    }


@app.post(
    "/api/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED
)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse a resume file.

    Args:
        file: Resume file (PDF or DOCX)

    Returns:
        Parsed resume data with document ID
    """
    try:
        logger.info(f"Received file upload: {file.filename}")

        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            logger.error(f"Invalid file type: {file_ext}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}",
            )

        # Generate unique document ID
        document_id = str(uuid.uuid4())

        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{document_id}{file_ext}")
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        logger.info(f"File saved: {file_path}")

        # Parse resume
        resume_data = parse_resume(file_path, file_ext)

        # Create response
        resume_response = ResumeResponse(
            document_id=document_id,
            data=resume_data,
            extracted_at=datetime.now(),
            file_name=file.filename,
        )

        # Store in memory
        resume_storage.save(document_id, resume_response)

        logger.info(f"Resume processed successfully: {document_id}")
        return resume_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload processing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume: {str(e)}",
        )


@app.get("/api/resume/{document_id}", response_model=ResumeResponse)
def get_resume(document_id: str):
    """
    Retrieve parsed resume data by document ID.

    Args:
        document_id: Unique document identifier

    Returns:
        Parsed resume data
    """
    try:
        logger.info(f"Retrieving resume: {document_id}")

        # Retrieve from storage
        resume_response = resume_storage.get(document_id)

        if resume_response is None:
            logger.warning(f"Resume not found: {document_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Resume with ID '{document_id}' not found",
            )

        logger.info(f"Resume retrieved successfully: {document_id}")
        return resume_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve resume: {str(e)}",
        )
