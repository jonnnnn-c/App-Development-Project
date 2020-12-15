class Feedback:

    def __init__(self, id, firstName, lastName, email, phone, region, surveyOne, surveyTwo, improvements):
        self.__feedbackID = id
        self.__firstName = firstName
        self.__lastName = lastName
        self.__email = email
        self.__phone = phone
        self.__region = region
        self.__surveyOne = surveyOne
        self.__surveyTwo = surveyTwo
        self.__improvements = improvements

    # getter
    def get_feedbackID(self):
        return self.__feedbackID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_region(self):
        return self.__region

    def get_surveyOne(self):
        return self.__surveyOne

    def get_surveyTwo(self):
        return self.__surveyTwo

    def get_improvements(self):
        return self.__improvements

    # setter
    def set_feedbackID(self, feedbackID):
        self.__feedbackID = feedbackID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_email(self, email):
        self.__email = email

    def set_phone(self, phone):
        self.__phone = phone

    def set_country(self, region):
        self.__region = region

    def set_surveyOne(self, surveyOne):
        self.__surveyOne = surveyOne

    def set_surveyTwo(self, surveyTwo):
        self.__surveyTwo = surveyTwo

    def set_improvements(self, improvements):
        self.__improvements = improvements
