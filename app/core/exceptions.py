class BaseAppError(Exception):
    """Базовое исключение для проекта."""
    pass


class DataFormatError(BaseAppError):
    """Ошибка структуры или чтения файла."""
    pass


class ValidationError(BaseAppError):
    """Ошибка бизнес-логики (неверные значения)."""
    pass


class CurrencyMismatchError(BaseAppError):
    """Ошибка при несовпадении валют."""
    pass
