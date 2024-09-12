from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    """
    Representing a book in the database.

    Attributes:
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        author (str): The author of the book.
        genre (str): The genre of the book.
        year_published (int): The year the book was published.
        summary (str): A summary of the book.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    genre = Column(String(255))
    year_published = Column(Integer)
    summary = Column(Text)

    reviews = relationship(
        "Review",
        back_populates="book",
        cascade="all, delete-orphan"
    )


class Review(Base):
    """
    Representing a review of a book in the database.

    Attributes:
        id (int): The unique identifier for the review.
        book_id (int): The foreign key referencing the associated book.
        user_id (int): The identifier for the user who wrote the review.
        review_text (str): The text of the review.
        rating (int): The rating given in the review.
    """
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer)
    review_text = Column(Text)
    rating = Column(Integer)

    book = relationship(
        "Book",
        back_populates="reviews"
    )
