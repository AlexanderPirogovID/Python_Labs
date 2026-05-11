from datetime import datetime
from typing import List, Dict, Any

from app.core.exceptions import ValidationError


class DataProcessor:
    """Класс для обработки и агрегации финансовых транзакций."""

    def __init__(self):
        self.aggregated_data: Dict[str, float] = {}
        self.seen_ids = set()

    def validate_and_aggregate(
        self, raw_data: List[Dict[str, Any]], filename: str
    ) -> None:
        """Валидирует список транзакций и агрегирует суммы по категориям."""
        for index, row in enumerate(raw_data):
            required_keys = {'id', 'amount', 'category', 'date'}
            if not required_keys.issubset(row.keys()):
                raise ValidationError(
                    f"[{filename}] Запись {index}: нет обязательных полей."
                )

            tx_id = str(row['id']).strip()
            if not tx_id:
                raise ValidationError(f"[{filename}] Пустой ID.")

            if tx_id in self.seen_ids:
                raise ValidationError(f"[{filename}] Дубликат ID: {tx_id}.")

            try:
                amount = float(row['amount'])
            except (ValueError, TypeError):
                raise ValidationError(f"[{filename}] {tx_id}: amount не число.")

            if amount <= 0:
                raise ValidationError(f"[{filename}] {tx_id}: amount <= 0.")
            if amount > 1e9:  # Защита от переполнения
                raise ValidationError(f"[{filename}] {tx_id}: сумма огромна.")

            try:
                datetime.strptime(str(row['date']), "%Y-%m-%d")
            except ValueError:
                raise ValidationError(f"[{filename}] {tx_id}: неверная дата.")

            category = str(row['category']).strip()
            self.seen_ids.add(tx_id)
            self.aggregated_data[category] = self.aggregated_data.get(
                category, 0.0
            ) + amount

    def get_result(self) -> Dict[str, float]:
        """Возвращает агрегированный результат."""
        return self.aggregated_data
