from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
# Ensure .env is loaded early for the running process
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from core.config import Settings
from services.pdf_service import extract_text_from_pdf
from services.llm_service import extract_structured_info
from services.tavily_service import search_news
from utils.logger import setup_logging
from schemas.cv import CVSummaryResponse
from schemas.news import NewsResponse

setup_logging()
app = FastAPI(title="CV Summarizer + Tavily News API")
settings = Settings()


@app.post("/cv/summarize", response_model=CVSummaryResponse)
async def summarize_cv(file: UploadFile = File(...)):
    if not file.content_type or "pdf" not in file.content_type.lower():
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid file type. Please upload a PDF.")

    try:
        content = await file.read()
        text = extract_text_from_pdf(content)
        if not text.strip():
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Could not extract text from PDF.")
        if not settings.OPENROUTER_API_KEY:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="OPENROUTER_API_KEY is not configured")

        try:
            llm_result = extract_structured_info(
                text,
                api_key=settings.OPENROUTER_API_KEY,
                model=settings.OPENROUTER_MODEL,
                url=settings.OPENROUTER_URL,
            )
        except ValueError as ve:
            # client/config error
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
        except RuntimeError as re:
            # upstream API error
            raise HTTPException(status_code=502, detail=str(re))

        response = {
            "name": llm_result.get("name"),
            "location": llm_result.get("location"),
            "work_experience_summary": llm_result.get("work_experience_summary"),
            "raw_text_excerpt": text[:2000]
        }
        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal error: {str(e)}")


@app.get("/news", response_model=NewsResponse)
def news_search(query: str = Query(..., min_length=1, max_length=256)):
    try:
        if not settings.TAVILY_API_KEY:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="TAVILY_API_KEY is not configured")

        try:
            articles = search_news(query, api_key=settings.TAVILY_API_KEY, base_url=settings.TAVILY_API_URL)
        except ValueError as ve:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
        except RuntimeError as re:
            raise HTTPException(status_code=502, detail=str(re))

        return {"query": query, "results": articles}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"News service error: {str(e)}")
