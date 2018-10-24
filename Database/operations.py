from Database.connect import *
from Database.tables import Person, Reason


def persian_sort(e):
    print(e)
    alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
    alphabet += "absdefghigklmnopqrstuvwxyz"
    return alphabet.index(e[0])


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


def is_registered(user_id):
    persons = get_all_persons()
    for person in persons:
        if person.user_id == user_id:
            return True

    return False


def get_all_persons():
    session = session_factory()
    persons_list = session.query(Person).order_by(Person.last_name).all()
    persons_list.sort(key=lambda p: persian_sort(str(p.last_name)), reverse=False)
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
    persons.sort(key=lambda p: p.total_pins, reverse=True)
    ranck_list = [persons[0]]
    counter = 0
    for i in range(1, len(persons)):
        if counter > 2:
            break
        ranck_list.append(persons[i])
        if persons[i].total_pins != persons[counter]:
            counter += 1

    print(len(ranck_list))

    persons_pins = [p.learning + p.hardworking + p.resposibility + p.teamworking + p.product_concern + p.other for p in
                    persons]
    sorted_list = [pin for pin in persons_pins]
    sorted_list.sort(reverse=True)
    return ranck_list


def sort_by_special_field():
    persons = get_all_persons()
    persons_list = list(persons)
    fields = []
    persons_list.sort(key=lambda p: p.learning, reverse=True)
    ranck_list = [persons_list[0]]
    counter = 0
    for i in range(1, len(persons_list)):
        if counter > 0:
            break
        ranck_list.append(persons_list[i])
        if persons_list[0].learning != persons_list[i].learning:
            counter += 1
    fields.append([p for p in ranck_list])
    persons_list.sort(key=lambda p: p.hardworking, reverse=True)
    ranck_list = [persons_list[0]]
    counter = 0
    for i in range(1, len(persons_list)):
        if counter > 0:
            break
        ranck_list.append(persons_list[i])
        if persons_list[0].hardworking != persons_list[i].hardworking:
            counter += 1
    fields.append([p for p in ranck_list])
    persons_list.sort(key=lambda p: p.resposibility, reverse=True)
    ranck_list = [persons_list[0]]
    counter = 0
    for i in range(1, len(persons_list)):
        if counter > 0:
            break
        ranck_list.append(persons_list[i])
        if persons_list[0].resposibility != persons_list[i].resposibility:
            counter += 1
    fields.append([p for p in ranck_list])
    persons_list.sort(key=lambda p: p.teamworking, reverse=True)
    ranck_list = [persons_list[0]]
    counter = 0
    for i in range(1, len(persons_list)):
        if counter > 0:
            break
        ranck_list.append(persons_list[i])
        if persons_list[0].teamworking != persons_list[i].teamworking:
            counter += 1
    fields.append([p for p in ranck_list])
    persons_list.sort(key=lambda p: p.product_concern, reverse=True)
    ranck_list = [persons_list[0]]
    counter = 0
    for i in range(1, len(persons_list)):
        if counter > 0:
            break
        ranck_list.append(persons_list[i])
        if persons_list[0].product_concern != persons_list[i].product_concern:
            counter += 1
    fields.append([p for p in ranck_list])
    persons_list.sort(key=lambda p: p.other, reverse=True)
    ranck_list = [persons_list[0]]
    counter = 0
    for i in range(1, len(persons_list)):
        if counter > 0:
            break
        ranck_list.append(persons_list[i])
        if persons_list[0].other != persons_list[i].other:
            counter += 1
    fields.append([p for p in ranck_list])

    return fields


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


def reset_date():
    session = session_factory()
    persons = session.query(Person).all()
    for p in persons:
        p.product_concern = 0
        p.teamworking = 0
        p.resposibility = 0
        p.hardworking = 0
        p.learning = 0
        p.other = 0
        p.total_pins = 0
        p.pins = 5
        session.commit()
    for r in session.query(Reason).all():
        session.delete(r)
        session.commit()

    session.close()
