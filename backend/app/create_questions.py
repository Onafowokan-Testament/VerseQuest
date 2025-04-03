import os
from typing import List

from dotenv import load_dotenv
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from pydantic import BaseModel, Field

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


class Question(BaseModel):
    chapter: str = Field(..., description="")
    question_text: List[str] = Field(
        ...,
        description="give me 20 multi choice questions on the bible chapter user will provide",
    )
    options: List[List[str]] = Field(
        ..., description="provide the 4 options each for each question"
    )
    correct_answer: List[str] = Field(
        ..., description="Corrct answers to the question given"
    )


json_agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile", frequency_penalty=2, presence_penalty=2),
    response_model=Question,
    description=" Generate multiple-choice questions for a learning platform based on a given chapter ",
    instructions=[
        "The questions should be engaging, relevant, and structured for effective learning. Ensure diversity in difficulty level and avoid ambiguity",
        " Ensure a mix of question types, including Direct recall (e.g., ‘Which verse says…?’) Interpretation (e.g., ‘What does this verse mean?’), Fill in the blanks (e.g., ‘Complete this verse: …’), Context-based (e.g., ‘In what situation was this verse spoken?’)",
        "Ensure questions are randomly arranged so that no particular pattern emerges.",
        "Maintain diversity in difficulty levels and avoid ambiguity.",
        " Be intelligent in your question",
    ],
   
)


def generate_question(chapter):
    """function to generate questions"""
    response: RunResponse = json_agent.run(chapter)
    return response


generate_question("romans 5")
