from databases import Base
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship


class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)

association_table = Table(
    "association_table",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("category.id"), primary_key=True),
)


class DBBook(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    author = Column(String)
    count = Column(Integer)
    categories = relationship(
        "DBCategory", secondary=association_table, back_populates="books"
    )

class DBCategory(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    books = relationship(
        "DBBook", secondary=association_table, back_populates="categories"
    )
