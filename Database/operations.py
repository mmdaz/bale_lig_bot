from Database.connect import *
from Database.tables import Person, Reason

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

def update_pins(id, pin_type, pin_numbers):
    session = session_factory()
    target_person =  session.query(Person).filter_by(id=id).first()
    if pin_type == 1:
        target_person.learning += pin_numbers
    elif pin_type == 2:
        target_person.hardworking += pin_numbers
    elif pin_type == 3:
        target_person.resposibility += 1
    elif pin_type == 4:
        target_person.teamworking += 1
    elif pin_type == 5 :
        target_person.product_concern +=1
    elif pin_type == 6:
        target_person.other += 1

    session.commit()
    session.close()

def save_reason(reason_from_bot):
    session = session_factory()
    reason = Reason(reason_from_bot)
    session.add(reason)
    session.commit()
    session.close()

