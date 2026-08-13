from pydantic import BaseModel, Field


class DevelopmentProposal(BaseModel):
    summary: str = Field(
        description="Concise description of the proposed work."
    )
    artifacts: list[str] = Field(
        description="Files or artifacts the work would create or modify."
    )
    risks: list[str] = Field(
        description="Known risks, assumptions, or uncertainties."
    )
    needs_human_input: bool = Field(
        description="Whether execution requires unresolved human input."
    )