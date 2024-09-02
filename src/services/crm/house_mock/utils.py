from services.crm.house_mock.dto import CustomerDTO
import math
import asyncio
from typing import (
    Callable,
    ParamSpec,
    TypeVar, Any,
)


F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")


def get_from_all_pages(
    func: Callable[F_Spec, F_Return],
) -> Callable[F_Spec, F_Return]:
    """
    Если на странице не все данные, декоратор
    "дозапросит" их с остальных страниц
    """
    async def wrapper(
        self: Any,
        path: str,
        query: str,
        page: int = 1,
        page_size: int = 3,  # set max 200
    ) -> F_Return:
        res = await func(self, path, query, page, page_size)
        total_pages, received_result = res

        if total_pages > 1:
            # с какой записи запросить следующую выборку
            next_page = page + 1 if page == 1 else 1
            # далее формируем список задач для их
            # одновременного выполнения, чтобы сократить время
            # выполнения, если будет много страниц
            tasks = []
            for _ in range(total_pages):
                if next_page == page:
                    continue
                task = func(self, path, query, next_page, page_size)
                tasks.append(task)
                next_page += 1
            res = await asyncio.gather(*tasks)  # ожидаем ответ от всех задач
            # и расширяем ответ начальной функции новыми номерами
            for item in res:
                _, result = item
                received_result.extend(result)
        return total_pages, received_result

    return wrapper


def convert_data_to_dto(data: dict) -> CustomerDTO:
    return CustomerDTO(
        id=data["id"],
        phone=data["mobile_number"],
    )
