from Database.connect import Base
from sqlalchemy import Column, Integer, String


class Person(Base):
    __tablename__ = "Persons"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    access_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    learning = Column(Integer)
    hardworking = Column(String)
    resposibility = Column(String)
    teamworking = Column(String)
    other = Column(String)
    pins = Column(Integer)

    def __init__(self, person):

        self.first_name = person.first_name
        self.last_name = person.last_name
        self.user_id = person.user_id
        self.access_hash = person.access_hash
        self.learning = person.learning
        self.teamworking = person.teamworking
        self.resposibility = person.resposibility
        self.hardworking = person.hardworking
        self.other = person.other
        self.pins = person.pins

    def __repr__(self):
        return "<Person(first_name = {}, last_name = {}, user_id = {}, access_hash = {}, learning = {}, teamworking = {}, resposibility = {}, hardworking = {}, other = {}, pins = {} )>".format(
            self.first_name, self.last_name, self.user_id, self.access_hash, self.learning, self.teamworking, self.resposibility, self.hardworking, self.other, self.pins
        )

    