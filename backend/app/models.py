from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    chapter = Column(String, index=True)
    question_text = Column(String)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_answer = Column(String)

    user_results = relationship("UserResult", back_populates="question")

    def __repr__(self):
        return f"<Question(id={self.id}, chapter={self.chapter}, question_text={self.question_text})>"


class UserResult(Base):
    __tablename__ = "user_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(String)
    is_correct = Column(Boolean)

    question = relationship("Question", back_populates="user_results")

    def __repr__(self):
        return f"<UserResult(id={self.id}, user_id={self.user_id}, question_id={self.question_id})>"
