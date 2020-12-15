class Candy:
    countID = 0
    def __init__(self, candyName, candyStockLevel, candyRetailPrice, candyCostPrice, candyCategory, candyImage, candySupplier, candyKeyInformation, candyIngredients, candyCountry):
        self.__class__.countID += 1     # User.countID += 1 (more tedious because if you were to change the class name, you have to keep changing this too)
        self.__candyID = self.__class__.countID
        self.__candyID = Candy.countID
        self.__candyCategory = candyCategory
        self.__candyRetailPrice = candyRetailPrice
        self.__candyCostPrice = candyCostPrice
        self.__candyStockLevel = 0
        self.__candyName = candyName
        self.__candyImage = candyImage
        self.__candySupplier = candySupplier
        self.__candyKeyInformation = candyKeyInformation
        self.__candyIngredients = candyIngredients
        self.__candyCountry = candyCountry

    def set_candyCategory(self, candyCategory):
        self.__candyCategory = candyCategory

    def set_candyRetailPrice(self, retail):
        self.__candyRetailPrice = retail

    def set_candyCostPrice(self, cost):
        self.__candyCostPrice = cost

    def set_candyStockLevel(self, stock):
        self.__candyStockLevel = stock

    def set_candyName(self, name):
        self.__candyName = name

    def set_candyImage(self, candyImage):
        self.__candyImage = candyImage

    def set_candySupplier(self, candySupplier):
        self.__candySupplier = candySupplier

    def set_candyKeyInformation(self, candyKeyInformation):
        self.__candyKeyInformation = candyKeyInformation

    def set_candyIngredients(self, candyIngredients):
        self.__candyIngredients = candyIngredients

    def set_candyCountry(self, candyCountry):
        self.__candyCountry = candyCountry





    def get_candyCategory(self):
        return self.__candyCategory

    def get_candyRetailPrice(self):
        return self.__candyRetailPrice

    def get_candyCostPrice(self):
        return self.__candyCostPrice

    def get_candyStockLevel(self):
        return self.__candyStockLevel

    def get_candyName(self):
        return self.__candyName

    def get_candyID(self):
        return self.__candyID

    def get_candyImage(self):
        return self.__candyImage

    def get_candySupplier(self):
        return self.__candySupplier

    def get_candyKeyInformation(self):
        return self.__candyKeyInformation

    def get_candyIngredients(self):
        return self.__candyIngredients

    def get_candyCountry(self):
        return self.__candyCountry
