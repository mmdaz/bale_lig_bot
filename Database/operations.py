from Database.connect import *
from Database.tables import Person

def get_pin_numbers(user_id):
    session = session_factory()
    target_person = session.query(Person).filter_by(user_id=user_id).first()
    return target_person.pins

def save_person(person_from_bot):
    session = session_factory()
    person = Person(person_from_bot)
    session.add(person)
    session.commit()
    session.close()



