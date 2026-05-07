from fastapi import APIRouter, Request
from typing import List
from model import JobDescriptionInput, RankedCandidate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from supabase import AsyncClient
from service import recommend_candidates_service

router = APIRouter(prefix="/api/mike")


@router.post("/match", response_model=List[RankedCandidate])
async def recommend_candidates_handler(
    req: Request, input: JobDescriptionInput
) -> List[RankedCandidate]:
    llm: ChatOpenAI = req.app.state.llm_client
    embedding: OpenAIEmbeddings = req.app.state.embedding
    supabase_client: AsyncClient = req.app.state.supabase_client

    response = await recommend_candidates_service(
        llm, embedding, supabase_client, input
    )

    return response
