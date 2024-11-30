"""
Этот файл содержит определение схем данных для тура в приложении, используя библиотеку Pydantic.
Он включает в себя несколько классов, каждый из которых представляет собой схему с определенными атрибутами и
валидацией.
"""

import logging
from typing import Any
from fastapi import Path
from pydantic import BaseModel, field_validator

# Настройка логирования
logger = logging.getLogger('log')


class SchemaTour(BaseModel):
    """
    Схема для описания тура.

    Атрибуты:
        title (str): Название тура (максимум 17 символов).
        description (str): Описание тура (максимум 1100 символов).
        place (str): Место проведения тура (максимум 27 символов).
        start_date_tour (str): Дата начала тура.
        duration (int): Длительность тура в днях (должно быть больше 0).
        max_people (int): Максимальное количество участников тура (должно быть больше 0).
        available_places (int): Количество доступных мест (должно быть больше 0).
        occupied_places (int): Количество занятых мест (по умолчанию 0).
        price_per_person (int): Цена за человека.
    """
    title: str = Path(max_length=17)
    description: str = Path(max_length=1100)
    place: str = Path(max_length=27)
    start_date_tour: str
    duration: int = Path(gt=0)
    max_people: int = Path(gt=0)
    available_places: int = Path(gt=0)
    occupied_places: int = 0
    price_per_person: int

    @field_validator('duration')
    @classmethod
    def duration_must_be_positive(cls, value: Any):
        """
        Проверяет, что значение длительности тура положительное.

        Параметры:
            value (Any): Значение длительности.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле duration введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value

    @field_validator('max_people')
    @classmethod
    def max_people_must_be_positive(cls, value: Any):
        """
        Проверяет, что максимальное количество участников положительное.

        Параметры:
            value (Any): Значение максимального количества участников.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле max_people введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value

    @field_validator('available_places')
    @classmethod
    def available_places_must_be_positive(cls, value: Any):
        """
        Проверяет, что количество доступных мест положительное.

        Параметры:
            value (Any): Значение доступных мест.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле available_places введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value

    @field_validator('price_per_person')
    @classmethod
    def price_per_person_must_be_positive(cls, value: Any):
        """
        Проверяет, что цена за человека положительная.

        Параметры:
            value (Any): Значение цены за человека.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле price_per_person введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value


class Tour(SchemaTour):
    """
    Схема для описания тура с идентификатором.

    Наследует:
        SchemaTour: Базовая схема тура.

    Атрибуты:
        id (int): Уникальный идентификатор тура.
    """
    id: int


class TourUpdate(BaseModel):
    """
    Схема для обновления информации о туре.

    Атрибуты:
        new_title (str): Новое название тура (максимум 17 символов).
        new_description (str): Новое описание тура (максимум 1100 символов).
        new_place (str): Новое место проведения тура (максимум 27 символов).
        new_start_date_tour (str): Новая дата начала тура.
        new_duration (int): Новая длительность тура в днях (должно быть больше 0).
        new_max_people (int): Новое максимальное количество участников тура (должно быть больше 0).
        new_available_places (int): Новое количество доступных мест (должно быть больше 0).
        new_occupied_places (int): Новое количество занятых мест (по умолчанию 0).
        new_price_per_person (int): Новая цена за человека.
    """
    new_title: str = Path(max_length=17)
    new_description: str = Path(max_length=1100)
    new_place: str = Path(max_length=27)
    new_start_date_tour: str
    new_duration: int = Path(gt=0)
    new_max_people: int = Path(gt=0)
    new_available_places: int = Path(gt=0)
    new_occupied_places: int = 0
    new_price_per_person: int

    @field_validator('new_duration')
    @classmethod
    def new_duration_must_be_positive(cls, value: Any):
        """
        Проверяет, что новое значение длительности тура положительное.

        Параметры:
            value (Any): Значение новой длительности.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле new_duration введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value

    @field_validator('new_max_people')
    @classmethod
    def new_max_people_must_be_positive(cls, value: Any):
        """
        Проверяет, что новое максимальное количество участников положительное.

        Параметры:
            value (Any): Значение нового максимального количества участников.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле new_max_people введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value

    @field_validator('new_available_places')
    @classmethod
    def new_available_places_must_be_positive(cls, value: Any):
        """
        Проверяет, что новое количество доступных мест положительное.

        Параметры:
            value (Any): Значение новых доступных мест.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле new_available_places введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value

    @field_validator('new_price_per_person')
    @classmethod
    def new_price_per_person_must_be_positive(cls, value: Any):
        """
        Проверяет, что новая цена за человека положительная.

        Параметры:
            value (Any): Значение новой цены за человека.

        Возвращает:
            Any: Проверенное значение.

        Исключения:
            ValueError: Если значение меньше или равно 0.
        """
        if value <= 0:
            logger.warning('В поле new_price_per_person введено отрицательное значение')
            raise ValueError("Данное значение должно быть больше 0.")
        return value
