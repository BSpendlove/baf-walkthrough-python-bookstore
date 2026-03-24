from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.isbn import validate_isbn13
from app.models import Book
from app.schemas import BookCreate, BookResponse, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)) -> Book:
    try:
        normalized_isbn = validate_isbn13(book.isbn)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    db_book = Book(
        title=book.title,
        author=book.author,
        isbn=normalized_isbn,
        price=book.price,
        published_year=book.published_year,
        description=book.description,
    )
    db.add(db_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists")
    db.refresh(db_book)
    return db_book


@router.get("", response_model=list[BookResponse])
def list_books(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Book]:
    return list(db.query(Book).offset(skip).limit(limit).all())


@router.get("/search", response_model=list[BookResponse])
def search_books(
    q: str = Query(...),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[Book]:
    pattern = f"%{q}%"
    return list(
        db.query(Book)
        .filter(or_(Book.title.ilike(pattern), Book.author.ilike(pattern)))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)
) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)

    if "isbn" in update_data:
        try:
            update_data["isbn"] = validate_isbn13(update_data["isbn"])
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))

    for field, value in update_data.items():
        setattr(book, field, value)

    book.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="A book with this ISBN already exists")
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
