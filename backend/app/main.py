from typing import List
from database import SessionLocal
from fastapi import Depends, FastAPI, HTTPException
from models import Question
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils import add_question, add_user_result, get_questions_by_chapter

app = FastAPI()


@app.get("/")
def home():
    return {"message": "hello world"}


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


class QuestionCreate(BaseModel):
    chapter: str
    question_text: List[str]
    options: List[List[str]]
    correct_answer: List[str]


@app.post("/add-questions/")
async def create_questions(
    question_data: QuestionCreate, db: Session = Depends(get_db)
):
    return add_question(
        db,
        question_data.chapter,
        question_data.question_text,
        question_data.options,
        question_data.correct_answer,
    )


@app.post("/test-question/")
async def test_question(data: QuestionCreate):
    return data


@app.get("/questions/{chapter}")
async def get_questions(chapter: str, db: Session = Depends(get_db)):
    return get_questions_by_chapter(db, chapter)


class UserResultCreate(BaseModel):
    user_id: int
    question_id: int
    user_answers: List[str]


@app.post("/add-user-result/")
async def store_user_result(
    user_result: UserResultCreate, db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == user_result.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question set not found")

    return add_user_result(
        db,
        user_result.user_id,
        user_result.question_id,
        user_result.user_answers,
        question.correct_answer,
    )
