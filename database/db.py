"""
Этот файл отвечает за взаимодействие с базой данных. Он содержит функции для подключения к базе данных и
выполнения операций, таких как создание таблиц, добавление, удаление и обновление записей.
"""

import logging
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Настройка логирования
logger = logging.getLogger('log')

# URL для подключения к базе данных
DATABASE_URL = "sqlite:///./data.db"

# Создание движка базы данных с использованием SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание локальной сессии для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание объекта MetaData для управления схемой базы данных
metadata = MetaData()

# Создание базового класса для декларативного определения моделей
Base = declarative_base()


class TourTable(Base):
    """
    Модель базы данных для таблицы "tours", представляющая информацию о турах.

    Атрибуты:
    id (int): Уникальный идентификатор тура (первичный ключ).
    title (str): Название тура.
    description (str): Описание тура.
    place (str): Место проведения тура.
    start_date_tour (str): Дата начала тура.
    duration (int): Продолжительность тура в днях.
    max_people (int): Максимальное количество человек.
    available_places (int): Количество доступных мест.
    occupied_places (int): Количество занятых мест.
    price_per_person (int): Цена за человека.
    image (str): URL или путь к изображению тура.
    """
    __tablename__ = 'tours'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    place = Column(String)
    start_date_tour = Column(String)
    duration = Column(Integer)
    max_people = Column(Integer)
    available_places = Column(Integer)
    occupied_places = Column(Integer)
    price_per_person = Column(Integer)
    image = Column(String)


def create_tables():
    """
    Создает таблицы в базе данных на основе определенных моделей.

    Эта функция использует SQLAlchemy для создания всех таблиц, определенных в моделях,
    наследуемых от базового класса Base. В данном случае создается таблица "tours".

    Логирует информацию о создании базы данных и добавлении таблицы.
    """
    Base.metadata.create_all(bind=engine)
    logger.info(f'База данных создана. Добавлена таблица: "{TourTable.__tablename__}"')
