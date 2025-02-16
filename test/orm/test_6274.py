from sqlalchemy import Integer, union, select
from sqlalchemy.orm import declarative_base, aliased

from sqlalchemy.testing.schema import Table, Column
from sqlalchemy.testing import fixtures

class Test6274(fixtures.MappedTest):

    @classmethod
    def define_tables(cls, metadata):
        Table("testtable", metadata, Column("id", Integer, primary_key=True))

    @classmethod
    def setup_classes(cls):

        Base = declarative_base()
        class TestTable(Base):
            __tablename__ = "testtable"
            id = Column(Integer, primary_key=True)

        cls.classes.TestTable = TestTable


    def test_6274(self):
        TestTable = self.classes.TestTable
        q1 = select(TestTable).filter(TestTable.id == 1)
        q2 = select(TestTable).filter(TestTable.id == 2)
        q3 = aliased(element=union(q1, q2), name="test_table")
        assert q3.name == "test_table"