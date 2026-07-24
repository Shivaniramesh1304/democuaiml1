from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, ConfigDict
#databse setup
DATABASE_URL = "sqlite:///./company.db"
engine = create_engine(
DATABASE_URL,
connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
#SQLAlchemy Model
class EmployeeDB(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String)
    department=Column(String)
    salary=Column(Float)    
Base.metadata.create_all(bind=engine)
# Pydantic Schemas
class EmployeeBase(BaseModel):
    name: str
    department: str
    salary: float
class EmployeeResponse(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
# FastAPI App
app = FastAPI()
# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# CRUD APIs
@app.post("/employees/", response_model=EmployeeResponse)
def create_employee(emp: EmployeeBase, db: Session = Depends(get_db)):
    new_emp = EmployeeDB(**emp.model_dump())
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return new_emp

@app.get("/employees/", response_model=list[EmployeeResponse])
def read_employees(db: Session = Depends(get_db)):
    return db.query(EmployeeDB).all()

@app.put("/employees/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: int, emp: EmployeeBase, db: Session = Depends(get_db)):
    db_emp = db.query(EmployeeDB).filter(EmployeeDB.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    for k, v in emp.model_dump().items():
        setattr(db_emp, k, v)

    db.commit()
    db.refresh(db_emp)
    return db_emp

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    db_emp = db.query(EmployeeDB).filter(EmployeeDB.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(db_emp)
    db.commit()
    return {"message": "Employee deleted successfully"}