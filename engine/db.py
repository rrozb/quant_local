"""Database setup"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float

SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

class Candles(Base):
    "Creating model for OCHL data"
    __tablename__ = 'candles'
    id = Column(Integer, primary_key=True, index=True)
    MTS = Column(Integer)
    OPEN = Column(Float)
    CLOSE = Column(Float)
    HIGH = Column(Float)
    LOW = Column(Float)
    VOLUME = Column(Float)
    symbol = Column(String, nullable=False)   
    def __repr__(self):
        pass
Base.metadata.create_all(bind=engine)




class CandlesRepo:
    """CRUD operations for Candles table"""
    def create(candles, symbol):
        "Create Candle in DataBase"
        db_offer = Candles(MTS=candles[0], OPEN = candles[1], CLOSE = candles[2], HIGH = candles[3], LOW = candles[4], VOLUME = candles[5], symbol = symbol)
        session.add(db_offer)
        session.commit()
        session.refresh(db_offer)
        return db_offer