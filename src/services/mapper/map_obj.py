from types import UnionType
from typing import (
    Any,
    get_type_hints,
    Type,
    TypeVar,
    Union,
)

from django.db import models
from django.db.models import (
    ManyToManyRel,
    ManyToOneRel,
    Model,
    OneToOneRel,
)


TSchema = TypeVar("TSchema")


class Mapper:
    @classmethod
    def model_to_dataclass(cls, instance: Model, dataclass_type: Any) -> Any:
        """
        Конвертация django orm моделей в объекты dataclass.
        """
        attrs = {}
        fields_ = get_type_hints(dataclass_type)

        for field_name, field_type in fields_.items():
            try:
                model_field = instance._meta.get_field(field_name)
            except models.ObjectDoesNotExist:
                continue

            field_type = cls._extract_field_type_schema(field_type)

            if isinstance(model_field, OneToOneRel):
                if not hasattr(instance, field_name):
                    attrs[field_name] = None
                else:
                    related_instance = getattr(instance, field_name)
                    attrs[field_name] = cls.model_to_dataclass(
                        related_instance, field_type
                    )

            elif isinstance(model_field, (ManyToOneRel, ManyToManyRel)):
                related_manager = getattr(instance, field_name)
                related_instances = related_manager.all()
                attrs[field_name] = [
                    cls.model_to_dataclass(instance, field_type)
                    for instance in related_instances
                ]
            else:
                attrs[field_name] = getattr(instance, field_name)

        return dataclass_type(**attrs)

    @classmethod
    def dataclass_to_schema(cls, schema: Type[TSchema], obj: Any) -> TSchema:
        """
        Функция конвертирует объекты dataclass в pydantic схему.
        Правила:
            1. В датаклассе должны быть все обязательные поля, которые есть
            в схеме и с таким же названием
            2. Не поддерживает Union аннотации
            (за исключением <type | None = None>)
            3. Работает с Optional[type]
            4. Работает с VarType:
                T = TypeVar("T")

                class ASchema(BaseModel):
                    name: str

                class BSchema(BaseModel, Generic[T]):
                    field_: T

                Mapper.dataclass_to_schema(BSchema[ASchema], dataclass_obj)

            5. Поддерживает списки <list[type]> (все объекты должны быть
            одного типа) и вложенные объекты:
                class ASchema(BaseModel):
                    name: str

                class BSchema(BaseModel):
                    my_field: Optional[ASchema] = None

                class CSchema(BaseModel):
                    optional_field: str | None = None
                    list_field: list[BSchema] = Field(default_factory=list)

                Mapper.dataclass_to_schema(CSchema, dataclass_obj)
        """
        attrs = {}
        for field in schema.__fields__.keys():
            value = getattr(obj, field)
            sub_schema = schema.__fields__[field]
            field_type = cls._extract_field_type_schema(sub_schema.annotation)
            if (
                isinstance(value, list)
                and len(value) > 0
                and hasattr(value[0], "__dataclass_fields__")
            ):
                attrs[field] = [
                    cls.dataclass_to_schema(field_type, item) for item in value
                ]
            elif hasattr(value, "__dataclass_fields__"):
                attrs[field] = cls.dataclass_to_schema(field_type, value)
            else:
                attrs[field] = value
        return schema(**attrs)

    @staticmethod
    def _extract_field_type_schema(field_type: Any) -> Any:
        if isinstance(field_type, list):
            field_type = field_type[0]
        if isinstance(field_type, UnionType):
            return next(t for t in field_type.__args__ if t is not type(None))
        elif hasattr(field_type, "__origin__"):
            if field_type.__origin__ is list:
                return field_type.__args__[0]
            if field_type.__origin__ is Union:
                return next(
                    t for t in field_type.__args__ if t is not type(None)
                )
        return field_type
