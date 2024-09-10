from types import UnionType

from typing import (
    Any,
    Type,
    TypeVar,
    Union,
    Sequence,
)

import loguru

TSchema = TypeVar("TSchema")


def dataclass_to_schema(schema: Type[TSchema], obj: Any) -> TSchema:
    """
    Функция конвертирует объекты dataclass в pydantic схему.
    Правила:
        1. В датаклассе должны быть все обязательные поля, которые есть
        в схеме и с таким же названием
        2. Поддерживает Union аннотации
        3. Работает с Optional[type]
        4. Работает с VarType:
            T = TypeVar("T")

            class ASchema(BaseModel):
                name: str

            class BSchema(BaseModel, Generic[T]):
                field_: T

            dataclass_to_schema(BSchema[ASchema], dataclass_obj)

        5. Поддерживает списки <list[Obj]> или <list[Obj1 | Obj2 | Obj3]> и вложенные объекты:
            class ASchema(BaseModel):
                name: str

            class BSchema(BaseModel):
                my_field: Optional[ASchema] = None

            class CSchema(BaseModel):
                optional_field: str | None = None
                list_field: list[BSchema] = Field(default_factory=list)

            dataclass_to_schema(CSchema, dataclass_obj)
    :param schema: pydantic схема в которую нужно конвертировать
    :param obj: объект dataclass
    :return: конвертированный объект pydantic схемы
    """
    attrs = {}
    if isinstance(schema, Sequence):
        for c in schema:
            try:
                return dataclass_to_schema(c, obj)
            except AttributeError:
                continue
        raise
    for field in schema.__fields__.keys():
        value = getattr(obj, field)
        sub_schema = schema.__fields__[field]
        field_type = _extract_field_type_schema(sub_schema.annotation)
        if (
            isinstance(value, Sequence)
            and len(value) > 0
            and hasattr(value[0], "__dataclass_fields__")
            and isinstance(field_type, tuple)
        ):
            attrs[field] = []
            for v in value:
                for ft in field_type:
                    try:
                        attrs[field].append(dataclass_to_schema(ft, v))
                    except AttributeError:
                        continue

        elif hasattr(value, "__dataclass_fields__"):
            attrs[field] = dataclass_to_schema(field_type, value)
        else:
            attrs[field] = value
    return schema(**attrs)


def _extract_field_type_schema(field_type: Any) -> Any:
    if isinstance(field_type, UnionType):
        return field_type.__args__
    elif hasattr(field_type, "__origin__"):
        if field_type.__origin__ is list:
            field_type = field_type.__args__
            if isinstance(field_type[0], UnionType):
                field_type = field_type[0].__args__
            return field_type
        if field_type.__origin__ is Union:
            field_type = field_type.__args__
    return field_type


if __name__ == "__main__":
    import dataclasses
    from annotated_types import Ge, Le
    from pydantic import BaseModel
    from typing import (
        Optional,
        Generic,
        Annotated,
    )

    def test_list_union():
        @dataclasses.dataclass
        class AObj:
            a: int

        @dataclasses.dataclass
        class BObj:
            b: str

        @dataclasses.dataclass
        class CObj:
            dep: list[AObj | BObj]

        class ASchema(BaseModel):
            a: int

        class BSchema(BaseModel):
            b: str

        class CSchema(BaseModel):
            dep: list[BSchema | ASchema]

        a_obj = AObj(1)
        b_obj = BObj("abc")
        c_obj = CObj(dep=[a_obj, b_obj])

        c_schema = dataclass_to_schema(CSchema, c_obj)
        assert isinstance(c_schema, CSchema)
        assert isinstance(c_schema.dep[0], ASchema)
        assert isinstance(
            c_schema.dep[1], BSchema
        ), f"{type(c_schema.dep[0])} != {type(BSchema)}"
        assert c_schema.dep[0].a == a_obj.a == 1
        assert c_schema.dep[1].b == b_obj.b == "abc"

    def test_list_enumeration_types():
        @dataclasses.dataclass
        class AObj:
            a: int

        @dataclasses.dataclass
        class BObj:
            b: str

        @dataclasses.dataclass
        class CObj:
            dep: AObj | BObj

        class ASchema(BaseModel):
            a: int

        class BSchema(BaseModel):
            b: str

        class CSchema(BaseModel):
            dep: ASchema | BSchema

        a_obj = AObj(1)
        b_obj = BObj("abc")
        c_obj = CObj(dep=a_obj)
        c_schema = dataclass_to_schema(CSchema, c_obj)
        assert isinstance(c_schema, CSchema)
        assert isinstance(c_schema.dep, ASchema)
        assert c_schema.dep.a == a_obj.a == 1
        c_obj = CObj(dep=b_obj)
        c_schema = dataclass_to_schema(CSchema, c_obj)
        assert isinstance(c_schema, CSchema)
        assert isinstance(c_schema.dep, BSchema)
        assert c_schema.dep.b == b_obj.b == "abc"

    def test_optional():
        @dataclasses.dataclass
        class AObj:
            a: Optional[int] = None

        @dataclasses.dataclass
        class BObj:
            b: Optional[AObj] = None

        class ASchema(BaseModel):
            a: Optional[int] = None

        class BSchema(BaseModel):
            b: Optional[ASchema] = None

        a_obj = AObj(1)
        b_obj = BObj(a_obj)
        b_schema = dataclass_to_schema(BSchema, b_obj)
        assert isinstance(b_schema.b, ASchema | None)
        assert isinstance(b_schema, BSchema)

    def test_generic():
        T = TypeVar("T")

        @dataclasses.dataclass
        class AObj:
            name: str | None

        @dataclasses.dataclass
        class BObj:
            field_: AObj

        class ASchema(BaseModel):
            name: str | None

        class BSchema(BaseModel, Generic[T]):
            field_: T

        a_obj = AObj(None)
        b_obj = BObj(field_=a_obj)
        b_schema = dataclass_to_schema(BSchema[ASchema], b_obj)
        assert isinstance(b_schema.field_, ASchema)
        assert isinstance(b_schema, BSchema)
        assert b_schema.field_.name == a_obj.name is None

    def test_any_type():
        @dataclasses.dataclass
        class AObj:
            a: Any

        class ASchema(BaseModel):
            a: Any

        a_obj = AObj((1,))
        a_schema = dataclass_to_schema(ASchema, a_obj)
        assert isinstance(a_schema, ASchema)
        assert a_obj.a == a_schema.a == (1,)
        a_obj = AObj(None)
        a_schema = dataclass_to_schema(ASchema, a_obj)
        assert isinstance(a_schema, ASchema)
        assert a_obj.a == a_schema.a is None

    def test_annotated_type():
        @dataclasses.dataclass
        class AObj:
            a: Annotated[int, Ge(0), Le(10)] | None = dataclasses.field(
                default=0
            )

        class ASchema(BaseModel):
            a: Annotated[int, Ge(0), Le(10)]

        a_obj = AObj(5)
        a_schema = dataclass_to_schema(ASchema, a_obj)
        assert isinstance(a_schema, ASchema)
        assert a_schema.a == a_obj.a == 5

    def test_list():
        @dataclasses.dataclass
        class AObj:
            a: list[int]

        @dataclasses.dataclass
        class BObj:
            b: list[AObj]

        class ASchema(BaseModel):
            a: list[int]

        class BSchema(BaseModel):
            b: list[ASchema]

        a_obj1 = AObj([0, 1, 2])
        a_obj2 = AObj([3, 4, 5])
        b_obj = BObj([a_obj1, a_obj2])
        b_schema = dataclass_to_schema(BSchema, b_obj)
        assert isinstance(b_schema, BSchema)
        assert isinstance(b_schema.b[0], ASchema)
        assert isinstance(b_schema.b[1], ASchema)

    test_list_union()
    test_list_enumeration_types()
    test_optional()
    test_generic()
    test_any_type()
    test_annotated_type()
    test_list()
