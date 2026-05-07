from pydantic import BaseModel, Field
from typing import List, Optional


class JobDescriptionInput(BaseModel):
    job_description: str


class ExtractedJobRequirements(BaseModel):
    role: str = Field(description="The role a candidate has to perform in the job.")
    skills: List[str] = Field(description="The list of skills required for the job.")
    min_experience_years: int = Field(
        description="Minimum years of experience needed for the job. If not mentioned then consider it a fresher joba and keep the value as 0.",
        default=0,
    )
    max_salary_offered: Optional[int] = Field(
        description="Maximum amount of salary offered for the job in rupees per"
    )
    location: Optional[str] = Field(description="The location of the job.")


class RankedCandidate(BaseModel):
    candidate_name: str = Field(description="The name of the candidate.")
    rationale: str = Field(description="The rationale behind the ranking.")


class RankedCandidatesResponse(BaseModel):
    ranked_candidates: list[RankedCandidate]
