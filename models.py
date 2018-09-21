from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "Transactions"

    transactionid = Column("TransactionId", Integer, primary_key=True)
    description = Column("Description", String)

