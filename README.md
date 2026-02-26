# Resume Parser

AI-powered resume parsing application using FastAPI, Streamlit, and LLMs (OpenAI GPT-4 / GPT-5.2).

## Features

- **PDF and DOCX Support**: Upload resumes in PDF or DOCX format
- **LLM-Powered Extraction**: Uses OpenAI GPT-4 / GPT-5.2 for intelligent parsing
- **Comprehensive Data Extraction**:
  - Contact Information (name, email, phone, location, LinkedIn, GitHub)
  - Professional Summary
  - Work Experience (company, role, duration, responsibilities)
  - Projects (name, skills, description)
  - Education (degree, institution, year, location)
  - Skills (technical and soft skills)
  - Certifications
- **RESTful API**: FastAPI backend with auto-generated docs
- **Interactive UI**: Streamlit frontend for easy resume upload and viewing
- **Structured Logging**: Daily log rotation with detailed error tracking

## Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **LLM**: LangChain + OpenAI (GPT-4 / GPT-5.2)
- **Document Processing**: PyMuPDF (PDF), python-docx (DOCX)
- **Data Validation**: Pydantic
- **Logging**: Loguru

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd resume-parser
```

### 2. Create Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_CHAT_MODEL=gpt-4o
OPENAI_EMBED_MODEL=text-embedding-3-small
```

### 5. Run the Application

#### Start FastAPI Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Start Streamlit UI (in a new terminal)

```bash
streamlit run ui/streamlit_app.py
```

UI will be available at: http://localhost:8501

## API Endpoints

### POST /api/upload

Upload and parse a resume file.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF or DOCX)

**Response:**
```json
{
  "document_id": "uuid",
  "file_name": "resume.pdf",
  "extracted_at": "2024-01-01T12:00:00",
  "data": {
    "contact_information": {...},
    "professional_summary": "...",
    "work_experience": [...],
    "education": [...],
    "skills": {...},
    "certifications": [...]
  }
}
```

### GET /api/resume/{document_id}

Retrieve previously parsed resume data.

**Response:**
- 200: Resume data (same as POST response)
- 404: Resume not found

## Project Structure

```
resume-parser/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── models.py              # Pydantic models
│   ├── storage.py             # In-memory storage
│   ├── services/
│   │   ├── parser.py          # Resume parsing logic
│   │   ├── llm_service.py     # LLM configuration
│   │   └── document_extractor.py  # PDF/DOCX extraction
│   └── utils/
│       ├── logger.py          # Logging configuration
│       └── custom_exception.py # Custom exceptions
├── ui/
│   └── streamlit_app.py       # Streamlit UI
├── data/
│   └── uploads/               # Uploaded files
├── logs/                       # Application logs
├── requirements.txt
├── .env.example
└── README.md
```

## Usage

1. **Start both servers** (FastAPI and Streamlit)
2. **Open Streamlit UI** at http://localhost:8501
3. **Upload a resume** (PDF or DOCX)
4. **Click "Parse Resume"** and wait for processing
5. **View extracted data** in organized sections
6. **Download JSON** if needed

## Notes

- Resumes are stored in-memory (data lost on restart)
- OpenAI API key required (costs apply)
- Processing time depends on resume size and API response

## Further improvements

- Use Vector DB / DB to store the parsed data for persistence
- Enable users to chat with the parsed data
- React based UI


## License

MIT License
