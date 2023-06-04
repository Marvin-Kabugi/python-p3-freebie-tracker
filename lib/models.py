from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

company_dev = Table(
    'company_devs',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('dev_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    freebies = relationship('Freebie', backref='company')
    devs = relationship('Dev', secondary=company_dev, back_populates='companies')

    @classmethod
    def oldest_compay(cls):
        return session.query(Company).order_by(Company.founding_year.asc()).first()

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(
            item_name = item_name,
            value = value,
            dev_id = dev.id,
            company_id = self.id
        )
        dev.companies.append(self)
        session.add(freebie)
        # session.add(dev)
        session.commit()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    freebies = relationship('Freebie', backref='dev')
    companies = relationship('Company', secondary=company_dev, back_populates='devs')
    
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
            else:
                return False
            
    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
        
            # session.add(freebie)
            # session.commit()

    def __repr__(self):
        return f'<Dev {self.name}>'


class Freebie(Base): 
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def print_details(self):
        return f'{self.dev} owns a ' + \
            f'{self.item_name} from {self.company}'
    

    def __repr__(self) -> str:
        return f'<Freebie {self.id} {self.item_name}'