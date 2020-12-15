class Supplier:

    def __init__(self, companyName, companyPhone, companyEmail, address, postalCode):

        self.__companyName = companyName
        self.__companyPhone = companyPhone
        self.__companyEmail = companyEmail
        self.__address = address
        self.__postalCode = postalCode
        self.__numOrders = 0

    def get_companyName(self):
        return self.__companyName

    def get_companyPhone(self):
        return self.__companyPhone

    def get_companyEmail(self):
        return self.__companyEmail

    def get_address(self):
        return self.__address

    def get_postalCode(self):
        return self.__postalCode

    def get_numOrders(self):
        return self.__numOrders


    def set_companyName(self, companyName):
        self.__companyName = companyName

    def set_companyPhone(self, companyPhone):
        self.__companyPhone = companyPhone

    def set_companyEmail(self, companyEmail):
        self.__companyEmail = companyEmail

    def set_address(self, address):
        self.__address = address

    def set_postalCode(self, postalCode):
        self.__postalCode = postalCode

    def set_numOrders(self, numOrders):
        self.__numOrders = numOrders
