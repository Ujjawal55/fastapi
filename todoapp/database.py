from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(SQL_DATABASE_URL, connect_args={"check same threads": False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
