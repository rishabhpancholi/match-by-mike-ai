from model import RankedCandidate, RankedCandidatesResponse
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from typing import List


async def rerank_candidates(
    llm: ChatOpenAI, all_candidate_str: str, job_description: str
) -> List[RankedCandidate]:
    prompt = PromptTemplate(
        template="""
        You are an expert technical recruiter.
        Your task is to rank the eligible candidates for the following job description.

        Here is the job description:
        {jd_str}

        Candidates:
        {all_candidates_str}

        Instructions:
        - Rank candidates from best to worst fit
        - Consider skills, experience, and relevance
        - Give a concise 1 line rationale for each candidate
        - Return structured list of ranked candidates.
        """,
        input_variables=["jd_str", "all_candidates_str"],
    )

    ranker_llm = llm.with_structured_output(RankedCandidatesResponse)

    chain = prompt | ranker_llm

    response: RankedCandidatesResponse = await chain.ainvoke(
        {"jd_str": job_description, "all_candidates_str": all_candidate_str}
    )

    return response.ranked_candidates
