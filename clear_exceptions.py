import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import *

engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(bind=engine)

session = Session()

def main():
    for exception in session.query(PythonException).all():
        session.delete(exception)
        print "Deleted exception"
    session.commit()


if __name__ == '__main__':
    main()
