from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    status: int = Field(..., description="Status code: 0 for failure, 1 for success")
    message: str = Field(..., min_length=1, description="Response message")
    data: Optional[T] = Field(None, description="Response data")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: int) -> int:
        if v not in [0, 1]:
            raise ValueError("Status must be 0 (failure) or 1 (success)")
        return v

    @classmethod
    def success(cls, message: str, data: Optional[T] = None) -> "BaseResponse[T]":
        """Create a success response"""
        return cls(status=1, message=message, data=data)

    @classmethod
    def error(cls, message: str, data: Optional[T] = None) -> "BaseResponse[T]":
        """Create an error response"""
        return cls(status=0, message=message, data=data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert to JSON string"""
        return self.model_dump_json()

    def __str__(self) -> str:
        return f"BaseResponse(status={self.status}, message='{self.message}')"

    def __repr__(self) -> str:
        return f"BaseResponse(status={self.status}, message='{self.message}', data={self.data})"
