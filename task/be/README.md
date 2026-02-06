# Chi tiết Backend — Quản lý Tòa nhà Văn phòng

**Stack**: FastAPI + PostgreSQL + asyncpg (100% raw SQL, không ORM)  
**Server**: http://localhost:8222  
**API docs**: http://localhost:8222/docs (Swagger UI)

---

## 1. Kiến trúc code

```text
Request → Routes (HTTP) → Services (Logic) → Repositories (SQL) → PostgreSQL
```

### Cấu trúc chi tiết

```text
back_end/
├── api/
│   ├── main.py                  # FastAPI app, lifespan (init/close pool)
│   ├── config.py                # Pydantic Settings từ .env
│   ├── database/
│   │   ├── connection.py        # asyncpg pool (create, get, close)
│   │   └── transaction.py       # @asynccontextmanager transaction
│   ├── models/                  # Pydantic schemas (14 files)
│   │   ├── office.py            # OfficeCreate, OfficeUpdate, OfficeResponse
│   │   ├── company.py           # CompanyCreate, CompanyUpdate, CompanyResponse
│   │   ├── rent_contract.py     # ContractCreate, ContractResponse
│   │   ├── building_employee.py # EmployeeResponse, SalaryResponse
│   │   ├── invoice.py
│   │   ├── service.py
│   │   ├── salary_rule.py
│   │   ├── service_role_rule.py
│   │   ├── service_subscriber.py
│   │   ├── company_employee.py
│   │   ├── company_monthly_usage.py
│   │   └── employee_daily_usage.py
│   ├── repositories/            # Raw SQL queries
│   │   ├── office_repository.py
│   │   ├── company_repository.py
│   │   ├── rent_contract_repository.py
│   │   └── building_employee_repository.py
│   ├── services/                # Business logic
│   │   ├── office_service.py
│   │   ├── company_service.py
│   │   ├── rent_contract_service.py
│   │   └── building_employee_service.py
│   └── routes/                  # API endpoints
│       ├── office_routes.py
│       ├── company_routes.py
│       ├── rent_contract_routes.py
│       ├── building_employee_routes.py
│       └── report_routes.py
├── migrations/
│   ├── 001_initial_schema.sql   # CREATE TABLE 12 bảng + constraints
│   └── 002_sample_data.sql      # INSERT dữ liệu mẫu 2 tháng
├── auto_test/
│   ├── api/
│   │   ├── test_api.py          # 98 API tests
│   │   └── api_utils.py         # Helper functions cho test
│   ├── sql/
│   │   ├── test_sql.py          # 31 SQL tests
│   │   └── db_utils.py          # DB connection helper
│   └── script/
│       ├── setup_db.py          # Tạo DB + schema + data
│       ├── reset_db.py          # Drop + tạo lại
│       ├── truncate_all.py      # Xóa data, giữ schema
│       ├── run_migrations.py    # Chạy SQL migrations
│       └── test_connection.py   # Test kết nối DB
├── requirements.txt
├── .env / .env.example
└── start_server.sh
```

---

## 2. Database Schema — 12 bảng

### offices

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(50) | NOT NULL |
| area | NUMERIC(10,2) | NOT NULL |
| floor | INTEGER | NOT NULL |
| position | VARCHAR(100) | — |
| base_price | NUMERIC(15,2) | NOT NULL |

### companies

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| tax_code | VARCHAR(50) | UNIQUE NOT NULL |
| email | VARCHAR(100) | — |
| address | VARCHAR(255) | — |

### rent_contracts

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| office_id | INTEGER | FK → offices.id, NOT NULL |
| company_id | INTEGER | FK → companies.id, NOT NULL |
| invoice_id | INTEGER | FK → invoices.id |
| from_date | DATE | NOT NULL |
| end_date | DATE | NOT NULL |
| signed_date | DATE | DEFAULT CURRENT_DATE |
| rent_price | NUMERIC(15,2) | NOT NULL |
| status | VARCHAR(20) | DEFAULT 'active' |

### building_employees

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| employee_id | SERIAL | PRIMARY KEY |
| first_name | VARCHAR(50) | — |
| last_name | VARCHAR(50) | — |
| phone_number | VARCHAR(20) | — |
| role | VARCHAR(50) | NOT NULL |
| email | VARCHAR(100) | — |
| address | VARCHAR(255) | — |
| date_of_birth | DATE | — |
| base_salary | NUMERIC(15,2) | — |
| hire_date | DATE | — |
| status | VARCHAR(20) | — |

### company_employees

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| company_id | INTEGER | FK → companies.id, NOT NULL |
| full_name | VARCHAR(100) | NOT NULL |
| job_title | VARCHAR(100) | — |
| phone_number | VARCHAR(20) | — |
| email | VARCHAR(100) | — |
| status | VARCHAR(20) | DEFAULT 'working' |

### services

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(100) | NOT NULL |
| description | TEXT | — |
| base_price | NUMERIC(15,2) | — |
| price_method | VARCHAR(50) | per_sqm, per_head, fixed |

### salary_rules

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| bonus_rate | FLOAT | — |
| status | VARCHAR(20) | — |

### service_role_rules (BCNF)

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| service_id | INTEGER | FK → services.id, NOT NULL |
| role | VARCHAR(50) | NOT NULL |
| salary_rule_id | INTEGER | FK → salary_rules.id, NOT NULL |

### service_subscribers (BCNF)

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| service_id | INTEGER | NOT NULL |
| employee_id | INTEGER | FK → building_employees.employee_id, NOT NULL |
| service_role_rules_id | INTEGER | FK → service_role_rules.id, NOT NULL |
| from_date | DATE | NOT NULL |
| end_date | DATE | — |
| invoice_id | INTEGER | FK → invoices.id |

### company_monthly_usages

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| company_id | INTEGER | FK → companies.id, NOT NULL |
| service_id | INTEGER | FK → services.id, NOT NULL |
| invoice_id | INTEGER | FK → invoices.id |
| from_date | DATE | — |
| to_date | DATE | — |
| quantity | INTEGER | — |
| price | NUMERIC(15,2) | — |

### employee_daily_usages

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| employee_id | INTEGER | FK → company_employees.id, NOT NULL |
| invoice_id | INTEGER | FK → invoices.id |
| service_id | INTEGER | FK → services.id, NOT NULL |
| usage_date | DATE | NOT NULL |
| price | NUMERIC(15,2) | — |
| service_type | VARCHAR(50) | — |

### invoices

| Cột | Kiểu | Ràng buộc |
| --- | ---- | --------- |
| id | SERIAL | PRIMARY KEY |
| created_date | DATE | DEFAULT CURRENT_DATE |
| pay_day | DATE | — |
| from_date | DATE | — |
| to_date | DATE | — |
| total_amount | NUMERIC(15,2) | — |
| status | VARCHAR(20) | DEFAULT 'unpaid' |
| note | TEXT | — |

---

## 3. API Endpoints chi tiết

### Offices

```text
GET    /api/offices                  → List (hỗ trợ ?limit=&offset=)
POST   /api/offices                  → Create (body: name, area, floor, position, base_price)
GET    /api/offices/{id}             → Get by ID
PUT    /api/offices/{id}             → Update (partial)
DELETE /api/offices/{id}             → Delete
```

### Companies

```text
GET    /api/companies                → List
POST   /api/companies                → Create (body: name, tax_code, email, address)
GET    /api/companies/{id}           → Get by ID
PUT    /api/companies/{id}           → Update (partial)
DELETE /api/companies/{id}           → Delete
GET    /api/companies/{id}/monthly-costs?month=1&year=2026
       → Chi phí tháng: rent_cost + service_costs[] + total_cost
GET    /api/companies/{id}/service-details?month=1&year=2026
       → Chi tiết: monthly_services[], daily_services[], total_service_cost
```

### Contracts

```text
GET    /api/contracts                → List hợp đồng
```

### Building Employees

```text
GET    /api/building-employees       → List nhân viên tòa nhà
GET    /api/building-employees/salaries/monthly?month=1&year=2026
       → employee_id, full_name, role, base_salary, bonus_rate, monthly_revenue, total_salary
```

### Reports

```text
GET    /api/reports/building-finance?month=1&year=2026
       → total_revenue, revenue_breakdown{rent, services}, total_expense, net_profit
GET    /api/reports/building-finance/details?month=1&year=2026
       → revenue_details[], expense_details[]
```

---

## 4. Business Logic

### Tính lương nhân viên tòa nhà

```text
total_salary = base_salary + (monthly_revenue × bonus_rate)
```

**JOIN path**: building_employees → service_subscribers → service_role_rules → salary_rules

- `monthly_revenue`: SUM doanh thu dịch vụ mà nhân viên phụ trách trong tháng.
- Mỗi tháng nhân viên có thể đổi vị trí/bậc → query theo `from_date` / `end_date` của `service_subscribers`.

### Tính giá dịch vụ vệ sinh

```text
Nếu company có < 10 người VÀ tổng diện tích ≤ 100m²:
  → giá = base_price

Ngược lại:
  surcharge = MAX(ceil((số_người - 10) / 5), ceil((diện_tích - 100) / 10))
  → giá = base_price × (1 + surcharge × 0.05)

Không dùng hết tháng:
  → giá × (số_ngày_sử_dụng / tổng_ngày_tháng)
```

### Chi phí công ty tháng

```text
total_cost = rent_cost + total_service_cost
  rent_cost = SUM(rent_price) từ rent_contracts đang active
  total_service_cost = SUM(monthly_services) + SUM(daily_services)
```

### Validation & Constraints

- **Overlap check**: Mỗi văn phòng tại 1 thời điểm chỉ 1 công ty thuê.
- **Tax code unique**: companies.tax_code UNIQUE.
- **Status**: hợp đồng (`active`/`expired`/`terminated`), nhân viên (`working`/`resigned`), hóa đơn (`paid`/`unpaid`/`overdue`).
- **Error handling**: 404 (not found), 422 (validation error), 400 (bad request).

---

## 5. Kết quả kiểm thử

### SQL Tests — 31/31 PASS

- Kết nối DB, kiểm tra 12 bảng tồn tại.
- Sample data loaded.
- CRUD operations.
- UNIQUE constraint (tax_code).
- Foreign key constraints.
- Date range constraints.
- Tính lương, tính chi phí.

### API Tests — 98/98 PASS

- Health check.
- CRUD: Offices (5), Companies (5), Contracts, Employees.
- Monthly costs, service details.
- Salary calculation.
- Building finance + details.
- Pagination (?limit=).
- Error handling: 404, 422.

**Tổng BE**: 129/129 tests — 100% PASS.

Chi tiết: `test/backend/REPORT.md`

---

## 6. Cài đặt & Chạy

```bash
cd back_end

# 1. Dependencies
pip install -r requirements.txt

# 2. Database
conda run -n sql python auto_test/script/setup_db.py

# 3. Server (auto-reload)
uvicorn api.main:app --host 0.0.0.0 --port 8222 --reload
```

### Biến môi trường (.env)

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=datsql09
POSTGRES_DB=office_db
APP_PORT=8222
```

### Requirements

```text
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
asyncpg>=0.30.0
pydantic[email]>=2.10.0
pydantic-settings>=2.7.0
python-dotenv>=1.0.0
httpx>=0.28.0 (test)
```

---

## 7. Lưu ý kỹ thuật

- **100% raw SQL**: Tất cả queries viết bằng SQL thuần qua asyncpg. Không dùng SQLAlchemy, Tortoise, hay bất kỳ ORM nào.
- **Async/Await**: Toàn bộ codebase dùng async. Connection pool quản lý kết nối tự động.
- **Transaction thủ công**: `async with conn.transaction():` — BEGIN/COMMIT/ROLLBACK tự động.
- **Parameterized queries**: Dùng `$1, $2...` để tránh SQL injection.
- **CORS**: Middleware cho phép `localhost:5173` và `localhost:5174`.
- **Auto-reload**: `uvicorn --reload` — server tự restart khi code thay đổi, không cần stop/start lại.
