from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from database import SessionLocal, Todo

app = FastAPI()

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: str
    done: bool

@app.get("/todos", response_model=List[TodoUpdate])
def get_todos():
    db = SessionLocal()
    return db.query(Todo).all()

@app.post("/todos", response_model=TodoUpdate)
def create_todo(todo: TodoCreate):
    db = SessionLocal()
    new_todo = Todo(title=todo.title, done=False)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", response_model=TodoUpdate)
def update_todo(todo_id: int, todo: TodoUpdate):
    db = SessionLocal()
    target = db.query(Todo).filter(Todo.id == todo_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Not found")
    target.title = todo.title
    target.done = todo.done
    db.commit()
    return target

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    target = db.query(Todo).filter(Todo.id == todo_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(target)
    db.commit()
    return {"message": "deleted"}
