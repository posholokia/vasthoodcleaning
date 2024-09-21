from enum import Enum
from typing import Any

from apps.jobs.models import (
    DetailMaterialEntity,
    DiscountEntity,
    DiscountType,
    JobDetailEntity,
    MaterialsEntity,
)
from apps.jobs.models.entity import (
    JobPartEntity,
    MultipleSelectEntity,
    NumericalRangeEntity,
    QuantitySelectEntity,
    SingleSelectEntity,
    T,
)
from loguru import logger


class JobLineType(Enum):
    job: str = "labor"
    materials: str = "materials"
    percent_discount: str = "percent discount"
    fixed_discount: str = "fixed discount"


class JobInlinesType(Enum):
    multiple: str = "multiple_select"
    range: str = "numerical_range"
    quantity: str = "quantity_select"
    single: str = "single_select"


def parse_job_detail(job_lines_data: dict[str, Any]) -> JobDetailEntity:
    """
    Парсер детальной информации о заказанной работе.

    :param job_lines_data:  Json со списком всех лайнов заказа.
    :return:                Детальная информация о заказе.
    """
    parts: list[JobPartEntity] = []  # список услуг в рамках одной работы
    materials: list[DetailMaterialEntity] = []  # список выбранных материалов
    # фиксированная и процентная скидки взаимозамещают друг друга в CRM
    fixed_discounts: list[DiscountEntity] = []  # список фиксированных скидок
    discount: DiscountEntity | None = None  # процентная скидка

    for line in job_lines_data["data"]:
        try:
            kind = JobLineType(line["kind"])
        except ValueError:
            logger.warning("Неизвестный тип line {}", line["kind"])
            continue

        if kind is JobLineType.job:
            parts.append(_parse_job(line))
        elif kind is JobLineType.materials:
            materials.append(_parse_materials(line))
        elif kind is JobLineType.fixed_discount:
            fixed_discounts.append(_parse_discount(line))
        elif kind is JobLineType.percent_discount:
            discount = _parse_discount(line)

    # если скидки фиксированные, пересобираем их в одну
    if fixed_discounts:
        discount = DiscountEntity(
            value=sum([discount.value for discount in fixed_discounts]),
            kind=DiscountType.fixed,
        )
    material_entity = MaterialsEntity(
        total_cost=sum([material.cost for material in materials]),
        detail=materials,
    )
    cost_before_discount = (
        sum([part.cost for part in parts]) + material_entity.total_cost
    )
    return JobDetailEntity(
        parts=parts,
        cost_before_discount=cost_before_discount,
        materials=material_entity if material_entity else None,
        discount=discount,
    )


def _parse_discount(discount: dict) -> DiscountEntity:
    """
    Парсит данные о скидке.

    :param discount:    Json с данными о скидке.
    :return:            Скидка.
    """
    return DiscountEntity(
        value=discount["amount"], kind=DiscountType(discount["kind"])
    )


def _parse_materials(material: dict) -> DetailMaterialEntity:
    """
    Парсит данные о материалах.

    :param material:    Json с данными о материале.
    :return:            Материал.
    """
    return DetailMaterialEntity(
        name=material["name"],
        quantity=material["quantity"],
        cost=material["amount"],
    )


def _parse_job(job_data: dict[str, Any]) -> JobPartEntity:
    """
    Парсит данные о работе в рамках заказа.

    :param job_data:    Json с данными о работе.
    :return:            Работа.
    """
    name = job_data.get("name")
    cost = job_data.get("amount")
    inlines = _parse_job_inlines(
        job_data["pricing_form"]["data"]["form"]["fields"]
    )
    return JobPartEntity(name=name, cost=cost, inlines=inlines)


def _parse_job_inlines(fields: list[dict[str, Any]]) -> T:
    """
    Парсинг выбранных параметров в работе.

    :param fields:  Json c выбранными параметрами.
    :return:        Параметр (услуга) работы.
    """
    inlines: T = []
    for field_ in fields:
        try:
            kind = JobInlinesType(field_["kind"])
        except ValueError:
            logger.warning("Неизвестный тип inline {}", field_["kind"])
            continue

        if kind is JobInlinesType.multiple:
            inlines.append(_parse_multiple_select(field_))
        elif kind is JobInlinesType.quantity:
            inlines.append(_parse_quantity_select(field_))
        elif kind is JobInlinesType.single:
            inlines.append(_parse_single_select(field_))
        elif kind is JobInlinesType.range:
            inlines.append(_parse_range_select(field_))

    inline_filter = filter(lambda x: x is not None, inlines)
    return [inline for inline in inline_filter]


def _parse_multiple_select(inline: dict) -> MultipleSelectEntity | None:
    """
    Парсинг параметра множественного выбора.

    :param inline:  Json c конкретным параметром множественного выбора.
    :return:        Множественный параметр.
    """
    selected: list[int] = inline["selected"]
    if not selected:
        return

    name: str = inline["name"]
    choice_filter = filter(lambda x: x["id"] in selected, inline["options"])

    return MultipleSelectEntity(
        name=name, choices=[choice["name"] for choice in choice_filter]
    )


def _parse_quantity_select(inline: dict) -> QuantitySelectEntity | None:
    """
    Парсинг параметра количественного выбора.

    :param inline:  Json c конкретным параметром количественного выбора.
    :return:        Количественный параметр.
    """
    value = inline["value"]
    if not value:
        return
    return QuantitySelectEntity(name=inline["name"], value=value)


def _parse_single_select(inline: dict) -> SingleSelectEntity | None:
    """
    Парсинг параметра единственного выбора.

    :param inline:  Json c конкретным параметром единственного выбора.
    :return:        Единственный параметр.
    """
    selected: list[int] = inline["selected"]
    if not selected:
        return

    choice = next(
        (
            item["name"]
            for item in inline["options"]
            if item["id"] == selected[0]
        ),
        None,
    )
    return SingleSelectEntity(name=inline["name"], choice=choice)


def _parse_range_select(inline: dict) -> NumericalRangeEntity | None:
    """
    Парсинг параметра выбора выпадающего списка.

    :param inline:  Json c конкретным параметром из выпадающего списка.
    :return:        Выбранный параметр.
    """
    selected: list[int] = inline["selected"]
    if not selected:
        return

    choice = next(
        (
            item["name"]
            for item in inline["options"]
            if item["id"] == selected[0]
        ),
        None,
    )
    return NumericalRangeEntity(name=inline["name"], choice=choice)


if __name__ == "__main__":
    datajob = {
        "object": "list",
        "data": [
            {
                "object": "line_item",
                "id": "rli_ced490a1f7874c1894567ed1d7664556",
                "name": "Airbnb Cleaning Service",
                "description": "What is included::\r\nBedroom, Living Room & Common Areas\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Bathroom Cleaning\r\n•  Wash and sanitize the toilet, shower, tub and sink\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Kitchen Cleaning\r\n•  Dust accessible surfaces\r\n•  Wipe down exterior of stove, oven and fridge\r\n\r\n\n1 bedroom: 2 bathrooms\n2 bedrooms: none\n3 bedrooms : none\n4 bedrooms: none\n5 bedrooms: none\nSquare feet: none\nExtra: Pet Friendly, Eco Friendly, Green\nInside Oven Cleaning - $40: 0\nInside Fridge Cleaning - $40: 0\nBalcony - $35: 0\nPatio - $75: 9\nLoading /Unloading Dishwasher Machine - $10: 0\nLoading/Unloading Washer-Dryer 1 cycle - $10 : 0\nMaking Beds (each) - $10: 0\nWindow /Track Cleaning (per regular windows) - $10: 0\nShutters (per 1 Shutter section) - $5: 0\nSliding Door Window Cleaning (per slider) + tracks - $5: 0",
                "unit_price": 83500,
                "unit_cost": 0,
                "unit_of_measure": None,
                "quantity": 1.0,
                "kind": "labor",
                "taxable": False,
                "amount": 83500,
                "order_index": 1,
                "service_item_id": None,
                "service_item_type": None,
                "pricing_form": {
                    "object": "request_line_item_pricing_form",
                    "data": {
                        "object": "request_line_item_pricing_form",
                        "industry_uuid": None,
                        "pricebook_price_form_uuid": "pbpf_53825d6d712243e28002d0fd4a5d66b1",
                        "form": {
                            "id": "pbpf_53825d6d712243e28002d0fd4a5d66b1",
                            "name": "Airbnb Cleaning Service",
                            "description": "What is included::\r\nBedroom, Living Room & Common Areas\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Bathroom Cleaning\r\n•  Wash and sanitize the toilet, shower, tub and sink\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Kitchen Cleaning\r\n•  Dust accessible surfaces\r\n•  Wipe down exterior of stove, oven and fridge\r\n\r\n",
                            "fields": [
                                {
                                    "id": 209716,
                                    "name": "1 bedroom",
                                    "kind": "multiple_select",
                                    "amount": 16000,
                                    "options": [
                                        {
                                            "id": 353280,
                                            "name": "Studio",
                                            "price": 14900,
                                        },
                                        {
                                            "id": 353284,
                                            "name": "1 bathroom",
                                            "price": 14900,
                                        },
                                        {
                                            "id": 365671,
                                            "name": "2 bathrooms",
                                            "price": 16000,
                                        },
                                    ],
                                    "selected": [365671],
                                },
                                {
                                    "id": 214438,
                                    "name": "2 bedrooms",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 361321,
                                            "name": "1 bathroom",
                                            "price": 16000,
                                        },
                                        {
                                            "id": 361323,
                                            "name": "2 bathrooms",
                                            "price": 18500,
                                        },
                                        {
                                            "id": 361324,
                                            "name": "3 bathrooms",
                                            "price": 22500,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 214439,
                                    "name": "3 bedrooms ",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 361325,
                                            "name": "1 bathroom",
                                            "price": 22500,
                                        },
                                        {
                                            "id": 361327,
                                            "name": "2 bathrooms",
                                            "price": 23500,
                                        },
                                        {
                                            "id": 361328,
                                            "name": "3 bathrooms",
                                            "price": 24500,
                                        },
                                        {
                                            "id": 361329,
                                            "name": "4 bathrooms",
                                            "price": 27000,
                                        },
                                        {
                                            "id": 361330,
                                            "name": "5 bathrooms",
                                            "price": 29500,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 214440,
                                    "name": "4 bedrooms",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 361331,
                                            "name": "1 bathroom",
                                            "price": 24500,
                                        },
                                        {
                                            "id": 361333,
                                            "name": "2 bathrooms",
                                            "price": 28000,
                                        },
                                        {
                                            "id": 361334,
                                            "name": "3 bathrooms",
                                            "price": 30000,
                                        },
                                        {
                                            "id": 361335,
                                            "name": "4 bathrooms",
                                            "price": 33000,
                                        },
                                        {
                                            "id": 361336,
                                            "name": "5 bathrooms",
                                            "price": 34000,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 214441,
                                    "name": "5 bedrooms",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 361337,
                                            "name": "1 bathroom",
                                            "price": 37000,
                                        },
                                        {
                                            "id": 361339,
                                            "name": "2 bathrooms",
                                            "price": 39000,
                                        },
                                        {
                                            "id": 361340,
                                            "name": "3 bathrooms",
                                            "price": 42000,
                                        },
                                        {
                                            "id": 361341,
                                            "name": "4 bathrooms",
                                            "price": 46000,
                                        },
                                        {
                                            "id": 361342,
                                            "name": "5 bathrooms",
                                            "price": 47000,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 209718,
                                    "name": "Square feet",
                                    "kind": "numerical_range",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 353300,
                                            "name": "501 - 1000",
                                            "price": 0,
                                            "upper_bound": 1000,
                                            "lower_bound": 501,
                                        },
                                        {
                                            "id": 353301,
                                            "name": "1001 - 1500",
                                            "price": 0,
                                            "upper_bound": 1500,
                                            "lower_bound": 1001,
                                        },
                                        {
                                            "id": 353302,
                                            "name": "1501 - 2000",
                                            "price": 0,
                                            "upper_bound": 2000,
                                            "lower_bound": 1501,
                                        },
                                        {
                                            "id": 353303,
                                            "name": "2001 - 2500",
                                            "price": 0,
                                            "upper_bound": 2500,
                                            "lower_bound": 2001,
                                        },
                                        {
                                            "id": 353304,
                                            "name": "2501 - 3000",
                                            "price": 0,
                                            "upper_bound": 3000,
                                            "lower_bound": 2501,
                                        },
                                        {
                                            "id": 353305,
                                            "name": "3001 - 3500",
                                            "price": 0,
                                            "upper_bound": 3500,
                                            "lower_bound": 3001,
                                        },
                                        {
                                            "id": 353306,
                                            "name": "3501 - 4000",
                                            "price": 0,
                                            "upper_bound": 4000,
                                            "lower_bound": 3501,
                                        },
                                        {
                                            "id": 353307,
                                            "name": "4001 - 4500",
                                            "price": 0,
                                            "upper_bound": 4500,
                                            "lower_bound": 4001,
                                        },
                                        {
                                            "id": 353308,
                                            "name": "4501 - 5000",
                                            "price": 0,
                                            "upper_bound": 5000,
                                            "lower_bound": 4501,
                                        },
                                        {
                                            "id": 353309,
                                            "name": "5001 - 2147483647",
                                            "price": 0,
                                            "upper_bound": 2147483647,
                                            "lower_bound": 5001,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 216681,
                                    "name": "Extra",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 365635,
                                            "name": "Pet Friendly",
                                            "price": 0,
                                        },
                                        {
                                            "id": 365636,
                                            "name": "Eco Friendly",
                                            "price": 0,
                                        },
                                        {
                                            "id": 365637,
                                            "name": "Green",
                                            "price": 0,
                                        },
                                        {
                                            "id": 365638,
                                            "name": "Other",
                                            "price": 0,
                                        },
                                    ],
                                    "selected": [365635, 365636, 365637],
                                },
                                {
                                    "id": 209723,
                                    "name": "Inside Oven Cleaning - $40",
                                    "kind": "quantity_select",
                                    "price": 4000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209721,
                                    "name": "Inside Fridge Cleaning - $40",
                                    "kind": "quantity_select",
                                    "price": 4000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209722,
                                    "name": "Balcony - $35",
                                    "kind": "quantity_select",
                                    "price": 3500,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209720,
                                    "name": "Patio - $75",
                                    "kind": "quantity_select",
                                    "price": 7500,
                                    "value": 9,
                                    "amount": 67500,
                                },
                                {
                                    "id": 209728,
                                    "name": "Loading /Unloading Dishwasher Machine - $10",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209729,
                                    "name": "Loading/Unloading Washer-Dryer 1 cycle - $10 ",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209727,
                                    "name": "Making Beds (each) - $10",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209730,
                                    "name": "Window /Track Cleaning (per regular windows) - $10",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209725,
                                    "name": "Shutters (per 1 Shutter section) - $5",
                                    "kind": "quantity_select",
                                    "price": 500,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209731,
                                    "name": "Sliding Door Window Cleaning (per slider) + tracks - $5",
                                    "kind": "quantity_select",
                                    "price": 500,
                                    "value": 0,
                                    "amount": 0,
                                },
                            ],
                        },
                        "total_price": 83500,
                        "bedroom_count": None,
                        "bathroom_count": None,
                        "story_count": None,
                        "room_count": None,
                        "window_count": None,
                        "square_footage_lower_bound": None,
                        "square_footage_upper_bound": None,
                        "total_bedroom_price": None,
                        "total_bathroom_price": None,
                        "total_story_price": None,
                        "total_window_price": None,
                        "total_room_price": None,
                        "total_square_footage_price": None,
                    },
                },
                "url": "/jobs/job_5af0cdda35f54fff9b006400a63fbf5a/line_items/rli_ced490a1f7874c1894567ed1d7664556",
            },
            {
                "object": "line_item",
                "id": "rli_e227cd5fcc154e1b9dbde96e332c28a7",
                "name": "Apartments Cleaning",
                "description": "What is included::\r\nBedroom, Living Room & Common Areas\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Bathroom Cleaning\r\n•  Wash and sanitize the toilet, shower, tub and sink\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Kitchen Cleaning\r\n•  Dust accessible surfaces\r\n•  Wipe down exterior of stove, oven and fridge\r\n\r\n\n1 bedroom: 1 bathroom\n2 bedrooms: 2 bathrooms\n3 bedrooms : none\n4 bedrooms : none\n5 bedrooms: none\nSquare feet: none\nExtra: none\nInside Oven Cleaning - $40: 0\nInside Fridge Cleaning - $40: 0\nBalcony - $35: 0\nPatio - $75: 0\nLoading /Unloading Dishwasher Machine - $10: 0\nLoading/Unloading Washer-Dryer 1 cycle - $10 : 0\nMaking Beds (each) - $10: 0\nWindow /Track Cleaning (per regular windows) - $10: 0\nShutters (per 1 Shutter section) - $5: 0\nSliding Door Window Cleaning (per slider) + tracks - $5: 0",
                "unit_price": 33400,
                "unit_cost": 0,
                "unit_of_measure": None,
                "quantity": 1.0,
                "kind": "labor",
                "taxable": False,
                "amount": 33400,
                "order_index": 2,
                "service_item_id": None,
                "service_item_type": None,
                "pricing_form": {
                    "object": "request_line_item_pricing_form",
                    "data": {
                        "object": "request_line_item_pricing_form",
                        "industry_uuid": None,
                        "pricebook_price_form_uuid": "pbpf_678170a6b77a4c7eac7db5429a17a670",
                        "form": {
                            "id": "pbpf_678170a6b77a4c7eac7db5429a17a670",
                            "name": "Apartments Cleaning",
                            "description": "What is included::\r\nBedroom, Living Room & Common Areas\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Bathroom Cleaning\r\n•  Wash and sanitize the toilet, shower, tub and sink\r\n•  Dust accessible surfaces\r\n•  Wipe down mirrors and glass fixtures\r\n•  Mop & vacuum floors\r\n•  Take out garbage\r\n•  Kitchen Cleaning\r\n•  Dust accessible surfaces\r\n•  Wipe down exterior of stove, oven and fridge\r\n\r\n",
                            "fields": [
                                {
                                    "id": 209755,
                                    "name": "1 bedroom",
                                    "kind": "multiple_select",
                                    "amount": 14900,
                                    "options": [
                                        {
                                            "id": 353339,
                                            "name": "Studio",
                                            "price": 14900,
                                        },
                                        {
                                            "id": 361260,
                                            "name": "1 bathroom",
                                            "price": 14900,
                                        },
                                        {
                                            "id": 361261,
                                            "name": "2 bathroom",
                                            "price": 16000,
                                        },
                                    ],
                                    "selected": [361260],
                                },
                                {
                                    "id": 214424,
                                    "name": "2 bedrooms",
                                    "kind": "multiple_select",
                                    "amount": 18500,
                                    "options": [
                                        {
                                            "id": 361262,
                                            "name": "1 bathroom",
                                            "price": 16000,
                                        },
                                        {
                                            "id": 361264,
                                            "name": "2 bathrooms",
                                            "price": 18500,
                                        },
                                        {
                                            "id": 361265,
                                            "name": "3 bathrooms",
                                            "price": 22500,
                                        },
                                    ],
                                    "selected": [361264],
                                },
                                {
                                    "id": 214425,
                                    "name": "3 bedrooms ",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 361266,
                                            "name": "1 bathroom",
                                            "price": 22500,
                                        },
                                        {
                                            "id": 361268,
                                            "name": "2 bathrooms",
                                            "price": 23500,
                                        },
                                        {
                                            "id": 361269,
                                            "name": "3 bathrooms",
                                            "price": 24500,
                                        },
                                        {
                                            "id": 361270,
                                            "name": "4 bathrooms",
                                            "price": 27000,
                                        },
                                        {
                                            "id": 361271,
                                            "name": "5 bathrooms",
                                            "price": 29500,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 209756,
                                    "name": "4 bedrooms ",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 353349,
                                            "name": "1 bathroom",
                                            "price": 24500,
                                        },
                                        {
                                            "id": 361296,
                                            "name": "2 bathrooms",
                                            "price": 28000,
                                        },
                                        {
                                            "id": 361297,
                                            "name": "3 bathrooms",
                                            "price": 30000,
                                        },
                                        {
                                            "id": 361298,
                                            "name": "4 bathrooms",
                                            "price": 33000,
                                        },
                                        {
                                            "id": 361299,
                                            "name": "5 bathrooms",
                                            "price": 34000,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 214426,
                                    "name": "5 bedrooms",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 361272,
                                            "name": "1 bathroom",
                                            "price": 37000,
                                        },
                                        {
                                            "id": 361274,
                                            "name": "2 bathrooms",
                                            "price": 39000,
                                        },
                                        {
                                            "id": 361275,
                                            "name": "3 bathrooms",
                                            "price": 42000,
                                        },
                                        {
                                            "id": 361276,
                                            "name": "4 bathrooms",
                                            "price": 46000,
                                        },
                                        {
                                            "id": 361277,
                                            "name": "5 bathrooms",
                                            "price": 47000,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 209757,
                                    "name": "Square feet",
                                    "kind": "numerical_range",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 353359,
                                            "name": "501 - 1000",
                                            "price": 0,
                                            "upper_bound": 1000,
                                            "lower_bound": 501,
                                        },
                                        {
                                            "id": 353360,
                                            "name": "1001 - 1500",
                                            "price": 0,
                                            "upper_bound": 1500,
                                            "lower_bound": 1001,
                                        },
                                        {
                                            "id": 353361,
                                            "name": "1501 - 2000",
                                            "price": 0,
                                            "upper_bound": 2000,
                                            "lower_bound": 1501,
                                        },
                                        {
                                            "id": 353362,
                                            "name": "2001 - 2500",
                                            "price": 0,
                                            "upper_bound": 2500,
                                            "lower_bound": 2001,
                                        },
                                        {
                                            "id": 353363,
                                            "name": "2501 - 3000",
                                            "price": 0,
                                            "upper_bound": 3000,
                                            "lower_bound": 2501,
                                        },
                                        {
                                            "id": 353364,
                                            "name": "3001 - 3500",
                                            "price": 0,
                                            "upper_bound": 3500,
                                            "lower_bound": 3001,
                                        },
                                        {
                                            "id": 353365,
                                            "name": "3501 - 4000",
                                            "price": 0,
                                            "upper_bound": 4000,
                                            "lower_bound": 3501,
                                        },
                                        {
                                            "id": 353366,
                                            "name": "4001 - 4500",
                                            "price": 0,
                                            "upper_bound": 4500,
                                            "lower_bound": 4001,
                                        },
                                        {
                                            "id": 353367,
                                            "name": "4501 - 5000",
                                            "price": 0,
                                            "upper_bound": 5000,
                                            "lower_bound": 4501,
                                        },
                                        {
                                            "id": 353368,
                                            "name": "5001 - 2147483647",
                                            "price": 0,
                                            "upper_bound": 2147483647,
                                            "lower_bound": 5001,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 216680,
                                    "name": "Extra",
                                    "kind": "multiple_select",
                                    "amount": 0,
                                    "options": [
                                        {
                                            "id": 365632,
                                            "name": "Pet Friendly",
                                            "price": 0,
                                        },
                                        {
                                            "id": 365633,
                                            "name": "Eco Friendly",
                                            "price": 0,
                                        },
                                        {
                                            "id": 365634,
                                            "name": "Green",
                                            "price": 0,
                                        },
                                        {
                                            "id": 365670,
                                            "name": "Other",
                                            "price": 0,
                                        },
                                    ],
                                    "selected": [],
                                },
                                {
                                    "id": 209762,
                                    "name": "Inside Oven Cleaning - $40",
                                    "kind": "quantity_select",
                                    "price": 4000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209760,
                                    "name": "Inside Fridge Cleaning - $40",
                                    "kind": "quantity_select",
                                    "price": 4000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209761,
                                    "name": "Balcony - $35",
                                    "kind": "quantity_select",
                                    "price": 3500,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209759,
                                    "name": "Patio - $75",
                                    "kind": "quantity_select",
                                    "price": 7500,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209767,
                                    "name": "Loading /Unloading Dishwasher Machine - $10",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209768,
                                    "name": "Loading/Unloading Washer-Dryer 1 cycle - $10 ",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209766,
                                    "name": "Making Beds (each) - $10",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209769,
                                    "name": "Window /Track Cleaning (per regular windows) - $10",
                                    "kind": "quantity_select",
                                    "price": 1000,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209764,
                                    "name": "Shutters (per 1 Shutter section) - $5",
                                    "kind": "quantity_select",
                                    "price": 500,
                                    "value": 0,
                                    "amount": 0,
                                },
                                {
                                    "id": 209770,
                                    "name": "Sliding Door Window Cleaning (per slider) + tracks - $5",
                                    "kind": "quantity_select",
                                    "price": 500,
                                    "value": 0,
                                    "amount": 0,
                                },
                            ],
                        },
                        "total_price": 33400,
                        "bedroom_count": None,
                        "bathroom_count": None,
                        "story_count": None,
                        "room_count": None,
                        "window_count": None,
                        "square_footage_lower_bound": None,
                        "square_footage_upper_bound": None,
                        "total_bedroom_price": None,
                        "total_bathroom_price": None,
                        "total_story_price": None,
                        "total_window_price": None,
                        "total_room_price": None,
                        "total_square_footage_price": None,
                    },
                },
                "url": "/jobs/job_5af0cdda35f54fff9b006400a63fbf5a/line_items/rli_e227cd5fcc154e1b9dbde96e332c28a7",
            },
            {
                "object": "line_item",
                "id": "rli_2aa134c99949480a81c5062afbaa70d7",
                "name": "Chemical - Windex",
                "description": "Test",
                "unit_price": 1200,
                "unit_cost": 500,
                "unit_of_measure": None,
                "quantity": 1.0,
                "kind": "materials",
                "taxable": False,
                "amount": 1200,
                "order_index": 3,
                "service_item_id": "pbmat_2107d82c2df64ebe9a3012d0239828d1",
                "service_item_type": "Pricebook::Material",
                "url": "/jobs/job_5af0cdda35f54fff9b006400a63fbf5a/line_items/rli_2aa134c99949480a81c5062afbaa70d7",
            },
            {
                "object": "line_item",
                "id": "rli_b0c8426db2e4403ca76e8adbf67e7af7",
                "name": "test material 2",
                "description": "",
                "unit_price": 200,
                "unit_cost": 0,
                "unit_of_measure": None,
                "quantity": 1.0,
                "kind": "materials",
                "taxable": False,
                "amount": 200,
                "order_index": 4,
                "service_item_id": None,
                "service_item_type": None,
                "url": "/jobs/job_5af0cdda35f54fff9b006400a63fbf5a/line_items/rli_b0c8426db2e4403ca76e8adbf67e7af7",
            },
            {
                "object": "line_item",
                "id": "rli_a1056437e0e54c289c14ff22a691c564",
                "name": "",
                "description": "",
                "unit_price": 5000,
                "unit_cost": 0,
                "unit_of_measure": None,
                "quantity": 1.0,
                "kind": "percent discount",
                "taxable": False,
                "amount": 5000,
                "order_index": None,
                "service_item_id": None,
                "service_item_type": None,
                "url": "/jobs/job_5af0cdda35f54fff9b006400a63fbf5a/line_items/rli_a1056437e0e54c289c14ff22a691c564",
            },
        ],
        "url": "/jobs/job_5af0cdda35f54fff9b006400a63fbf5a/line_items",
    }

    r = parse_job_detail(datajob)
    print(r)
