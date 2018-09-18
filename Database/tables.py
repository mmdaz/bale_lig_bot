from Database.connect import Base
from sqlalchemy import Column, Integer, String
from Bot.template_messages import Message


class Person(Base):
    __tablename__ = "Persons"
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    access_hash = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    learning = Column(Integer)
    hardworking = Column(Integer)
    resposibility = Column(Integer)
    teamworking = Column(Integer)
    product_concern = Column(Integer)
    other = Column(Integer)
    pins = Column(Integer)
    total_pins = Column(Integer)

    def __init__(self, person):

        self.first_name = person.first_name
        self.last_name = person.last_name
        self.user_id = person.user_id
        self.access_hash = person.access_hash
        self.learning = person.learning
        self.teamworking = person.teamworking
        self.resposibility = person.resposibility
        self.hardworking = person.hardworking
        self.product_concern = person.product_concern
        self.other = person.other
        self.pins = person.pins
        self.total_pins = person.product_concern + person.teamworking + person.other + person.hardworking + person.resposibility + person.learning

    def __repr__(self):
        return "<Person(first_name = {}, last_name = {}, user_id = {}, access_hash = {}, learning = {}, teamworking = {}, resposibility = {}, hardworking = {}, other = {}, pins = {} )>".format(
            self.first_name, self.last_name, self.user_id, self.access_hash, self.learning, self.teamworking, self.resposibility, self.hardworking, self.other, self.pins
        )


class Reason(Base):
    __tablename__ = "Reasons"
    id = Column(Integer, primary_key=True)
    owner_id = Column(String)
    text = Column(String)
    pin_name = Column(String)

    def __init__(self, reason):
        self.owner_id = reason.owner_id
        self.text = reason.text
        self.pin_name = (reason.pin_type_number == 1 and Message.LEARNING) or (reason.pin_type_number == 2 and Message.HARDWORKING) or\
                        (reason.pin_type_number == 3 and Message.RESPONSIBILITI) or (reason.pin_type_number == 4 and Message.TEAMWORKING) or\
                        (reason.pin_type_number == 5 and Message.PRODUCT_CONCERN) or (reason.pin_type_number == 6 and Message.OTHER)





"""
{"$type":"Group","id":568560388,"accessHash":"-993816927678809060"}

"""