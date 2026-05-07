from supabase import AsyncClient
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from model import RankedCandidate
from typing import List
from .job_description_extractor import extract_job_description
from .candidate_filter import filter_candidates
from .candidate_reranker import rerank_candidates


async def recommend_candidates_service(
    llm: ChatOpenAI, embedding: OpenAIEmbeddings, supabase: AsyncClient, input: str
) -> List[RankedCandidate]:
    job_description, requirements = await extract_job_description(llm, input)

    all_candidate_str = await filter_candidates(
        embedding, supabase, job_description, requirements
    )

    ranked_candidates = await rerank_candidates(llm, all_candidate_str, job_description)

    return ranked_candidates
