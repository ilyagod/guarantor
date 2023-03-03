from abc import ABC
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

import tortoise

all = ["BaseDAO"]

DAOModel = TypeVar("DAOModel", bound=tortoise.models.Model)


class BaseDAO(ABC, Generic[DAOModel]):
    """Class for accessing to tortoise model."""

    _model: Type[DAOModel]

    @classmethod
    async def record_exists(cls, id_: int) -> bool:
        obj = await cls.get_by_id(id_)
        return True if obj else False

    @classmethod
    async def create(cls, data: Dict[str, Any]) -> DAOModel:
        """
        Add single model to session.
        """
        return await cls._model.create(**data)

    @staticmethod
    async def update_by_models(models: List[DAOModel]) -> None:
        """
        :param models: List[Model]
        """
        for model in models:
            await model.save()

    @classmethod
    async def update(cls, id_: int, data: Dict[str, Any], prefetch: str = None) -> DAOModel:
        query = cls._model.get(id=id_)
        if prefetch:
            query = query.prefetch_related(prefetch)
        obj = await query
        for k, v in data.items():
            setattr(obj, k, v)

        await obj.save()
        return obj

    @classmethod
    async def get_by_id(cls, id_: int) -> DAOModel:
        return await cls._model.get(id=id_)

    @classmethod
    async def get_all(
        cls,
        limit: int,
        offset: int,
        with_count: bool = False,
    ) -> Union[Tuple[List[DAOModel], int], List[DAOModel]]:
        """
        Get all models with limit/offset pagination.
        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :param with_count: count of all records.
        :return: stream of dummies.
        """
        data = await cls._model.all().offset(offset).limit(limit)
        if with_count:
            count = await cls._model.all().count()
            return data, count

        return data

    @classmethod
    async def _get_all_with_prefetch(
        cls,
        limit: int,
        offset: int,
        prefetch: str,
        with_count: bool = False,
    ) -> Union[tuple[list[DAOModel], int], list[DAOModel]]:
        data = (
            await cls._model.all()
            .offset(offset)
            .limit(limit)
            .prefetch_related(prefetch)
        )
        if with_count:
            count = await cls._model.all().count()
            return data, count

        return data

    @classmethod
    async def filter(cls, data: Dict[str, Any]) -> List[DAOModel]:
        """
        Get specific model.
        """
        query = cls._model.all()
        query = query.filter(**data)
        return await query

    @classmethod
    async def filter_with_order(
        cls,
        filter_data: Dict[str, Any],
        order_col_name: str,
    ) -> List[DAOModel]:
        query = cls._model.all().filter(**filter_data).order_by(order_col_name)
        return await query

    @classmethod
    async def filter_with_prefetch(
        cls,
        data: Dict[str, Any],
        prefetch: str,
    ) -> List[DAOModel]:
        """
        Get specific model.
        """
        query = cls._model.all().filter(**data).prefetch_related(prefetch)
        return await query

    @classmethod
    async def delete_by_id(cls, id_: int) -> Any:  # id_ отдельным коммитом
        obj = await cls._model.get_by_id(id_)
        return await obj.delete()

    @classmethod
    async def exclude(cls, data: Dict[str, Any]) -> List[DAOModel]:
        return await cls._model.exclude(**data)

    @classmethod
    async def get_or_none(cls, data: Dict[str, Any]) -> Optional[DAOModel]:
        return await cls._model.get_or_none(**data)

    @classmethod
    async def get_or_none_with_prefetch(
        cls,
        data: Dict[str, Any],
        prefetch: str
    ) -> Optional[DAOModel]:
        return await cls._model.get_or_none(**data).prefetch_related(prefetch)
