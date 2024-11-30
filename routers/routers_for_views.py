"""
Этот файл содержит маршруты и обработчики, которые предоставляют доступ к общим страницам и функционалу для
пользователей приложения.
"""

import logging
from sqlalchemy import select
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.db import SessionLocal, TourTable

# Настройка логирования
logger = logging.getLogger('log')

# Настройка шаблонов Jinja2
templates = Jinja2Templates(directory='templates')

# Создание маршрутизатора для отображения туров
router = APIRouter(prefix='/views', tags=['Отображение туров'])


@router.get('/tours/', response_class=HTMLResponse)
async def tours_page(request: Request):
    """
    Отображает страницу со списком всех туров.

    Параметры:
        request (Request): Объект запроса FastAPI.

    Возвращает:
        HTMLResponse: HTML-страница со списком туров или страница с сообщением о пустом списке.
    """
    logger.debug("Запрос на страницу туров")
    with SessionLocal() as session:
        logger.debug("Открытие сессии базы данных")
        query = select(TourTable)
        logger.debug(f"Выполнение запроса: {query}")
        result = session.execute(query)
        tour_models = result.scalars().all()
        if not tour_models:
            logger.info("Список туров пуст")
            context = {
                'request': request,
            }
            return templates.TemplateResponse('empty_list_tours_page.html', context)
        logger.info(f"Найдено {len(tour_models)} туров")
        context = {
            'request': request,
            'tour_models': tour_models,
        }
        return templates.TemplateResponse('list_tours_page.html', context)


@router.get('/tours/current_tour/{tour_id}')
async def current_tour_page(request: Request, tour_id: int):
    """
    Отображает страницу с информацией о текущем туре по его ID.

    Параметры:
        request (Request): Объект запроса FastAPI.
        tour_id (int): ID тура, который необходимо отобразить.

    Возвращает:
        HTMLResponse: HTML-страница с информацией о туре или страница ошибки, если тур не найден.

    Исключения:
        HTTPException: Если тур с указанным ID не найден.
    """
    logger.debug(f"Запрос на страницу текущего тура с ID: {tour_id}")
    try:
        with SessionLocal() as session:
            logger.debug("Открытие сессии базы данных")
            query = select(TourTable).where(TourTable.id == tour_id)
            logger.debug(f"Выполнение запроса: {query}")
            result = session.execute(query)
            tour = result.scalars().first()
            if not tour:
                logger.warning(f"Тур с ID {tour_id} не найден")
                raise HTTPException(status_code=404, detail="Тур не найден")

            logger.info(f"Тур с ID {tour_id} найден")
            context = {
                'request': request,
                'tour': tour,
            }
            return templates.TemplateResponse('book_tour_page.html', context)
    except HTTPException as e:
        logger.error(f"Ошибка: {e.detail} - ID тура: {tour_id}")
        context = {
            'request': request,
        }
        return templates.TemplateResponse('error_page.html', context)
