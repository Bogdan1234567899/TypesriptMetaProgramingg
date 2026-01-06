from typing import Union

Number = Union[int, float]


class Product:
    def __init__(self, price: Number, quantity: Number):
        # 1) типи
        if not isinstance(price, (int, float)):
            raise TypeError("price має бути числом (int або float)")
        if not isinstance(quantity, (int, float)):
            raise TypeError("quantity має бути числом (int або float)")

        # 2) не менше 0
        if price < 0:
            raise ValueError("price має бути >= 0")
        if quantity < 0:
            raise ValueError("quantity має бути >= 0")

        self.price = price
        self.quantity = quantity


if __name__ == "__main__":
    p1 = Product(10.5, 3)
    print("OK:", p1.price, p1.quantity)

    # Приклади помилок
    try:
        Product(-1, 2)
    except Exception as e:
        print("Error:", e)

    try:
        Product("100", 2)  # type: ignore
    except Exception as e:
        print("Error:", e)
