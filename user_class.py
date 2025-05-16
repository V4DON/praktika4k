from sqlalchemy import Integer, Column, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Connect:
    @staticmethod
    def create_connection():
        try:
            engine = create_engine("postgresql://postgres:1234@localhost:5432/podgotovka1")
            Base.metadata.create_all(engine)
            Session = sessionmaker(bind=engine)
            return Session()
        except SQLAlchemyError as e:
            print(f"Ошибка подключения к базе данных: {str(e)}")
            return None
    
    
class Partner(Base):
    __tablename__ = 'partners'
    partners_id = Column(Integer, primary_key=True, autoincrement=True)
    type_partner = Column(String)
    company_name = Column(String)
    director_name = Column(String)
    phone = Column(String)
    rating = Column(Integer)
    partnerproducts = relationship("PartnerProduct", back_populates="partner_relation")
    

class PartnerProduct(Base):
    __tablename__ = 'partnerproduct'
    pp_id = Column(Integer, primary_key=True)
    id_partner = Column(Integer, ForeignKey('partners.partners_id'))
    id_product = Column(Integer)
    count_product = Column(Integer)
    partner_relation = relationship("Partner", back_populates="partnerproducts")