
class Person:

    def __init__(self, first_name, last_name, user_id, access_hash, learning=0, hardworking=0, responsibility=0, teamworking=0, product_concern = 0,  other=0, pins=5):


        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.user_id = str(user_id)
        self.access_hash = str(access_hash)
        self.learning = int(learning)
        self.hardworking = int(hardworking)
        self.resposibility = int(responsibility)
        self.teamworking = int(teamworking)
        self.product_concern = int(product_concern)
        self.other = int(other)
        self.pins = int(pins)


    def __isadmin__(self):
        pass


class Reason:

    def __init__(self, text, pin_type_number, owner_id):

        self.text = str(text)
        self.pin_type_number = int(pin_type_number)
        self.owner_id = str(owner_id)

