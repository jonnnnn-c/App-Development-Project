class User:
    countID = 0
    def __init__(self, firstName, lastName, gender, email, password):
        self.__firstName = firstName
        self.__lastName = lastName
        self.__gender = gender
        self.__email = email
        self.__password = password
        __class__.countID += 1     # User.countID += 1 (more tedious because if you were to change the class name, you have to keep changing this too)
        self.__userID = __class__.countID
        self.__type = ""
        print('in class')
        print(__class__.countID)


    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_password(self, newpassword):
        self.__password = newpassword

    def set_username(self, username):
        self.__username = username

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_userID(self):
        return self.__userID

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

class Login:
    def __init__(self, userID, password, type):
        self.__userID = userID
        self.__password = password
        self.__type = type

    def get_userID(self):
        return self.__userID

    def get_password(self):
        return self.__password

    def get_type(self):
        return self.__type

    def set_password(self, password):
        self.__password = password
