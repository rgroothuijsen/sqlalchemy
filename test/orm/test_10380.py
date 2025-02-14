import dataclasses
from inspect import getfullargspec
from typing import Optional, List, Union

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column, composite, declarative_base
from sqlalchemy.sql.ddl import CreateTable
from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.testing import fixtures

class Test10380(fixtures.MappedTest):

    @classmethod
    def define_tables(cls, metadata):
        Table(
            "points",
            metadata,
            Column("x", Integer),
            Column("y", Integer)
        )

        Table(
            "vertices",
            metadata,
            Column("id", Integer, primary_key=True),
            Column("x1", Integer),
            Column("y1", Integer),
            Column("x2", Integer),
            Column("y2", Integer)
        )

    @classmethod
    def setup_classes(cls):
        Base = declarative_base()

        @dataclasses.dataclass
        class OptionalPoint:
            x: Optional[int]
            y: Optional[int]

        @dataclasses.dataclass
        class Point:
            x: int
            y: int

        x2 = mapped_column("x2")
        x1 = mapped_column("x1")
        @dataclasses.dataclass
        class Vertex(Base):
            __tablename__ = "vertices"
            id: Mapped[int] = mapped_column(primary_key=True)
            start: Mapped[Point] = composite(x1, mapped_column("y1"))
            end: Mapped[OptionalPoint] = composite(x2, mapped_column("y2"))
            # end: Mapped[Point] = composite(mapped_column("x2"), mapped_column("y2"))

        # print(x1.column.type)
        # print(x2.column.type)
        cls.classes.Vertex = Vertex
        cls.classes.Point = Point


    def test_10380(self):
        # testing.skip_test("10380")
        print(CreateTable(self.classes.Vertex.__table__))