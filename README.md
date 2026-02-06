# Hệ thống Quản lý Tòa nhà Văn phòng

**Sinh viên**: Trần Quý Đạt — PTIT  
**Đề tài 7**: Xây dựng Hệ CSDL quản lý một Tòa nhà văn phòng

---

## Đề bài tóm tắt

Xây dựng hệ CSDL quản lý Tòa nhà văn phòng cho thuê, bao gồm:

- Quản lý văn phòng, công ty thuê, nhân viên tòa nhà, nhân viên công ty, dịch vụ.
- Một công ty thuê nhiều văn phòng; mỗi văn phòng chỉ do tối đa 1 công ty thuê tại một thời điểm.
- Dịch vụ (vệ sinh, ăn uống, gửi xe, bảo vệ, bảo trì): đơn giá tỉ lệ theo số người/diện tích, tính theo tháng hoặc theo ngày.
- Lương nhân viên tòa nhà tỉ lệ thuận với doanh thu dịch vụ họ phụ trách.
- CRUD, liệt kê chi phí công ty, chi tiết dịch vụ, lương nhân viên, tổng thu chi tòa nhà.

---

## Kiến trúc tổng quan

```text
┌──────────────┐    HTTP    ┌──────────────┐    SQL     ┌────────────┐
│   Frontend   │ ────────── │   Backend    │ ────────── │ PostgreSQL │
│  React/Vite  │  :5173     │   FastAPI    │  :8222     │   17.7     │
└──────────────┘            └──────────────┘            └────────────┘
```

| Thành phần | Công nghệ |
| ---------- | --------- |
| Frontend | React 19, Vite 7, Tailwind CSS v4, Axios, Lucide React |
| Backend | FastAPI, asyncpg (100% raw SQL, không ORM) |
| Database | PostgreSQL 17, 12 bảng, chuẩn hóa BCNF |
| Testing | 129 tests (31 SQL + 98 API) — 100% pass |

---

## Cấu trúc thư mục

```text
SQL_MASTER/
├── README.md                 # File này
├── back_end/
│   ├── api/                  # FastAPI app (routes, services, repositories, models)
│   ├── migrations/           # SQL schema + sample data
│   ├── auto_test/            # Test suites (SQL + API)
│   ├── requirements.txt
│   └── .env
├── front_end/
│   ├── src/                  # React app (pages, components, api, utils)
│   ├── vite.config.js
│   └── package.json
├── task/                     # Tài liệu chi tiết hệ thống
│   ├── overall/README.md     # Tổng quan: đề bài, kiến trúc, schema, business logic
│   ├── be/README.md          # Chi tiết backend: API, DB schema, code structure
│   └── fe/README.md          # Chi tiết frontend: pages, design system, components
└── test/
    ├── frontend/REPORT.md    # Báo cáo kiểm thử frontend
    └── backend/REPORT.md     # Báo cáo kiểm thử backend
```

---

## Cài đặt

### Yêu cầu

- Python 3.11+ (khuyến nghị dùng Conda)
- Node.js 18+
- PostgreSQL 15+

### 1. Database

```bash
# Tạo database và nạp dữ liệu mẫu
cd back_end
conda run -n sql python auto_test/script/setup_db.py
```

Hoặc thủ công:

```sql
CREATE DATABASE office_db;
```

```bash
psql -U postgres -d office_db -f migrations/001_initial_schema.sql
psql -U postgres -d office_db -f migrations/002_sample_data.sql
```

### 2. Backend

```bash
cd back_end

# Cài dependencies
pip install -r requirements.txt

# Cấu hình .env (copy từ .env.example)
cp .env.example .env
# Sửa thông tin DB trong .env nếu cần

# Chạy server
uvicorn api.main:app --host 0.0.0.0 --port 8222 --reload
```

Server chạy tại `http://localhost:8222`. API docs: `http://localhost:8222/docs`.

### 3. Frontend

```bash
cd front_end

# Cài dependencies
npm install

# Chạy dev server
npm run dev
```

Frontend chạy tại `http://localhost:5173`.

---

## Chạy Tests

```bash
cd back_end

# SQL Tests (31 tests) — kiểm tra schema, constraints, CRUD
conda run -n sql python auto_test/sql/test_sql.py

# API Tests (98 tests) — cần server đang chạy
conda run -n sql python auto_test/api/test_api.py
```

---

## API chính

| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| GET | `/api/offices` | Danh sách văn phòng |
| POST | `/api/offices` | Tạo văn phòng |
| GET | `/api/companies` | Danh sách công ty |
| POST | `/api/companies` | Tạo công ty |
| GET | `/api/companies/{id}/monthly-costs` | Chi phí tháng của công ty |
| GET | `/api/companies/{id}/service-details` | Chi tiết dịch vụ công ty |
| GET | `/api/building-employees/salaries/monthly` | Lương nhân viên tòa nhà |
| GET | `/api/reports/building-finance` | Tổng thu chi tòa nhà |
| GET | `/api/reports/building-finance/details` | Chi tiết các khoản thu chi |

Full API docs: `http://localhost:8222/docs` (Swagger UI)

---

## Database Schema (12 bảng)

| Bảng | Mô tả |
| ---- | ----- |
| offices | Văn phòng cho thuê |
| companies | Công ty khách thuê |
| company_employees | Nhân viên công ty |
| building_employees | Nhân viên tòa nhà |
| rent_contracts | Hợp đồng thuê |
| services | Dịch vụ (vệ sinh, ăn uống, an ninh...) |
| salary_rules | Quy tắc tính lương (bonus_rate) |
| service_role_rules | Phân công vai trò theo dịch vụ (BCNF) |
| service_subscribers | Nhân viên phụ trách dịch vụ (BCNF) |
| company_monthly_usages | Dịch vụ theo tháng |
| employee_daily_usages | Dịch vụ theo ngày (ăn uống, gửi xe) |
| invoices | Hóa đơn |

---

## Dữ liệu mẫu

- 6 văn phòng (P101–P302)
- 3 công ty (TNHH Công Nghệ ABC, Cổ Phần XYZ, Startup Innovation)
- 5 nhân viên tòa nhà
- Dữ liệu đầy đủ cho 2 tháng
