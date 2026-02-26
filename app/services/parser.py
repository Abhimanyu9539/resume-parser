"""
Resume parsing service using LLM for structured extraction.
"""

import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.models import ResumeData
from app.services.llm_service import get_llm
from app.services.document_extractor import DocumentExtractor
from app.utils.custom_exception import CustomException
from app.utils.logger import logger


def parse_resume_text(resume_text: str) -> ResumeData:
    """
    Parse resume text using LLM.

    Args:
        resume_text: Extracted text from resume

    Returns:
        ResumeData object
    """
    try:
        logger.info("Parsing resume with LLM")

        # Setup LLM and parser
        llm = get_llm()
        parser = PydanticOutputParser(pydantic_object=ResumeData)

        # Create prompt
        prompt = ChatPromptTemplate.from_template(
            """You are an expert resume parser. Extract all information from the resume text.

            Extract: Name, Email, Phone, Location, LinkedIn, GitHub, Portfolio, professional summary, work experience, projects, education, skills, and certifications.

            {format_instructions}

            Resume Text:
            {resume_text}

            Output:"""
        )

        # Create chain and invoke
        chain = prompt | llm | parser
        result = chain.invoke(
            {
                "resume_text": resume_text,
                "format_instructions": parser.get_format_instructions(),
            }
        )

        logger.info("Resume parsed successfully")
        return result

    except Exception as e:
        logger.error(f"Parsing failed: {str(e)}")
        raise CustomException(e, sys)


def parse_resume(file_path: str, file_extension: str) -> ResumeData:
    """
    Parse resume file.

    Args:
        file_path: Path to resume file
        file_extension: File extension (.pdf or .docx)

    Returns:
        ResumeData object
    """
    try:
        logger.info(f"Parsing resume: {file_path}")

        # Extract text
        text = DocumentExtractor.extract_text(file_path, file_extension)

        # Parse with LLM
        resume_data = parse_resume_text(text)

        return resume_data

    except Exception as e:
        logger.error(f"Resume parsing failed: {str(e)}")
        raise CustomException(e, sys)
