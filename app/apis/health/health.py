from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import get_async_db, settings
from app.core.utils.response import BaseResponse

from .models import DatabaseHealthInfo, DatabasePoolInfo, HealthResponseData

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=BaseResponse[HealthResponseData])
async def health_check(
    db: AsyncSession = Depends(get_async_db),
) -> BaseResponse[HealthResponseData]:
    try:
        await db.execute(text("SELECT 1"))
        connected = True

        result = await db.execute(text("SELECT version()"))
        version = result.scalar()

        try:
            result = await db.execute(
                text(
                    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
                )
            )
            table_count = result.scalar()
            tables_accessible = True
        except Exception:
            table_count = 0
            tables_accessible = False

        pool_info = DatabasePoolInfo(
            size=db.bind.pool.size() if hasattr(db.bind, "pool") else "unknown",
            checked_in=db.bind.pool.checkedin()
            if hasattr(db.bind, "pool")
            else "unknown",
            checked_out=db.bind.pool.checkedout()
            if hasattr(db.bind, "pool")
            else "unknown",
        )

        database_info = DatabaseHealthInfo(
            connected=connected,
            version=version,
            tables_accessible=tables_accessible,
            table_count=table_count,
            pool_info=pool_info,
        )

        health_data = HealthResponseData(
            app_name=settings.app_name,
            version=settings.app_version,
            timestamp=datetime.now().isoformat(),
            database=database_info,
        )

        return BaseResponse.success(
            message=f"{settings.app_name} is running healthy!", data=health_data
        )

    except Exception as e:
        pool_info = DatabasePoolInfo(
            size="unknown", checked_in="unknown", checked_out="unknown"
        )

        database_info = DatabaseHealthInfo(
            connected=False,
            version=None,
            tables_accessible=False,
            table_count=0,
            pool_info=pool_info,
            error=str(e),
        )

        health_data = HealthResponseData(
            app_name=settings.app_name,
            version=settings.app_version,
            timestamp=datetime.now().isoformat(),
            database=database_info,
        )

        return BaseResponse.error(
            message="Database connection failed - service unhealthy", data=health_data
        )
