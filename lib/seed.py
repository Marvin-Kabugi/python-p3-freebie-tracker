#!/usr/bin/env python3

from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Company, Freebie, Dev, company_dev, session
import random

if __name__ == '__main__':
    # engine = create_engine('sqlite:///freebies.db')
    # Session = sessionmaker(bind=engine)
    # session = Session()

    session.query(Company).delete()
    session.query(Dev).delete()
    session.query(Freebie).delete()
    session.query(company_dev).delete()

    faker = Faker()
    companies = []
    for i in range(50):
        company = Company(
            name = faker.company(),
            founding_year = random.randint(1990, 2023)
        )

        session.add(company)
        session.commit()
        companies.append(company)


    devs = []
    for i in range(50):
        dev = Dev(
            name=faker.name()
        )

        session.add(dev)
        session.commit()

        devs.append(dev)

    platforms = ['nintendo 64', 'gamecube', 'wii', 'wii u', 'switch',
        'playstation', 'playstation 2', 'playstation 3', 'playstation 4',
        'playstation 5', 'xbox', 'xbox 360', 'xbox one', 'pc']
    
    freebies = []
    for company in companies:
        for i in range(random.randint(1,5)):
            dev = random.choice(devs)
            if company not in dev.companies:
                dev.companies.append(company)
                session.add(dev)
                session.commit()
                
            freebie = Freebie(
                item_name = platforms[random.randint(0, len(platforms) - 1)],
                value = random.randint(100, 5000),
                dev_id = dev.id,
                company_id = company.id,
            )

            freebies.append(freebie)

    session.bulk_save_objects(freebies)
    session.commit()
    session.close()

