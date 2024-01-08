from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import DBUser, DBBook, DBCategory
from databases import engine, SessionLocal, Base
from auth import is_admin, get_current_user, create_access_token
from schemas import UserCreate, UserResponse, UserLogin, BookCreate, Book, BookBase, CategoryResponse
from typing import List

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/user/register", response_model=UserResponse)
async def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(DBUser).filter(DBUser.email == user_create.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = DBUser(name=user_create.name, email=user_create.email, password=user_create.password, is_admin=user_create.is_admin)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully", "user_details":user, "status": status.HTTP_201_CREATED}


@app.post("/api/user/login", response_model=dict)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.email == user_credentials.email, DBUser.password == user_credentials.password).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Create and return JWT token
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/book", response_model=Book, dependencies=[Depends(is_admin)])
async def create_book(book_create: BookCreate, db: Session = Depends(get_db)):
    try:
        book = DBBook(**book_create.dict())
        book = db.query(book_create)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    except HTTPException as e:
        # Handle the HTTPException raised by is_admin dependency
        if e.status_code == status.HTTP_403_FORBIDDEN:
            return {"message": "Permission denied, admin only"}
        raise


@app.get("/api/books", response_model=List[Book], dependencies=[Depends(get_current_user)])
async def get_all_books(db: Session = Depends(get_db)):
    books = db.query(DBBook).all()
    return books


@app.get("/api/book/{book_id}", response_model=Book, dependencies=[Depends(get_current_user)])
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.put("/api/book/{book_id}", response_model=Book, dependencies=[Depends(is_admin)])
def update_book(book_id: int, book_update: BookBase, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    # Update book properties
    for key, value in book_update.dict(exclude_unset=True).items():

        """This function is used to set the attribute (property) of the db_book object 
        with the specified key to the provided value. Essentially, it dynamically 
        updates each property of the db_book with the corresponding values from the book_update dictionary."""

        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.delete("/api/book/{book_id}", response_model=dict, dependencies=[Depends(is_admin)])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(DBBook).filter(DBBook.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(db_book)
    db.commit()

    return {"message": "Book deleted successfully", "status_code": status.HTTP_200_OK}



@app.post("/api/category", response_model=dict, dependencies=[Depends(get_current_user)])
async def create_category(category: CategoryResponse, db: Session = Depends(get_db)):
    category = DBCategory(**category.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category