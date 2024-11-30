"""
Этот файл содержит настройки логирования для приложения. Он определяет конфигурацию логирования,
такую как уровень логирования, формат сообщений и обработчики.
"""

# Импортируем класс Path из модуля pathlib для работы с файловыми путями.
from pathlib import Path

# Определяем BASE_DIR как путь к директории, в которой находится текущий файл, с разрешением на абсолютный путь.
BASE_DIR = Path(__file__).resolve().parent.parent

# Определяем словарь конфигурации для логирования.
LOGGING = {
    # Указываем версию конфигурации логирования (1 - это текущая версия).
    'version': 1,
    # Указываем, что существующие логгеры не должны быть отключены.
    'disable_existing_loggers': False,

    'formatters': {  # Определяем форматтеры для форматирования лог-сообщений.
        'main_format': {  # Имя форматтера.
            # Шаблон формата лог-сообщений.
            'format': '[{asctime}] - [{levelname}] - {module} - /{filename} : {message}',
            # Указываем стиль форматирования (используем фигурные скобки).
            'style': '{',
        },
    },

    'handlers': {  # Определяем обработчики логирования, которые будут записывать сообщения.
        'console': {  # Обработчик для вывода логов в консоль.
            'class': 'logging.StreamHandler',  # Указываем класс обработчика.
            # Применяем форматтер 'main_format' к этому обработчику.
            'formatter': 'main_format',
        },
        'file': {  # Обработчик для записи логов в файл.
            # Указываем класс обработчика для записи в файл.
            'class': 'logging.FileHandler',
            # Применяем форматер 'main_format' к этому обработчику.
            'formatter': 'main_format',
            # Указываем имя файла для записи логов, используя BASE_DIR.
            'filename': BASE_DIR / 'logs.log'
        },
    },

    'loggers': {  # Определяем логгеры, которые будут использоваться в приложении.
        'log': {  # Имя логгера.
            # Указываем, что логгер будет использовать обработчик 'file'.
            'handlers': ['file'],
            'level': 'DEBUG',  # Устанавливаем уровень логирования на 'DEBUG'.
            # Указываем, что сообщения этого логгера будут передаваться родительским логгерам.
            'propagate': True,
        },
    },
}
