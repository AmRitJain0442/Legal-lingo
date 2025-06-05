from typing import Optional, Union

from pydantic import BaseModel


class DatabasePoolInfo(BaseModel):
    size: Union[int, str]
    checked_in: Union[int, str]
    checked_out: Union[int, str]


class DatabaseHealthInfo(BaseModel):
    connected: bool
    version: Optional[str] = None
    tables_accessible: bool
    table_count: int
    pool_info: DatabasePoolInfo
    error: Optional[str] = None


class HealthResponseData(BaseModel):
    app_name: str
    version: str
    timestamp: str
    database: DatabaseHealthInfo
