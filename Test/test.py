from Database.operations import sort_by_all_elements, sort_by_special_field, reset_date

# sort_by_special_field()

def arabic_to_eng_number(number):
    number = str(number)
    return number.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


def eng_to_arabic_number(number):
    number = str(number)
    return number.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))

print(arabic_to_eng_number("65315"))