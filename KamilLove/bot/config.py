import logging
from pathlib import Path

from dotenv import dotenv_values

# Настраиваем логирование по умолчанию, если оно еще не было инициализировано
if not logging.getLogger().handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

logger = logging.getLogger(__name__)

_env_path = Path(__file__).parent.parent / ".env"

# Загрузка строго из .env (без os.environ)
if _env_path.is_file():
    logger.debug(f"Найден файл конфигурации: {_env_path}")
    _env_vars = dotenv_values(_env_path)
    logger.debug(
        f"Переменные успешно прочитаны из .env (найдено ключей: {len(_env_vars)})"
    )
else:
    logger.warning(
        f"Файл .env не найден по пути: {_env_path}. "
        "Настройки будут пустыми, так как чтение системных переменных отключено."
    )
    _env_vars = {}


class Settings:
    def __init__(self) -> None:
        logger.info("Инициализация настроек приложения (только из .env)...")

        # Берем значения ТОЛЬКО из словаря _env_vars.
        # Если ключа нет или он пустой (None), используем дефолт через `or`.
        self.BOT_TOKEN: str = _env_vars.get("BOT_TOKEN") or ""
        self.PROXY_URL: str = _env_vars.get("PROXY_URL") or ""

        # --- Логирование загруженных значений ---

        # 1. BOT_TOKEN (с маскировкой)
        if self.BOT_TOKEN:
            if len(self.BOT_TOKEN) > 12:
                masked_token = f"{self.BOT_TOKEN[:4]}...{self.BOT_TOKEN[-4:]}"
            else:
                masked_token = "***"
            logger.info(
                f"  [Config] BOT_TOKEN: {masked_token} (длина: {len(self.BOT_TOKEN)})"
            )
        else:
            logger.error("  [Config] BOT_TOKEN: ОТСУТСТВУЕТ!")

        # 2. PROXY_URL
        if self.PROXY_URL:
            logger.info(f"  [Config] PROXY_URL: {self.PROXY_URL}")
        else:
            logger.info("  [Config] PROXY_URL: не задан (прямое подключение)")

        # --- Валидация ---
        if not self.BOT_TOKEN:
            logger.critical(
                "Критическая ошибка: BOT_TOKEN не найден в .env. Бот не может быть запущен."
            )
            raise RuntimeError("BOT_TOKEN не найден в .env")


# Инициализируем настройки
settings = Settings()
