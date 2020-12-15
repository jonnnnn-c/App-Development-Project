import Candy

class CandyCart(Candy.Candy):
    def __init__(self, candyName, candyStockLevel, candyRetailPrice, candyCostPrice, candyCategory, candyImage, candySupplier, candyKeyInformation, candyIngredients, candyCountry):
        super().__init__(candyName, candyStockLevel, candyRetailPrice, candyCostPrice, candyCategory, candyImage, candySupplier, candyKeyInformation, candyIngredients, candyCountry)
        self.__quantity = 0
        self.__subtotal = 0

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_quantity(self):
        return self.__quantity

    def set_subtotal(self, subtotal):
        self.__subtotal = subtotal

    def get_subtotal(self):
        return self.__subtotal
