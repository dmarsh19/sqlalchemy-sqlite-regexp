#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Transaction

DB_NAME = "txns"


def main():
    engine = create_engine("sqlite:///{}.sqlite".format(DB_NAME))
    session_factory = sessionmaker(bind=engine)

    # create teh tables from the defined model(s)
    Base.metadata.create_all(engine)

    session = session_factory()
    # insert some FALSE test data
    session.add_all([
        Transaction(description="Purchase: 12345678 100 Main St TARGET T-0111 Atlanta GA Card: ****1111 11/22/2015",),
        Transaction(description="Purchase: LK111222 FRESH MKT-011 ATL ATLANTA GA Card: ****2222 11/22/2015",),
        Transaction(description="Purchase: 12345678 100 Main St TARGET T-0111 Atlanta GA Card: ****1111 11/25/2015",),
        Transaction(description="Purchase: 111 2222 SUR LA TABLE DIRECT 800-123-4567 WA Card: ****2222 11/25/2015",),
        Transaction(description="Deposit SOMEWHERE CO-DIR DEP *****2222"),
        Transaction(description="Deposit SOMEWHERE ELSE CO-DIR DEP *****1111"),
        Transaction(description="Withdrawal VENMO-PAYMENT *****1111 (S)"),
        Transaction(description="Withdrawal Check # 1111 Trace: 123456789")
    ])
    session.commit()


if __name__ == "__main__":
    main()

