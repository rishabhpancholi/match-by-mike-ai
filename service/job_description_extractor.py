from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from model import ExtractedJobRequirements
from typing import Tuple


async def extract_job_description(
    llm: ChatOpenAI, job_description_input: str
) -> Tuple[str, ExtractedJobRequirements]:
    prompt = PromptTemplate(
        template="""
        You are an experienced job description extractor.
        Your task is to extract the job requirements from the job description.
        You are expected to extract the following job requirements from the job description:
        - The role a candidate has to perform in the job.
        - The list of skills required for the job.
        - The minimum years of experience needed for the job.
        - The maximum amount of salary offered for the job in rupees per annum.
        - The location of the job(if applicable).

        Here is the job description: {job_description}
        """,
        input_variables=["job_description"],
    )

    llm_with_tool = llm.with_structured_output(ExtractedJobRequirements)

    chain = prompt | llm_with_tool

    requirements: ExtractedJobRequirements = await chain.ainvoke(
        {"job_description": job_description_input}
    )

    jd_str = f"""
    Role: {requirements.role}
    Skills: {", ".join(requirements.skills)}
    """

    jd_str = jd_str.strip()

    return (jd_str, requirements)
