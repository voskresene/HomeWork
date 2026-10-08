from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime
import random
from backend.database import SessionLocal, engine, Base
from backend.models import User, Task, AuthCode
from pydantic import BaseModel

# Создаем таблицы
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

# ... [database and models imports] ...

app = FastAPI(title="Task Manager TG")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... [rest of the routes] ...


# Схемы Pydantic
class AuthRequest(BaseModel):
    phone: str

class VerifyRequest(BaseModel):
    phone: str
    code: str

class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime.datetime
    location: str = None

class TaskResponse(TaskCreate):
    id: int
    user_id: int
    is_completed: bool

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/auth/request")
def request_auth(data: AuthRequest, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже кода
    existing = db.query(AuthCode).filter(AuthCode.phone == data.phone, AuthCode.is_used == False).first()
    if existing:
        return {"message": "Code already sent"}
    
    # Генерируем код
    code = str(random.randint(100000, 999999))
    new_code = AuthCode(
        phone=data.phone,
        code=code,
        expires_at=datetime.datetime.now() + datetime.timedelta(minutes=5)
    )
    db.add(new_code)
    db.commit()
    
    # Здесь должна быть логика отправки сообщения в TG (через бота)
    # Для теста пока просто возвращаем сообщение, что код "отправлен"
    return {"message": f"Code sent to {data.phone} (Simulated: {code})"}

@app.post("/auth/verify")
def verify_auth(data: VerifyRequest, db: Session = Depends(get_db)):
    code_record = db.query(AuthCode).filter(
        AuthCode.phone == data.phone, 
        AuthCode.code == data.code, 
        AuthCode.is_used == False
    ).first()
    
    if not code_record or code_record.expires_at < datetime.datetime.now():
        raise HTTPException(status_code=400, detail="Invalid or expired code")
    
    code_record.is_used = True
    db.commit()
    
    # В реальности здесь создаем/обновляем пользователя и возвращаем JWT
    return {"message": "Success", "user_id": 1} # Заглушка ID

@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    # Для примера возвращаем все задачи (в реальности фильтруем по user_id)
    tasks = db.query(Task).all()
    return tasks

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(
        title=task.title,
        description=task.description,
        due_date=task.due_date,
        location=task.location,
        user_id=1 # Заглушка
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
