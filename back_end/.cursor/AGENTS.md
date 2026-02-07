# Hướng Dẫn Coding - Office Building Management System

## Cách xưng hô
Em là culi của chủ nhân Trần Quý Đạt. 

**Tech Stack**: 
- **Backend**: FastAPI + PostgreSQL (SQL thuần 100%)
- **Frontend**: ReactJS

## 🚨 NGUYÊN TẮC QUAN TRỌNG NHẤT

### **CHỈ VIẾT SQL THUẦN**
- ❌ KHÔNG dùng SQLAlchemy ORM, Tortoise, Peewee, Django ORM...
- ✅ CHỈ dùng raw SQL với `asyncpg`
- ✅ Transaction thủ công: `BEGIN`, `COMMIT`, `ROLLBACK`

```python
# ❌ SAI
return await db.query(Office).filter(Office.id == office_id).first()

# ✅ ĐÚNG
query = "SELECT * FROM offices WHERE id = $1"
async with pool.acquire() as conn:
    return await conn.fetchrow(query, office_id)
```

## Kiến Trúc

**Repository → Service → Routes**:
- **Routes**: HTTP handling
- **Service**: Business logic
- **Repository**: SQL queries only
- **Models**: Pydantic schemas

```
back_end/
├── api/
│   ├── main.py
│   ├── config.py
│   ├── database/
│   │   ├── connection.py    # asyncpg pool
│   │   └── transaction.py
│   ├── models/              # Pydantic
│   ├── repositories/        # SQL thuần
│   ├── services/            # Business logic
│   └── routes/
├── migrations/              # SQL files
├── requirements.txt
└── .env.example
```

## 🔄 Server & Database

### Backend Server Auto-Reload
- **Lệnh chạy**: `uvicorn api.main:app --host 0.0.0.0 --port 8222 --reload`
- **Flag quan trọng**: `--reload` (KHÔNG phải `--autoreload`)
- **Kết quả**: Server tự động restart khi code thay đổi
- **⚠️ QUAN TRỌNG**: 
  - Server luôn được chủ nhân tự chạy và quản lý
  - Server tự động reload khi có thay đổi code
  - **KHÔNG BAO GIỜ** được kill, stop, restart, hoặc làm gì ảnh hưởng đến server
  - **KHÔNG** được chạy lệnh pkill, kill, hoặc start lại server
  - Chỉ cần edit code, server sẽ tự reload
- **Database connection**: Tự động reconnect khi server reload

### Frontend Server Auto-Reload (Vite HMR)
- **Lệnh chạy**: `npm run dev` (port 5173)
- **Cơ chế**: Vite HMR (Hot Module Replacement) - tự reload khi code thay đổi
- **⚠️ QUAN TRỌNG**:
  - Frontend server cũng luôn được chủ nhân tự chạy và quản lý
  - **KHÔNG BAO GIỜ** được kill, stop, restart frontend server
  - **KHÔNG** được chạy lệnh npm run dev, pkill node, hay bất kỳ lệnh nào ảnh hưởng đến FE server
  - Chỉ cần edit code React/CSS, browser sẽ tự cập nhật
- **Nếu gặp lỗi kết nối**: Đó KHÔNG phải do server chưa chạy, hãy check code logic thay vì restart server

### Database Management
- Database đã được setup sẵn với sample data
- Connection pool tự động quản lý connections
- Không cần reload database manually
- Scripts sẵn có: `setup_db.py`, `reset_db.py`, `truncate_all.py`

## Patterns Chính

### Connection Pool
```python
# database/connection.py
import asyncpg

pool = await asyncpg.create_pool(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME
)
```

### Repository
```python
async def get_by_id(self, id: int):
    query = "SELECT * FROM offices WHERE id = $1"
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(query, id)
        return dict(row) if row else None
```

### Transaction
```python
@asynccontextmanager
async def transaction():
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            yield conn
```

## Business Rules Chính

### 1. Offices & Contracts
- Văn phòng chỉ 1 công ty thuê/thời điểm (check overlap dates)
- Status: `active`, `expired`, `terminated`

```python
# Check office availability
query = """
    SELECT COUNT(*) FROM rent_contracts
    WHERE office_id = $1 AND status = 'active'
    AND (
        (from_date <= $2 AND end_date >= $2) OR
        (from_date <= $3 AND end_date >= $3) OR
        (from_date >= $2 AND end_date <= $3)
    )
"""
```

### 2. Companies & Employees
- `tax_code` unique
- Status: `working`, `resigned`

### 3. Services & Salary
- `price_method`: `per_sqm`, `per_head`, `fixed`
- Vệ sinh: < 10 người & <= 100m2 = base_price, +5 người hoặc +10m2 = +5%
- Lương = base_salary + (doanh thu * bonus_rate)

### 4. Invoices
- Status: `paid`, `unpaid`, `overdue`
- Gộp: thuê + dịch vụ tháng + dịch vụ ngày

## Yêu cầu API

1. **CRUD**: offices, companies, employees, services, contracts
2. **Chi phí công ty theo tháng**: `GET /api/companies/monthly-costs`
3. **Chi tiết dịch vụ**: `GET /api/companies/{id}/service-details`
4. **Lương nhân viên**: `GET /api/building-employees/salaries`
5. **Thu chi tòa nhà**: `GET /api/reports/building-finance`

## Migration & Files

```sql
-- migrations/001_initial_schema.sql
-- PostgreSQL Schema
CREATE TABLE offices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    area DECIMAL(10,2) NOT NULL,
    ...
);
```

**requirements.txt**:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
asyncpg==0.29.0
pydantic==2.5.3
pydantic-settings==2.1.0
```

## 🧪 Auto Test Toolkit

### Cấu trúc
```
back_end/auto_test/
├── api/
│   ├── api_utils.py     # APIExplorer + standalone functions (gọi từng API)
│   └── test_api.py      # 18 API tests (chạy all hoặc từng test)
├── sql/
│   ├── db_utils.py      # DatabaseUtils + quick_query/quick_execute
│   └── test_sql.py      # 10 SQL tests (chạy all hoặc từng test)
├── script/              # DB management scripts
└── output/              # JSON output (auto-generated)
```

### Chạy Tests

```bash
# Chạy toàn bộ API tests (98 assertions)
cd back_end && python -m auto_test.api.test_api

# Chạy 1 test cụ thể
cd back_end && python -m auto_test.api.test_api test_company_monthly_costs

# Chạy toàn bộ SQL tests (31 assertions)
cd back_end && python -m auto_test.sql.test_sql

# Chạy 1 SQL test cụ thể
cd back_end && python -m auto_test.sql.test_sql test_tables_exist
```

### Gọi Từng API Để Debug (Agent Toolkit)

Khi cần phân tích input/output của 1 API cụ thể, dùng `APIExplorer`:

```python
from auto_test.api.api_utils import APIExplorer

explorer = APIExplorer()

# Gọi từng API, xem input/output
result = await explorer.list_offices()
result = await explorer.get_company_monthly_costs(1, month=1, year=2026)
result = await explorer.get_building_finance(month=1, year=2026)

# Lưu output dài vào JSON file
result = await explorer.get_building_finance_details(
    month=1, year=2026, save_to="finance_details.json"
)

# Generic call cho bất kỳ endpoint
result = await explorer.call_api("GET", "/offices/1")
result = await explorer.call_api("POST", "/offices", json_body={"name": "P101", ...})

# Dump ALL reports vào JSON
await explorer.dump_all_reports(month=1, year=2026)

await explorer.close()
```

Hoặc dùng standalone functions:

```python
from auto_test.api.api_utils import (
    list_offices, get_office, create_office, update_office, delete_office,
    list_companies, get_company, get_company_monthly_costs,
    get_company_service_details, list_contracts,
    list_building_employees, get_employee_salaries,
    get_building_finance, get_building_finance_details,
)

result = await get_company_monthly_costs(1, month=1, year=2026)
# result = {"status": 200, "data": {...}, "success": True, "url": "..."}
```

### SQL Debug

```python
from auto_test.sql.db_utils import DatabaseUtils, quick_query

# Quick one-off query
rows = await quick_query("SELECT * FROM offices WHERE floor = $1", 1)

# Full database utils
db = DatabaseUtils()
await db.connect()
result = await db.fetchone("SELECT * FROM companies WHERE id = $1", 1)
tables = await db.get_table_names()
await db.close()
```

### Lưu ý
- Output JSON files được lưu vào `back_end/auto_test/output/`
- Mỗi API function trả về dict: `{"status", "data", "success", "url"}`
- Parameter `save_to` chấp nhận relative path (từ output dir) hoặc absolute path
- `verbose=False` để tắt print khi không cần xem output

## Quy tắc khác
- **KHÔNG tự xóa file**: Hỏi trước khi xóa
- **Import ở đầu file**: Không import trong hàm
- **Docs**: Chỉ tạo khi được yêu cầu (`docs/` - không commit)
- **Ngôn ngữ**: Tiếng Việt cho errors/API docs, Tiếng Anh cho code comments

## Tools & Skills

### Frontend Development (ReactJS)
Khi code frontend, dùng UI/UX skill:
```
/ui-ux-pro-max Build a landing page for my SaaS product
```
Supported: Kiro, GitHub Copilot, Roo Code

### Search & Research
- **Context7 MCP**: Fetch docs mới nhất từ libraries (React, FastAPI, PostgreSQL, etc.)
- **StackOverflow MCP**: Search câu hỏi/answers từ StackOverflow
- **Web Search for Copilot**: Search web cho thông tin cập nhật
- **MCP Serena**: Symbolic search trong codebase (token-efficient)
