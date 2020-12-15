class CustomerDelivery:
    def __init__(self, orderDate, deliveryDate, total, paymentType, status):
        candyPurchased = {}
        self.__orderDate = orderDate
        self.__deliveryDate = deliveryDate
        self.__total = total
        self.__paymentType = paymentType
        self.__status = status

    def set_orderDate(self, orderDate):
        self.__orderDate = orderDate

    def set_deliveryDate(self, deliveryDate):
        self.__deliveryDate = deliveryDate

    def set_total(self, total):
        self.__total = total

    def set_paymentType(self, paymentType):
        self.__paymentType = paymentType

    def set_status(self, status):
        self.__status = status

    def get_orderDate(self):
        return self.__orderDate

    def get_deliveryDate(self):
        return self.__deliveryDate

    def get_total(self):
        return self.__total

    def get_paymentType(self):
        return self.__paymentType

    def get_status(self):
        return self.__status
