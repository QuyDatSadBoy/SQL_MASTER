# Tổng quan Hệ thống — Quản lý Tòa nhà Văn phòng

**Sinh viên**: Trần Quý Đạt — PTIT  
**Đề tài 7**: Xây dựng Hệ CSDL quản lý một Tòa nhà văn phòng

---

## 1. Đề bài đầy đủ

### Yêu cầu về CSDL

- Thông tin về các công ty thuê văn phòng, các văn phòng cho thuê, nhân viên tòa nhà, nhân viên công ty, các dịch vụ trong tòa nhà.
- Tòa nhà chia nhỏ thành nhiều văn phòng với vị trí và diện tích khác nhau; giá thuê phụ thuộc vào vị trí và diện tích.
- Một công ty có thể thuê nhiều văn phòng, mỗi văn phòng tại một thời điểm chỉ do tối đa 1 công ty thuê. Tổng diện tích thuê = tổng diện tích các văn phòng của công ty đó.
- **Dịch vụ theo tháng** (vệ sinh, bảo vệ, bảo trì): đơn giá tỉ lệ số người và/hoặc diện tích.
  - Ví dụ dịch vụ vệ sinh: dưới 10 người & ≤ 100m² = mức giá cơ bản; cứ thêm 5 người hoặc 10m² → +5%.
  - Không dùng hết tháng: tính tỉ lệ ngày đã sử dụng / tổng ngày trong tháng.
- **Dịch vụ theo ngày** (ăn uống, gửi xe): tính theo số nhân viên từng công ty, từng ngày. Dữ liệu phải nhập đầy đủ.
- **Nhân viên tòa nhà**: phân cấp quản lý và nhân viên dịch vụ. Lương tỉ lệ thuận với doanh thu từng loại dịch vụ.
- Dữ liệu mẫu phải có ít nhất 2 tháng.

### Yêu cầu về ứng dụng

1. CRUD: công ty, nhân viên công ty, nhân viên tòa nhà, dịch vụ, văn phòng, hợp đồng.
2. Liệt kê công ty + chi phí tháng (tiền thuê + tiền dịch vụ từng loại), sắp xếp.
3. Chi tiết chi phí dịch vụ từng công ty, giá tiền từng lần sử dụng.
4. Lương nhân viên tòa nhà theo tháng (có thể đổi vị trí/bậc mỗi tháng).
5. Tổng thu + tổng chi toàn tòa nhà; chi tiết các khoản thu/chi.
6. Ràng buộc số lượng bản ghi thể hiện trong ứng dụng.

---

## 2. Kiến trúc hệ thống

```text
┌──────────────┐    HTTP     ┌──────────────┐    SQL      ┌────────────┐
│   Frontend   │ ─────────── │   Backend    │ ─────────── │ PostgreSQL │
│  React/Vite  │  port 5173  │   FastAPI    │  port 8222  │    17.7    │
└──────────────┘             └──────────────┘             └────────────┘
```

| Thành phần | Công nghệ |
| ---------- | --------- |
| Frontend | React 19, Vite 7, Tailwind CSS v4, Axios, React Router v7, Lucide React |
| Backend | FastAPI, asyncpg (**100% raw SQL**, không ORM), Pydantic v2 |
| Database | PostgreSQL 17.7, 12 bảng, chuẩn hóa BCNF |
| Testing | 129 tests tổng (31 SQL + 98 API), 6 trang FE auto-test qua Chrome |

---

## 3. Cấu trúc thư mục

```text
SQL_MASTER/
├── README.md               # Tổng quan + hướng dẫn cài đặt
├── back_end/
│   ├── api/                # FastAPI app
│   │   ├── main.py         # App entry + lifespan (pool init)
│   │   ├── config.py       # Settings (.env)
│   │   ├── database/       # connection.py, transaction.py
│   │   ├── models/         # Pydantic schemas (14 models)
│   │   ├── repositories/   # Raw SQL queries (4 repos)
│   │   ├── services/       # Business logic (4 services)
│   │   └── routes/         # Endpoints (5 route files)
│   ├── migrations/
│   │   ├── 001_initial_schema.sql   # 12 bảng
│   │   └── 002_sample_data.sql      # Dữ liệu mẫu 2 tháng
│   ├── auto_test/
│   │   ├── api/            # 98 API tests
│   │   ├── sql/            # 31 SQL tests
│   │   └── script/         # setup_db, reset_db, truncate_all
│   ├── requirements.txt
│   └── .env
├── front_end/
│   ├── src/
│   │   ├── App.jsx         # Router (6 routes)
│   │   ├── index.css       # Tailwind v4 + theme colors
│   │   ├── api/client.js   # Axios client (tất cả endpoints)
│   │   ├── components/     # Layout.jsx, Navbar.jsx
│   │   ├── pages/          # 6 trang (Dashboard, Offices, Companies, Costs, Salaries, Reports)
│   │   └── utils/          # formatters.js (VND, ngày, số)
│   ├── vite.config.js
│   └── package.json
├── task/
│   ├── overall/README.md   # File này — tổng quan hệ thống
│   ├── be/README.md        # Chi tiết backend
│   └── fe/README.md        # Chi tiết frontend
└── test/
    ├── frontend/REPORT.md  # Báo cáo kiểm thử FE (6 trang, screenshots)
    └── backend/REPORT.md   # Báo cáo kiểm thử BE (98 tests)
```

---

## 4. Database Schema — 12 bảng

| # | Bảng | Mô tả | Quan hệ chính |
| - | ---- | ----- | ------------- |
| 1 | offices | Văn phòng cho thuê | — |
| 2 | companies | Công ty khách thuê | — |
| 3 | company_employees | Nhân viên công ty | → companies |
| 4 | building_employees | Nhân viên tòa nhà | — |
| 5 | rent_contracts | Hợp đồng thuê | → offices, companies, invoices |
| 6 | services | Dịch vụ | — |
| 7 | salary_rules | Quy tắc lương (bonus_rate) | — |
| 8 | service_role_rules | Vai trò + dịch vụ → quy tắc lương (BCNF) | → services, salary_rules |
| 9 | service_subscribers | Nhân viên phụ trách dịch vụ (BCNF) | → building_employees, service_role_rules |
| 10 | company_monthly_usages | Sử dụng dịch vụ theo tháng | → companies, services, invoices |
| 11 | employee_daily_usages | Sử dụng dịch vụ theo ngày | → company_employees, services, invoices |
| 12 | invoices | Hóa đơn | — |

### Chuẩn hóa BCNF

- `service_role_rules`: tách quan hệ (service + role → salary_rule) để tránh phụ thuộc bắc cầu.
- `service_subscribers`: tách quan hệ (employee + service → rule + thời gian) để đảm bảo BCNF.

---

## 5. API Endpoints

### CRUD cơ bản

| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| GET/POST | /api/offices | Danh sách / Tạo văn phòng |
| GET/PUT/DELETE | /api/offices/{id} | Chi tiết / Sửa / Xóa |
| GET/POST | /api/companies | Danh sách / Tạo công ty |
| GET/PUT/DELETE | /api/companies/{id} | Chi tiết / Sửa / Xóa |
| GET | /api/contracts | Danh sách hợp đồng |
| GET | /api/building-employees | Danh sách nhân viên tòa nhà |

### Báo cáo nghiệp vụ (đáp ứng yêu cầu đề bài)

| # | Endpoint | Yêu cầu đề bài |
| - | -------- | -------------- |
| 1 | GET /api/companies/{id}/monthly-costs?month=&year= | Liệt kê chi phí tháng (thuê + dịch vụ) |
| 2 | GET /api/companies/{id}/service-details?month=&year= | Chi tiết dịch vụ từng công ty |
| 3 | GET /api/building-employees/salaries/monthly?month=&year= | Lương nhân viên tòa nhà |
| 4 | GET /api/reports/building-finance?month=&year= | Tổng thu + tổng chi toàn tòa nhà |
| 5 | GET /api/reports/building-finance/details?month=&year= | Chi tiết khoản thu/chi |

---

## 6. Business Logic quan trọng

### Công thức tính lương nhân viên tòa nhà

```text
total_salary = base_salary + (monthly_revenue × bonus_rate)
```

- `base_salary`: lương cơ bản theo nhân viên.
- `monthly_revenue`: doanh thu dịch vụ mà nhân viên phụ trách trong tháng.
- `bonus_rate`: tỉ lệ thưởng theo quy tắc (bảng `salary_rules`).
- JOIN path: `building_employees` → `service_subscribers` → `service_role_rules` → `salary_rules`.

### Tính giá dịch vụ vệ sinh

- Dưới 10 người + ≤ 100m²: giá cơ bản (`base_price`).
- Cứ thêm 5 người hoặc vượt 10m²: +5% giá.
- Không dùng hết tháng: tỉ lệ = số ngày sử dụng / tổng ngày tháng.

### Ràng buộc thuê văn phòng

- Check overlap dates: mỗi văn phòng tại 1 thời điểm chỉ 1 công ty thuê.
- Status hợp đồng: `active`, `expired`, `terminated`.

---

## 7. Dữ liệu mẫu

| Đối tượng | Số lượng | Chi tiết |
| --------- | -------- | -------- |
| Văn phòng | 6 | P101, P102, P201, P202, P301, P302 |
| Công ty | 3 | TNHH Công Nghệ ABC, Cổ Phần XYZ, Startup Innovation |
| Nhân viên tòa nhà | 5 | Nguyễn Minh, Trần Hương, Lê Bình, Phạm Cường, Hoàng Lan |
| Nhân viên công ty | 28+ | Phân bố đều 3 công ty |
| Dịch vụ | 5 | Vệ sinh, Ăn uống, Gửi xe, An ninh, Bảo trì |
| Dữ liệu tháng | 2 | Tháng 1 + 2 / 2026 |

---

## 8. Kết quả kiểm thử

| Loại test | Số test | Kết quả |
| --------- | ------- | ------- |
| SQL (schema, constraints, CRUD) | 31 | 31/31 PASS |
| API (endpoints, validation, business logic) | 98 | 98/98 PASS |
| Frontend (6 trang, Chrome auto-test) | 6 | 6/6 PASS |
| **Tổng** | **135** | **135/135 PASS** |

Chi tiết xem tại:
- `test/backend/REPORT.md` — báo cáo BE
- `test/frontend/REPORT.md` — báo cáo FE (có screenshots)

---

## 9. Mapping đề bài → Implementation

| Yêu cầu đề bài | Cách thực hiện |
| -------------- | ------------- |
| CRUD các đối tượng | 5 route files, 4 repositories, REST API chuẩn |
| Chi phí công ty theo tháng | `GET /companies/{id}/monthly-costs` → trang Chi phí |
| Chi tiết dịch vụ từng công ty | `GET /companies/{id}/service-details` → trang Chi phí |
| Lương nhân viên theo tháng | `GET /building-employees/salaries/monthly` → trang Lương |
| Tổng thu chi tòa nhà | `GET /reports/building-finance` → trang Báo cáo |
| Chi tiết khoản thu/chi | `GET /reports/building-finance/details` → trang Báo cáo |
| 100% SQL thuần | asyncpg raw queries, không ORM |
| BCNF | service_role_rules + service_subscribers |
| Dữ liệu 2 tháng | migrations/002_sample_data.sql |
| Ràng buộc bản ghi | Validation + constraints trong DB + API |

---

## 10. Hướng dẫn cài đặt nhanh

```bash
# 1. Database
cd back_end
conda run -n sql python auto_test/script/setup_db.py

# 2. Backend
pip install -r requirements.txt
uvicorn api.main:app --host 0.0.0.0 --port 8222 --reload

# 3. Frontend
cd ../front_end
npm install
npm run dev
```

Truy cập: `http://localhost:5173`
