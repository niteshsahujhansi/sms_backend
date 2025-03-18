from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Association(Base):
    __tablename__ = "association_table"

    left_id: Mapped[int] = mapped_column(ForeignKey("left_table.id"), primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey("right_table.id"), primary_key=True)
    extra_data: Mapped[Optional[str]]

    child: Mapped["Child"] = relationship(back_populates="parent_associations")
    parent: Mapped["Parent"] = relationship(back_populates="child_associations")

class Parent(Base):
    __tablename__ = "left_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    children: Mapped[List["Child"]] = relationship(secondary="association_table", back_populates="parents")
    child_associations: Mapped[List["Association"]] = relationship(back_populates="parent")


class Child(Base):
    __tablename__ = "right_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    parents: Mapped[List["Parent"]] = relationship(secondary="association_table", back_populates="children")
    parent_associations: Mapped[List["Association"]] = relationship(back_populates="child")