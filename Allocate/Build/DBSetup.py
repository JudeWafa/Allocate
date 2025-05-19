from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///Databases.db", echo=True)

Base = declarative_base()

session = sessionmaker(bind=engine)

def init_db():
    import Build.DBCreation
    Base.metadata.create_all(bind=engine)
