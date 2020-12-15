class Order:

    def __init__(self, id, companyName, product, productQuantity, productPrice, deliveryDate, deliveryStatus):
        self.__orderID = id
        self.__companyName = companyName

        self.__product = product
        self.__productQuantity = productQuantity
        self.__productPrice = productPrice
        self.__totalPrice = 0

        self.__deliveryDate = deliveryDate
        self.__deliveryStatus = deliveryStatus

    def get_orderID(self):
        return self.__orderID

    def get_companyName(self):
        return self.__companyName

    def get_product(self):
        return self.__product

    def get_productQuantity(self):
        return self.__productQuantity

    def get_productPrice(self):
        return self.__productPrice

    def get_totalPrice(self):
        return self.__totalPrice

    def get_deliveryDate(self):
        return self.__deliveryDate

    def get_deliveryStatus(self):
        return self.__deliveryStatus


    def set_orderID(self, orderID):
        self.__orderID = orderID

    def set_companyName(self, companyName):
        self.__companyName = companyName

    def set_product(self, product):
        self.__product = product

    def set_productQuantity(self, productQuantity):
        self.__productQuantity = productQuantity

    def set_productPrice(self, productPrice):
        self.__productPrice = productPrice

    def set_totalPrice(self, totalPrice):
        self.__totalPrice = totalPrice

    def set_deliveryDate(self, deliveryDate):
        self.__deliveryDate = deliveryDate

    def set_deliveryStatus(self, deliveryStatus):
        self.__deliveryStatus = deliveryStatus
