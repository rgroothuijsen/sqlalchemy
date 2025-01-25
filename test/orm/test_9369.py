from typing import List

from sqlalchemy import Table, Column, Integer, ForeignKey, testing
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.testing import fixtures


class Test9369(fixtures.MappedTest):
    @classmethod
    def define_tables(cls, metadata):
        Table("foo",
            metadata,
            Column("id", Integer, primary_key=True)
        )
        Table("bar",
            metadata,
            Column("id", Integer, primary_key=True)
        )
    @classmethod
    def setup_classes(cls):
        class Base:
            __allow_unmapped__ = True

            # raises, but shouldn't (right?)
            id: int = Column(Integer, primary_key=True)

        Base = declarative_base(cls=Base)

        # existing mapping proceeds, Declarative will ignore any annotations
        # which don't include ``Mapped[]``
        class Foo(Base):
            __tablename__ = "foo"

            bars: List["Bar"] = relationship("Bar", back_populates="foo")

        class Bar(Base):
            __tablename__ = "bar"
            foo_id = Column(ForeignKey("foo.id"))

            foo: Foo = relationship(Foo, back_populates="bars", cascade="all")

    def test_9369(self):
         pass