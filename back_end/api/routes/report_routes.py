"""
Report routes - Building finance and other reports (gọi functions PostgreSQL)
"""
import json
from fastapi import APIRouter, HTTPException, Query
from typing import Any, List, Optional

router = APIRouter(tags=["Reports"])


def _ensure_list(val: Any) -> List[Any]:
    """Đảm bảo giá trị từ JSONB (asyncpg có thể trả str) thành list."""
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        try:
            parsed = json.loads(val)
            return parsed if isinstance(parsed, list) else []
        except (json.JSONDecodeError, TypeError):
            return []
    return []


@router.get("/reports/building-finance")
async def get_building_finance(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020)
):
    """
    Tổng thu chi tòa nhà theo tháng — gọi function get_building_finance(p_year, p_month).
    """
    if not month or not year:
        raise HTTPException(status_code=400, detail="Tháng và năm là bắt buộc")
    try:
        from api.database import get_pool
        pool = get_pool()
        query = "SELECT * FROM get_building_finance($1, $2)"
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, year, month)
            if not row:
                return {
                    "month": int(month),
                    "year": int(year),
                    "total_revenue": 0.0,
                    "revenue_breakdown": {"rent": 0.0, "services": 0.0},
                    "total_expense": 0.0,
                    "net_profit": 0.0,
                }
            return {
                "month": int(row.get("month", month)),
                "year": int(row.get("year", year)),
                "total_revenue": float(row.get("total_revenue") or 0),
                "revenue_breakdown": {
                    "rent": float(row.get("revenue_rent") or 0),
                    "services": float(row.get("revenue_services") or 0),
                },
                "total_expense": float(row.get("total_expense") or 0),
                "net_profit": float(row.get("net_profit") or 0),
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/reports/building-finance/details")
async def get_building_finance_details(
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020)
):
    """
    Chi tiết thu chi tòa nhà theo tháng — gọi function get_building_finance_details(p_year, p_month).
    """
    if not month or not year:
        raise HTTPException(status_code=400, detail="Tháng và năm là bắt buộc")
    try:
        from api.database import get_pool
        pool = get_pool()
        query = "SELECT * FROM get_building_finance_details($1, $2)"
        async with pool.acquire() as conn:
            row = await conn.fetchrow(query, year, month)
            if not row:
                return {
                    "month": month,
                    "year": year,
                    "total_revenue": 0.0,
                    "total_expense": 0.0,
                    "net_profit": 0.0,
                    "revenue_details": [],
                    "expense_details": [],
                }
            rev_details = _ensure_list(row.get("revenue_details"))
            for r in rev_details:
                if isinstance(r, dict):
                    for key in ("from_date", "to_date"):
                        val = r.get(key)
                        if val is not None and hasattr(val, "isoformat"):
                            r[key] = val.isoformat()

            exp_details = _ensure_list(row.get("expense_details"))

            return {
                "month": int(row.get("month", month)),
                "year": int(row.get("year", year)),
                "total_revenue": float(row.get("total_revenue") or 0),
                "total_expense": float(row.get("total_expense") or 0),
                "net_profit": float(row.get("net_profit") or 0),
                "revenue_details": rev_details,
                "expense_details": exp_details,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
