class Pompe:
    def __init__(self, price: float, libelle: str) -> None:
        self._price = price
        self._libelle = libelle

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, price) -> None:
        self._price = price

    @property
    def libelle(self) -> str:
        return self._libelle

    @libelle.setter
    def libelle(self, libelle: str) -> None:
        self._libelle = libelle

    def __str__(self) -> str:
        return f"{self._libelle}: {self._price}€"