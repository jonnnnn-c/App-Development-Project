class CheckoutInformation:
    count = 0

    def __init__(self, firstName, lastName, phone, email, address, postalCode, shippingMethod, creditCardType, creditCardNumber, expiryDate, cardVerificationNumber, deliveryDate, deliveryStatus):
        self.__class__.count += 1
        self.__checkoutID = self.__class__.count
        self.__firstName = firstName
        self.__lastName = lastName
        self.__phone = phone
        self.__email = email
        self.__address = address
        self.__postalCode = postalCode
        self.__shippingMethod = shippingMethod
        self.__creditCardType = creditCardType
        self.__creditCardNumber = creditCardNumber
        self.__expiryDate = expiryDate
        self.__cardVerificationNumber = cardVerificationNumber
        self.__deliveryDate = deliveryDate
        self.__deliveryStatus = deliveryStatus
        self.__total = 0

    def get_checkoutID(self):
        return self.__checkoutID

    def get_firstName(self):
        return self.__firstName

    def get_lastName(self):
        return self.__lastName

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_address(self):
        return self.__address

    def get_postalCode(self):
        return self.__postalCode

    def get_shippingMethod(self):
        return self.__shippingMethod

    def get_creditCardType(self):
        return self.__creditCardType

    def get_creditCardNumber(self):
        return self.__creditCardNumber

    def get_expiryDate(self):
        return self.__expiryDate

    def get_cardVerificationNumber(self):
        return self.__cardVerificationNumber

    def get_deliveryDate(self):
        return self.__deliveryDate

    def get_total(self):
        return self.__total

    def get_deliveryStatus(self):
        return self.__deliveryStatus


    def set_checkoutID(self, checkoutID):
        self.__checkoutID = checkoutID

    def set_firstName(self, firstName):
        self.__firstName = firstName

    def set_lastName(self, lastName):
        self.__lastName = lastName

    def set_phone(self, phone):
        self.__phone = phone

    def set_email(self, email):
        self.__email = email

    def set_address(self, address):
        self.__address = address

    def set_postalCode(self, postalCode):
        self.__postalCode = postalCode

    def set_shippingMethod(self, shippingMethod):
        self.__shippingMethod = shippingMethod

    def set_creditCardType(self, creditCardType):
        self.__creditCardType = creditCardType

    def set_creditCardNumber(self, creditCardNumber):
        self.__creditCardNumber = creditCardNumber

    def set_expiryDate(self, expiryDate):
        self.__expiryDate = expiryDate

    def set_cardVerificationNumber(self, cardVerificationNumber):
        self.__cardVerificationNumber = cardVerificationNumber

    def set_deliveryDate(self, deliveryDate):
        self.__deliveryDate = deliveryDate

    def set_total(self, total):
        self.__total = total

    def set_deliveryStatus(self, deliveryStatus):
        self.__deliveryStatus = deliveryStatus
