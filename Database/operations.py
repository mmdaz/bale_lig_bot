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


def get_all_persons():
    session = session_factory()
    persons_list = session.query(Person).all()
    session.close()
    return persons_list

def update_pins(person, pin_type, pin_numbers):
    session = session_factory()
    target_person =  session.query(Person).filter_by(person.id).first()
    if pin_type == 1:
        target_person.learning += pin_numbers
    elif pin_type == 2:
        target_person.hardworking += pin_numbers
    elif pin_type == 3:
        target_person.responsibility += 1
    elif pin_type == 4:
        target_person.teamworking += 1
    elif pin_type == 5:
        target_person.other += 1

    session.commit()
    session.close()


