from fastapi import HTTPException, Request, Depends
from pydantic import BaseModel, ValidationError
from typing import TypeVar, Type
from app.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


def validate_request_params(request: Request, model_class: Type[T]) -> T:
    try:
        params = dict(request.query_params)
        return model_class(**params)
    except ValidationError as val_err:
        error_messages = []
        for error in val_err.errors():
            field = error["loc"][0]
            msg = error["msg"]
            error_messages.append(f"{field}: {msg}")

        logger.error(f"Validation error: {str(val_err)}")
        raise HTTPException(
            status_code=400,
            detail=error_messages[0] if error_messages else "Validation error",
        )


T = TypeVar("T", bound=BaseModel)


def ValidatedParams(model_class: Type[T]):
    async def validate(request: Request) -> T:
        return validate_request_params(request, model_class)

    return Depends(validate)
