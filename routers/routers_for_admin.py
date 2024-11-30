"""
Этот файл содержит маршруты и обработчики, специфичные для административной части приложения.
Он может включать функции для управления турами и другие административные действия.
"""

import os
import shutil
import logging
from typing import Annotated
from sqlalchemy import select
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from database.db import SessionLocal, TourTable
from schemas.schem import SchemaTour, TourUpdate

# Настройка логирования
logger = logging.getLogger('log')

# Настройка шаблонов Jinja2
templates = Jinja2Templates(directory='templates')

# Создание маршрутизатора для администратора
router = APIRouter(prefix='/admin', tags=['Админ панель'])


@router.get('/get_tours_admin')
async def get_tours():
    """
    Получает список всех туров из базы данных.

    Возвращает:
        list: Список объектов туров.
    """
    with SessionLocal() as session:
        logger.debug("Открытие сессии базы данных")
        query = select(TourTable)
        result = session.execute(query)
        logger.debug(f"Выполнение запроса: {query}")
        tour_models = result.scalars().all()
        logger.info(f"Найдено {len(tour_models)} туров")
        return tour_models


@router.post('/upload_tour_admin')
async def upload_tour(tour: Annotated[SchemaTour, Depends()], image: UploadFile = File(...)):
    """
    Загружает новый тур в базу данных.

    Параметры:
        tour (SchemaTour): Данные о туре.
        image (UploadFile): Изображение тура.

    Возвращает:
        int: ID загруженного тура.
    """
    logger.debug("Запрос на загрузку нового тура")
    with SessionLocal() as session:
        image_path = os.path.join(
            'static', 'image', 'img_tour', image.filename)

        with open(image_path, 'wb') as buffer:
            shutil.copyfileobj(image.file, buffer)

        tours_dict = tour.model_dump()
        tours_dict['image'] = image.filename

        tour = TourTable(**tours_dict)
        session.add(tour)
        session.flush()
        session.commit()
        logger.info(f"Тур загружен с ID: {tour.id}")
        return tour.id


@router.put('/update_tour_admin')
async def update_tour(tour_id: int, tour_update: Annotated[TourUpdate, Depends()], new_image: UploadFile = File(...)):
    """
    Обновляет существующий тур в базе данных.

    Параметры:
        tour_id (int): ID тура, который необходимо обновить.
        tour_update (TourUpdate): Новые данные о туре.
        new_image (UploadFile): Новое изображение тура.

    Возвращает:
            dict: Подтверждение обновления и обновленный объект тура.

    Исключения:
        HTTPException: Если тур с указанным ID не найден.
    """
    logger.debug(f"Запрос на обновление тура с ID: {tour_id}")
    with SessionLocal() as session:
        image_path = os.path.join(
            'static', 'image', 'img_tour', new_image.filename)

        with open(image_path, 'wb') as buffer:
            shutil.copyfileobj(new_image.file, buffer)

        logger.debug("Открытие сессии базы данных")
        query = select(TourTable).where(TourTable.id == tour_id)
        logger.debug(f"Выполнение запроса: {query}")
        result = session.execute(query)
        tour_model = result.scalars().first()

        if not tour_model:
            logger.warning(f"Тур с ID {tour_id} не найден")
            raise HTTPException(status_code=404, detail="Тур не найден")

        logger.info(f"Обновление тура с ID: {tour_id}")
        tour_model.title = tour_update.new_title
        tour_model.description = tour_update.new_description
        tour_model.place = tour_update.new_place
        tour_model.start_date_tour = tour_update.new_start_date_tour
        tour_model.duration = tour_update.new_duration
        tour_model.max_people = tour_update.new_max_people
        tour_model.available_places = tour_update.new_available_places
        tour_model.occupied_places = tour_update.new_occupied_places
        tour_model.price_per_person = tour_update.new_price_per_person
        image_path_deleted = os.path.join(
            'static', 'image', 'img_tour', tour_model.image)
        if os.path.exists(image_path_deleted):
            os.remove(image_path_deleted)
        tour_model.image = new_image.filename

        session.commit()
        logger.info(f"Тур с ID: {tour_id} успешно обновлён")
        return {"detail": "Tour updated successfully", "tour": tour_model}


@router.delete('/delete_tour_admin')
async def deleted_tour(tour_id: int):
    """
    Удаляет тур из базы данных.

    Параметры:
        tour_id (int): ID тура, который необходимо удалить.

    Возвращает:
        dict: Подтверждение удаления тура.

    Исключения:
        HTTPException: Если тур с указанным ID не найден.
    """
    logger.debug(f"Запрос на удаление тура с ID: {tour_id}")
    with SessionLocal() as session:
        logger.debug("Открытие сессии базы данных")
        query = select(TourTable).where(TourTable.id == tour_id)
        logger.debug(f"Выполнение запроса: {query}")

        result = session.execute(query)
        tour_model = result.scalars().first()

        if not tour_model:
            logger.warning(f"Тур с ID {tour_id} не найден")
            raise HTTPException(status_code=404, detail="Тур не найден")

        session.delete(tour_model)
        logger.info(f"Тур с ID: {tour_id} успешно удалён")
        session.commit()

        return {"detail": "Tour deleted successfully"}
