from models import Question, UserResult
from sqlalchemy.orm import Session


def add_question(
    db: Session, chapter: str, question_text: list, options: list, correct_answer: list
):
    """Function to add items questions to database"""

    db_question = Question(
        chapter=chapter,
        question_text=question_text,
        options=options,
        correct_answer=correct_answer,
    )

    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


##function to add users result


def add_user_result(
    db: Session,
    user_id: int,
    question_id: int,
    user_answers: list,
    correct_answers: list,
):
    """calculates users result"""
    correct_count = sum(
        1
        for users_ans, correct_ans in zip(user_answers, correct_answers)
        if users_ans == correct_ans
    )
    db_result = UserResult(
        user_id=user_id,
        question_id=question_id,
        user_answer=user_answers,
        is_correct=correct_count,
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_questions_by_chapter(db: Session, chapter: str):
    """Function to get all questions for a specific chapter"""

    questions = db.query(Question).filter(Question.chapter == chapter).all()
    return questions
