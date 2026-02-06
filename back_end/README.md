# Backend - Hệ thống Quản lý Tòa nhà Văn phòng

FastAPI + PostgreSQL — **100% Raw SQL** (asyncpg, không ORM)

---

## Cài đặt

```bash
cd back_end
pip install -r requirements.txt
cp .env.example .env   # Sửa thông tin DB nếu cần
```

## Chạy Server

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8222 --reload
```

- API docs: http://localhost:8222/docs
- Health check: http://localhost:8222/health

---

## Cấu trúc

```text
back_end/
├── api/
│   ├── main.py              # FastAPI app + lifespan
│   ├── config.py            # Settings từ .env
│   ├── database/            # Connection pool (asyncpg)
│   ├── models/              # Pydantic schemas
│   ├── repositories/        # SQL queries (raw SQL)
│   ├── services/            # Business logic
│   └── routes/              # API endpoints
├── migrations/
│   ├── 001_initial_schema.sql
│   └── 002_sample_data.sql
├── auto_test/
│   ├── api/test_api.py      # 98 API tests
│   ├── sql/test_sql.py      # 31 SQL tests
│   └── script/              # DB management scripts
├── requirements.txt
└── .env
```

**Pattern**: Routes → Services → Repositories → Database (SQL thuần)

---

## API Endpoints

### CRUD
| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| GET/POST | `/api/offices` | List / Tạo văn phòng |
| GET/PUT/DELETE | `/api/offices/{id}` | Chi tiết / Sửa / Xóa |
| GET/POST | `/api/companies` | List / Tạo công ty |
| GET/PUT/DELETE | `/api/companies/{id}` | Chi tiết / Sửa / Xóa |
| GET | `/api/contracts` | Danh sách hợp đồng |
| GET | `/api/building-employees` | Danh sách nhân viên tòa nhà |

### Báo cáo nghiệp vụ
| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| GET | `/api/companies/{id}/monthly-costs?month=&year=` | Chi phí tháng công ty |
| GET | `/api/companies/{id}/service-details?month=&year=` | Chi tiết dịch vụ công ty |
| GET | `/api/building-employees/salaries/monthly?month=&year=` | Lương nhân viên |
| GET | `/api/reports/building-finance?month=&year=` | Tổng thu chi tòa nhà |
| GET | `/api/reports/building-finance/details?month=&year=` | Chi tiết các khoản thu chi |

---

## Database Scripts

```bash
cd back_end

# Setup mới (tạo DB + schema + data)
conda run -n sql python auto_test/script/setup_db.py

# Reset (xóa + tạo lại)
conda run -n sql python auto_test/script/reset_db.py

# Xóa data, giữ schema
conda run -n sql python auto_test/script/truncate_all.py
```

---

## Tests

```bash
# SQL Tests (31 tests)
conda run -n sql python auto_test/sql/test_sql.py

# API Tests (98 tests) — server phải đang chạy
conda run -n sql python auto_test/api/test_api.py
```

**Kết quả**: 129/129 tests passed (100%)

---

## Công thức tính lương

```text
total_salary = base_salary + (monthly_revenue × bonus_rate)
```

JOIN: building_employees → service_subscribers → service_role_rules → salary_rules

---

## Tech Stack

| Component | Version |
| --------- | ------- |
| FastAPI | 0.128+ |
| asyncpg | 0.31+ |
| PostgreSQL | 17 |
| Pydantic | 2.12+ |
| Uvicorn | 0.32+ |
