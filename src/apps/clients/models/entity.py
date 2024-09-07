from dataclasses import dataclass


@dataclass
class ClientEntity:
    customer_ids: list[str]
    phone: str
