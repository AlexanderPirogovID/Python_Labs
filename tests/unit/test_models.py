import pytest
from app.core.models import Transaction


@pytest.mark.parametrize("tx_id, amount, category, date, currency", [
    ("tx_001", 150.0, "Food", "2023-10-01", "USD"),
    ("tx_002", 300.5, "Transport", "2023-10-02", "EUR"),
    ("tx_003", 50.0, "Salary", "2023-10-03", None),  # Проверка дефолтного
])
def test_transaction_creation(tx_id, amount, category, date, currency):
    """Проверка корректной инициализации датакласса Transaction."""
    if currency:
        tx = Transaction(
            id=tx_id, amount=amount, category=category, date=date, currency=currency
        )
        assert tx.currency == currency
    else:
        # Проверяем значение по умолчанию ("USD")
        tx = Transaction(id=tx_id, amount=amount, category=category, date=date)
        assert tx.currency == "USD"

    assert tx.id == tx_id
    assert tx.amount == amount
    assert tx.category == category
    assert tx.date == date
