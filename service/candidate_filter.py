from langchain_openai import OpenAIEmbeddings
from model import ExtractedJobRequirements
from supabase import AsyncClient


async def filter_candidates(
    embedding: OpenAIEmbeddings,
    supabase: AsyncClient,
    job_description: str,
    requirements: ExtractedJobRequirements,
) -> str:
    jd_embeddings = await embedding.aembed_query(job_description)

    similar_candidates = await supabase.rpc(
        "match_candidates",
        {
            "query_embedding": jd_embeddings,
            "required_skills": requirements.skills,
            "min_experience_years": requirements.min_experience_years,
        },
    ).execute()

    candidate_strings = []

    for candidate in similar_candidates.data:
        candidate_str = f"""
        Name: {candidate["name"]}
        Skills: {", ".join(candidate["skills"])}
        Experience: {candidate["years_experience"]} years
        Last CTC: {candidate["last_ctc_inr"]} rupees per annum
        Location: {candidate["current_location"]}
        """

        candidate_strings.append(candidate_str)

    all_candidate_str = "\n".join(candidate_strings)

    job_description += (
        f"\nMinimum experience years: {requirements.min_experience_years} years"
    )

    if requirements.max_salary_offered:
        job_description += f"\nMaximum salary offered: {requirements.max_salary_offered} rupees per annum"

    if requirements.location:
        job_description += f"\nLocation: {requirements.location}"

    return all_candidate_str
