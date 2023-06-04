#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    freebie = session.query(Freebie).first()
    print('_' * 50 + 'Freebie' + '_' * 50)
    print(freebie)
    print(freebie.dev)
    dev2 = freebie.dev
    print(freebie.company)
    print(freebie.print_details())
    # print('_' * 100)

    company = session.query(Company).first()
    print('_' * 50 + 'Company' + '_' * 50)
    dev = session.query(Dev).first()
    company.give_freebie(dev2, 'bike', 4000)
    session.add(dev2)
    session.commit()
    print(dev2)
    print(dev.freebies)
    print(company)
    print(company.freebies)
    print(company.devs)
    print(Company.oldest_compay())
    # print('_' * 100)

    # dev = session.query(Dev).first()
    freebie2 = session.query(Freebie).filter(Freebie.item_name == 'bike', Freebie.id == 151).first()
    print('_' * 50 + 'Dev' + '_' * 50)
    print(dev)
    print(dev.freebies)
    print(dev.companies)
    print(dev.received_one('playstation'))
    print(dev.give_away(dev2, freebie2))
    session.add(freebie2)
    session.commit()
    # print('_' * 100)
    print(dev2.freebies)
    print(company.devs)
    session.close()

    import pdb; pdb.set_trace()
