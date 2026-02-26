from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ContactInformation(BaseModel):
    """Contact information extracted from resume."""

    name: Optional[str] = Field(None, description="Full name of the candidate")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Location/Address")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    portfolio: Optional[str] = Field(
        None, description="Portfolio or personal website URL"
    )


class WorkExperience(BaseModel):
    """Work experience entry."""

    company: str = Field(..., description="Company name")
    role: str = Field(..., description="Job title/role")
    duration: str = Field(..., description="Duration of employment")
    location: Optional[str] = Field(None, description="Job location")
    responsibilities: Optional[List[str]] = Field(
        None, description="List of responsibilities and achievements"
    )


class Project(BaseModel):
    """Project details."""

    name: Optional[str] = Field(None, description="Project name")
    skills_used: Optional[List[str]] = Field(
        None, description="Technologies and skills used"
    )
    aim: Optional[str] = Field(None, description="Project objective or aim")
    description: Optional[str] = Field(None, description="Project description")


class Education(BaseModel):
    """Education details."""

    degree: Optional[str] = Field(None, description="Degree or qualification")
    institution: Optional[str] = Field(None, description="Institution name")
    year: Optional[str] = Field(None, description="Year of completion or duration")
    location: Optional[str] = Field(None, description="Institution location")


class Skills(BaseModel):
    """Skills categorized by type."""

    technical: Optional[List[str]] = Field(
        default_factory=list,
        description="Technical skills (programming languages, frameworks, tools)",
    )
    soft: Optional[List[str]] = Field(
        default_factory=list,
        description="Soft skills (leadership, communication, etc.)",
    )


class Certification(BaseModel):
    """Certification details."""

    name: str = Field(..., description="Certification name")
    issuer: Optional[str] = Field(None, description="Issuing organization")
    date: Optional[str] = Field(None, description="Date obtained")


class ResumeData(BaseModel):
    """Complete structured resume data."""

    contact_information: Optional[ContactInformation] = Field(
        None, description="Contact information"
    )
    professional_summary: Optional[str] = Field(
        None, description="Professional summary or objective statement"
    )
    work_experience: Optional[List[WorkExperience]] = Field(
        default_factory=list, description="Work experience history"
    )
    projects: Optional[List[Project]] = Field(
        default_factory=list, description="Projects worked on"
    )
    education: Optional[List[Education]] = Field(
        default_factory=list, description="Educational background"
    )
    skills: Optional[Skills] = Field(None, description="Skills and competencies")
    certifications: Optional[List[Certification]] = Field(
        default_factory=list, description="Professional certifications"
    )


class ResumeResponse(BaseModel):
    """API response for parsed resume."""

    document_id: str = Field(..., description="Unique document identifier")
    data: ResumeData = Field(..., description="Extracted resume data")
    extracted_at: datetime = Field(
        default_factory=datetime.now, description="Timestamp of extraction"
    )
    file_name: str = Field(..., description="Original filename")


class ErrorResponse(BaseModel):
    """API error response."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
