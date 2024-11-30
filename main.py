"""
Этот файл является основным файлом приложения на FastAPI.
"""

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database.db import create_tables
from routers.routers_for_admin import router as admin_routers
from routers.routers_for_views import router as views_routers
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging.config
from log_settings.log_settings import LOGGING

# Настройка логирования
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('log')

# Инициализация шаблонов Jinja2
templates = Jinja2Templates(directory='templates')

# Создание таблиц в базе данных
create_tables()

# Инициализация приложения FastAPI
app = FastAPI()

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение маршрутов для администраторов и для просмотра
app.include_router(admin_routers)
app.include_router(views_routers)


@app.get('/')
async def welcome_page(request: Request):
    """
    Обработчик для главной страницы приветствия.

    Параметры:
        request (Request): Объект запроса.

    Возвращает:
        TemplateResponse: Шаблон главной страницы с контекстом запроса.
    """
    logger.debug('Страница приветствия загружена')
    return templates.TemplateResponse('base_page.html', {'request': request})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """
    Обработчик исключений для несуществующих URL.

    Параметры:
        request (Request): Объект запроса.
        exc (StarletteHTTPException): Исключение HTTP.

    Возвращает:
        TemplateResponse: Шаблон страницы ошибки с контекстом запроса.
    """
    logger.warning(f"Запрошен несуществующий адрес URL: {request.url}")
    context = {
        'request': request,
    }
    return templates.TemplateResponse('error_page.html', context)
