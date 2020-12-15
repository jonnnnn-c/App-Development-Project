import User as u

class Customer(u.User):
    def __init__(self, firstName, lastName, gender, email, password, contactNo, membPoints):
        super().__init__(firstName, lastName, gender, email, password)
        self.__contactNo = contactNo
        self.__membStatus = ""
        self.__membPoints = membPoints
        self.__accumulation = 0

    def set_contactNo(self, contactNo):
        self.__contactNo = contactNo

    def set_membStatus(self):
        if self.__accumulation<=100:
            self.__membStatus = "BRONZE"
        elif self.__accumulation<=200:
            self.__membStatus = "SILVER"
        elif self.__accumulation>200:
            self.__membStatus = "GOLD"

    def set_accumulation(self):
        self.__accumulation = self.__membPoints

    def increase_accumulation(self, value):
        self.__accumulation += value

    def add_points(self, value):
        self.__membPoints += value
        self.__accumulation += value

    def deduct_points(self,value):
        self.__membPoints -= value

    def set_membPoints(self, membPoints):
        self.__membPoints = membPoints

    def get_contactNo(self):
        return self.__contactNo

    def get_membStatus(self):
        return self.__membStatus

    def get_membPoints(self):
        return self.__membPoints



