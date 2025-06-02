import pandas as pd

from domain.exceptions import DataSourceError


class DataSource:
    def read(self) -> pd.DataFrame:
        try:
            return self._load_data()
        except Exception as e:
            raise DataSourceError(
                f"Failed to read data source: {str(e)}"
            ) from e

    def _load_data(self) -> pd.DataFrame:
        """Метод должен быть реализован в подклассах"""
        raise NotImplementedError
