

from sqlalchemy import Integer, ForeignKey, inspect
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.testing import fixtures

from lib.sqlalchemy import MetaData


class Test8068(fixtures.MappedTest):
    @classmethod
    def define_tables(cls, metadata):
        Table("parent",
              metadata,
              Column("id", Integer, primary_key=True))
        Table("secondary",
              metadata,
              Column("id", Integer, primary_key=True))
        Table("child", metadata,
              Column("id", Integer, primary_key=True))

    @classmethod
    def setup_classes(cls):
        metadata = MetaData(schema="test_schema")
        Base = declarative_base(metadata=metadata)

        class Parent(Base):
            __tablename__ = "parent"
            id = Column(Integer, primary_key=True)
            children = relationship(
                # fails
                "Child", back_populates="parent", secondary="secondary"
                # works
                #  "Child", back_populates="parent", secondary="test_schema.secondary"
            )

        class Secondary(Base):
            __tablename__ = "secondary"
            fk_parent = Column(Integer, ForeignKey("parent.id"), primary_key=True)
            fk_child = Column(Integer, ForeignKey("child.id"), primary_key=True)

        class Child(Base):
            __tablename__ = "child"
            id = Column(Integer, primary_key=True)
            parent = relationship(
                # fails
                "Parent", back_populates="children", secondary="test_schema.secondary"
                # works
                # "Parent", back_populates="children", secondary="test_schema.secondary"
            )
        cls.classes.Child = Child
        cls.classes.Secondary = Secondary
        cls.classes.Parent = Parent

    def test_8068(self):
        ParentTable = self.classes.Parent.__table__
        SecondaryTable = self.classes.Secondary.__table__
        assert SecondaryTable.c.fk_parent.references(ParentTable.c.id)

        insp = inspect(self.classes.Child)

        for a in insp.relationships:
            print(a)