import User as u

class Staff(u.User):
    def __init__(self, firstName, lastName, gender, email, password):
        super().__init__(firstName, lastName, gender, email, password)
        #self.__userID = super().countID





