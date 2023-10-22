from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, exists
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import httpx
from pydantic import BaseModel


DATABASE_URL = "postgresql+asyncpg://user:password@postgres:5432/db_name"
Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)


class QuestionsNum(BaseModel):
    questions_num: int
app = FastAPI()


async def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


@app.on_event("startup")
async def startup_event():
    await create_tables()   

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def fetch_and_store_questions(db: AsyncSession, questions_num: int):
    async with httpx.AsyncClient() as client:
        for _ in range(questions_num):
            response = await client.get("https://jservice.io/api/random?count=1")
            data = response.json()[0]

            is_exists = await db.execute(select(exists().where(Question.id == data["id"])))
            is_exists = is_exists.scalar_one_or_none()

            while is_exists:
                response = await client.get("https://jservice.io/api/random?count=1")
                data = response.json()[0]
                is_exists = await db.execute(select(exists().where(Question.id == data["id"])))
                is_exists = is_exists.scalar_one_or_none()

            question_data = Question(
                id=data["id"],
                question=data["question"],
                answer=data["answer"],
                creation_date=datetime.strptime(data["airdate"], '%Y-%m-%dT%H:%M:%S.%fZ')
            )
            db.add(question_data)

    await db.commit()

@app.post("/questions/")
async def get_questions(questions_data: QuestionsNum, db: AsyncSession = Depends(get_db)):
    await fetch_and_store_questions(db, questions_data.questions_num)

    result = await db.execute(select(Question).order_by(Question.id.desc()).limit(1))
    last_question = result.scalar_one_or_none()
    return last_question.__dict__ if last_question else {"message": "No questions added yet"}



if __name__ == "__main__":  
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
