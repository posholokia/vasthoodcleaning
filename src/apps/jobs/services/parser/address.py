class AddressString:
    """
    Объект адреса пользователя, используется в строителе для корректного
    преобразования адреса в строку, чтобы пустые поля не выглядели
    в виде None или лишних пробелов.
    """

    def __init__(self, address_part: str = ""):
        self.address_part = address_part

    def __add__(self, other):
        if other is None or other == "":
            return self

        if not isinstance(other, str | type(self)):
            raise Exception(
                "Соединить AddressString можно только с "
                "объектами AddressString, строкой или None"
            )

        if self.address_part == "":
            self.address_part = f"{other}"
        else:
            self.address_part = f"{self.address_part} {other}"
        return self

    def __repr__(self):
        return self.address_part

    def __str__(self):
        return self.address_part


class AddressParser:
    def __init__(self):
        self.address = AddressString()

    def build(self, address_json: dict[str, str | None]) -> str:
        """Собирает из json адрес кастомера в строку."""
        self._add(address_json.get("street"))
        self._add(address_json.get("street_line_2"))
        self._add(address_json.get("city"))
        self._add(address_json.get("state"))
        self._add(address_json.get("zip"))
        return str(self.address)

    def _add(self, address_part: str) -> None:
        """Добавление строки к адресу."""
        self.address += address_part


if __name__ == "__main__":
    a = {
        "id": "adr_00950059aad0470a970995cd104f3627",
        "type": "service",
        "street": "4932 Acacia St",
        "street_line_2": "",
        "city": "San Gabriel",
        "state": "CA",
        "zip": "91776",
        "country": "US",
    }
    b = {
        "id": "adr_00950059aad0470a970995cd104f3627",
        "type": "service",
        "street": "4932 Acacia St",
        "street_line_2": None,
        "city": "San Gabriel",
        "state": "CA",
        "zip": "91776",
        "country": "US",
    }

    builder = AddressParser()
    a1 = builder.build(a)
    assert "4932 Acacia St San Gabriel CA 91776" == a1
    builder = AddressParser()
    b1 = builder.build(b)
    assert "4932 Acacia St San Gabriel CA 91776" == b1
