#!/usr/bin/env python3
import re

from sqlalchemy import event, func
from sqlalchemy.sql import label
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Transaction

DB_NAME = "txns"


def main():
    engine = create_engine("sqlite:///{}.sqlite".format(DB_NAME))
    session_factory = sessionmaker(bind=engine)
    session = session_factory()


    # select records based on a REGEXP WHERE clause
    query = session.query(Transaction).filter(Transaction.description.op("REGEXP")("^Withdrawal"))
    for record in query.all():
        print("{r.transactionid}: {r.description}".format(r=record))

    # alter the return of the column with a regexp_replace
    query = session.query(Transaction.transactionid,
                          label('description', func.regexp_replace(Transaction.description, '^\D*: \d* ', '')))
    for record in query.all():
        print("{r.transactionid}: {r.description}".format(r=record))


@event.listens_for(Engine, "connect")
def sqlite_engine_connect(dbapi_connection, connection_record):
    # regexp function in SQLite maps to a call of REGEXP
    dbapi_connection.create_function("regexp", 2, sqlite_regexp)
    dbapi_connection.create_function("REGEXP_REPLACE", 3, sqlite_regexp_replace)


def sqlite_regexp(expr, item):
    reg = re.compile(expr, re.IGNORECASE)
    return reg.search(item) is not None


def sqlite_regexp_replace(item, find, repl):
    reg = re.compile(find, re.IGNORECASE)
    return reg.sub(repl, item)


if __name__ == "__main__":
    main()

