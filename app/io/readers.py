import csv
import json
from pathlib import Path
from typing import List, Dict, Any
from app.core.exceptions import DataFormatError


class BaseReader:
    def read(self, file_path: Path) -> List[Dict[str, Any]]:
        raise NotImplementedError


class CSVReader(BaseReader):
    def read(self, file_path: Path) -> List[Dict[str, Any]]:
        data = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            raise DataFormatError(f"Ошибка чтения CSV {file_path.name}: {e}")
        return data


class JSONReader(BaseReader):
    def read(self, file_path: Path) -> List[Dict[str, Any]]:
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise DataFormatError("JSON должен содержать список.")
                return data
        except json.JSONDecodeError as e:
            msg = f"Ошибка парсинга JSON {file_path.name}: {e}"
            raise DataFormatError(msg)
        except Exception as e:
            msg = f"Ошибка чтения JSON {file_path.name}: {e}"
            raise DataFormatError(msg)


# Registry Pattern
READERS_REGISTRY = {
    '.csv': CSVReader(),
    '.json': JSONReader()
}


def get_reader(file_extension: str) -> BaseReader:
    reader = READERS_REGISTRY.get(file_extension.lower())
    if not reader:
        raise DataFormatError(f"Неподдерживаемый формат: {file_extension}")
    return reader
