import json
import logging
from pathlib import Path

from app.core.exceptions import BaseAppError
from app.io.readers import get_reader
from app.services.processor import DataProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


def run_pipeline(data_dir: Path, result_path: Path) -> None:
    """Основной процесс загрузки и обработки данных."""
    if not data_dir.exists():
        logging.fatal("Директория 'data' не найдена. (Fail Fast).")
        return

    processor = DataProcessor()
    processed_count = 0
    success_count = 0
    errors = []

    for file_path in data_dir.iterdir():
        if file_path.is_file():
            processed_count += 1
            try:
                reader = get_reader(file_path.suffix)
                raw_data = reader.read(file_path)
                processor.validate_and_aggregate(raw_data, file_path.name)
                success_count += 1
                logging.info(f"Файл успешно обработан: {file_path.name}")
            except BaseAppError as e:
                errors.append(str(e))
                logging.warning(str(e))
            except Exception as e:
                msg = f"Критический сбой в {file_path.name}: {e}"
                errors.append(msg)
                logging.error(msg)

    print(f"Обработано: {processed_count}. Успешно: {success_count}.")
    if errors:
        print("Список ошибок:")
        for err in errors:
            print(f" - {err}")

    tmp_path = result_path.with_suffix('.tmp')
    try:
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(processor.get_result(), f, indent=4)
        tmp_path.replace(result_path)
        logging.info("Результаты сохранены.")
    except Exception as e:
        logging.error(f"Ошибка сохранения результатов: {e}")
        if tmp_path.exists():
            tmp_path.unlink()


if __name__ == '__main__':
    run_pipeline(Path('data'), Path('result.json'))
