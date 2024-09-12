from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Book, Review
from schemas import BookCreate, ReviewCreate
from database import get_db
from llmmodelsetup import generate_summary
from mlmodel import model
from typing import Dict, List

app = FastAPI()

@app.post("/books", response_model=Book)
async def create_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db)
) -> Book:
    """
    Creating a new book entry.

    Args:
        book (BookCreate): The data to create a new book.
        db (AsyncSession): The database session dependency.

    Returns:
        Book: The newly created book.

    Raises:
        HTTPException: If there is an issue creating the book.
    """
    new_book = Book(**book.dict())
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    return new_book

@app.get("/books", response_model=List[Book])
async def get_books(
    db: AsyncSession = Depends(get_db)
) -> List[Book]:
    """
    Retrieving all books.

    Args:
        db (AsyncSession): The database session dependency.

    Returns:
        List[Book]: A list of all books.

    Raises:
        HTTPException: If there is an issue retrieving the books.
    """
    result = await db.execute(select(Book).order_by(Book.id))
    books = result.scalars().all()
    return books

@app.get("/books/{id}", response_model=Book)
async def get_book(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Book:
    """
    Retrieving a book by its ID.

    Args:
        id (int): The ID of the book to retrieve.
        db (AsyncSession): The database session dependency.

    Returns:
        Book: The book with the specified ID.

    Raises:
        HTTPException: If the book is not found.
    """
    book = await db.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{id}", response_model=Book)
async def update_book(
    id: int,
    book_data: BookCreate,
    db: AsyncSession = Depends(get_db)
) -> Book:
    """
    Updating an existing book entry.

    Args:
        id (int): The ID of the book to update.
        book_data (BookCreate): The new data to update the book with.
        db (AsyncSession): The database session dependency.

    Returns:
        Book: The updated book.

    Raises:
        HTTPException: If the book is not found.
    """
    book = await db.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_data.dict().items():
        setattr(book, key, value)
    await db.commit()
    await db.refresh(book)
    return book

@app.delete("/books/{id}")
async def delete_book(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> Dict[str, str]:
    """
    Deleting a book entry.

    Args:
        id (int): The ID of the book to delete.
        db (AsyncSession): The database session dependency.

    Returns:
        Dict[str, str]: A message confirming the deletion.

    Raises:
        HTTPException: If the book is not found.
    """
    book = await db.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted"}

@app.post("/books/{id}/reviews", response_model=Review)
async def create_review(
    id: int,
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db)
) -> Review:
    """
    Adding a review to a book.

    Args:
        id (int): The ID of the book to review.
        review (ReviewCreate): The data for the new review.
        db (AsyncSession): The database session dependency.

    Returns:
        Review: The newly created review.

    Raises:
        HTTPException: If the book is not found.
    """
    book = await db.get(Book, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    new_review = Review(**review.dict(), book_id=id)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

@app.get("/books/{id}/reviews", response_model=List[Review])
async def get_reviews(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> List[Review]:
    """
    Retrieving all reviews for a book.

    Args:
        id (int): The ID of the book for which to retrieve reviews.
        db (AsyncSession): The database session dependency.

    Returns:
        List[Review]: A list of reviews for the specified book.

    Raises:
        HTTPException: If the book is not found or there is an issue retrieving reviews.
    """
    result = await db.execute(select(Review).where(Review.book_id == id))
    reviews = result.scalars().all()
    return reviews

@app.post("/summarize")
async def summarize_text(
    text: str
) -> Dict[str, str]:
    """
    Generating a summary of the provided text using a pre-trained T5 model.

    Args:
        text (str): The text to be summarized.

    Returns:
        Dict[str, str]: A dictionary containing the generated summary.
    """
    summary = generate_summary(text)
    return {"summary": summary}

@app.get("/recommendations", response_model=Dict[str, str])
async def get_recommendations(
    genre: str,
    average_rating: float
) -> Dict[str, str]:
    """
    Providing a recommendation for a book based on its genre and average rating.

    Args:
        genre (str): The genre of the book.
        average_rating (float): The average rating of the book.

    Returns:
        Dict[str, str]: A dictionary with the recommendation result.

    Raises:
        HTTPException: If there is an issue with the recommendation process.
    """
    try:
        prediction = model.predict(genre, average_rating)
        if prediction == 1:
            return {"recommendation": "Recommended"}
        return {"recommendation": "Not Recommended"}
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid genre provided")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
