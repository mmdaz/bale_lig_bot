
class Person():

    def __init__(self, first_name, last_name, user_id, access_hash, learning=0, hardworking=0, responsibility=0, teamworking=0, other=0, pins=5):


        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.user_id = str(user_id)
        self.access_hash = str(access_hash)
        self.learning = int(learning)
        self.hardworking = int(hardworking)
        self.resposibility = int(responsibility)
        self.teamworking = int(teamworking)
        self.other = int(other)
        self.pins = int(pins)


    def __isadmin__(self):
        pass

