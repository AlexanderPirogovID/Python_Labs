import pytest
from app.services.processor import DataProcessor


@pytest.fixture
def processor():
    """Возвращает свежий экземпляр DataProcessor для каждого теста."""
    return DataProcessor()


@pytest.fixture
def valid_transaction():
    """Возвращает шаблон валидной транзакции."""
    return {
        "id": "t_100",
        "amount": "500.50",
        "category": "Sales",
        "date": "2023-12-01"
    }
