from pydantic import BaseModel
from typing import List, Optional

class ReviewBase(BaseModel):
    """
    Base model for review data.

    Attributes:
        review_text (str): The text of the review.
        rating (int): The rating given in the review (typically 1-5).
        user_id (Optional[int]): Optional ID of the user who made the review.
    """
    review_text: str
    rating: int
    user_id: Optional[int] = None

class ReviewCreate(ReviewBase):
    """
    Model for creating a review.

    Inherits from ReviewBase.
    """
    pass

class Review(ReviewBase):
    """
    Model representing a review with an ID and associated book ID.

    Attributes:
        id (int): The unique identifier of the review.
        book_id (int): The unique identifier of the book associated with the review.
    """
    id: int
    book_id: int

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    """
    Base model for book data.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        genre (Optional[str]): Optional genre of the book.
        year_published (Optional[int]): Optional year the book was published.
    """
    title: str
    author: str
    genre: Optional[str] = None
    year_published: Optional[int] = None

class BookCreate(BookBase):
    """
    Model for creating a book.

    Inherits from BookBase.
    """
    pass

class Book(BookBase):
    """
    Model representing a book with an ID, optional summary, and list of reviews.

    Attributes:
        id (int): The unique identifier of the book.
        summary (Optional[str]): Optional summary of the book.
        reviews (List[Review]): List of reviews associated with the book.
    """
    id: int
    summary: Optional[str] = None
    reviews: List[Review] = []

    class Config:
        orm_mode = True
