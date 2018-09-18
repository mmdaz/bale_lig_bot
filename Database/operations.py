from Database.connect import *
from Database.tables import Person, Reason


def get_pin_numbers(user_id):
    session = session_factory()
    target_person = session.query(Person).filter_by(user_id=user_id).first()
    return target_person


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
    target_person = session.query(Person).filter_by(id=id).first()
    if pin_type == 1:
        target_person.learning += pin_numbers
    elif pin_type == 2:
        target_person.hardworking += pin_numbers
    elif pin_type == 3:
        target_person.resposibility += pin_numbers
    elif pin_type == 4:
        target_person.teamworking += pin_numbers
    elif pin_type == 5:
        target_person.product_concern += pin_numbers
    elif pin_type == 6:
        target_person.other += pin_numbers

    target_person.total_pins = target_person.learning + target_person.resposibility + target_person.hardworking + target_person.teamworking + target_person.other + target_person.product_concern

    session.commit()
    session.close()


def update_pin_numbers(user_id, pin_numbers):
    session = session_factory()
    target_person = session.query(Person).filter_by(user_id=user_id).first()
    target_person.pins -= pin_numbers
    session.commit()
    session.close()


def save_reason(reason_from_bot):
    session = session_factory()
    reason = Reason(reason_from_bot)
    session.add(reason)
    session.commit()
    session.close()


def check_pins_limitation(user_id, pin_numbers):
    session = session_factory()
    target_person = session.query(Person).filter_by(user_id=user_id).first()
    if target_person.pins - pin_numbers < 0:
        session.close()
        return False
    else:
        session.close()
        return True


def check_person_validation(user_id, number_input):
    session = session_factory()
    all_persons = session.query(Person).all()
    target_person = session.query(Person).filter_by(id=number_input).first()
    if user_id == target_person.user_id:
        return False
    for p in all_persons:
        print(p.id)
        print(number_input)
        if p.id == int(number_input):
            return True
    return False


def sort_by_all_elements():
    persons = get_all_persons()
    persons.sort(key=lambda p: p.total_pins , reverse=True)
    persons_pins = [p.learning + p.hardworking + p.resposibility + p.teamworking + p.product_concern + p.other for p in
                    persons]
    sorted_list = [pin for pin in persons_pins]
    sorted_list.sort(reverse=True)
    return persons


def sort_by_special_field(pin_type_number):
    persons = get_all_persons()
    # TODO handle all fields
    if pin_type_number == 1:
        persons.sort(key=lambda p: p.other, reverse=True)
    if pin_type_number == 2:
        persons.sort(key=lambda p: p.other, reverse=True)
    if pin_type_number == 2:
        persons.sort(key=lambda p: p.other, reverse=True)
    if pin_type_number == 4:
        persons.sort(key=lambda p: p.other, reverse=True)
    if pin_type_number == 5:
        persons.sort(key=lambda p: p.other, reverse=True)
    if pin_type_number == 6:
        persons.sort(key=lambda p: p.other, reverse=True)

    return persons


def get_person_name_from_user_id(user_id):
    session = session_factory()
    target_person = session.query(Person).filter_by(user_id=user_id).first()
    return target_person


def check_register_validation(user_id):
    session = session_factory()
    persons_list = get_all_persons()
    for p in persons_list:
        if p.user_id == user_id:
            return False
    return True
