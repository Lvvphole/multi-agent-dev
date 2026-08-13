from agents import Agent

from contracts.development import DevelopmentProposal


developer_agent = Agent(
    name="Developer",
    instructions=(
        "You are a software development agent. "
        "Analyze the requested engineering task and produce a development proposal. "
        "Do not claim that work has been accepted, verified, approved, or completed. "
        "Identify uncertainty explicitly."
    ),
    model="gpt-5.6",
    output_type=DevelopmentProposal,
)