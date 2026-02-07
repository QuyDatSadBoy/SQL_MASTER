# Kiểm tra đề bài — Đề tài 7: Xây dựng Hệ CSDL quản lý Toà nhà văn phòng

Đối chiếu từng yêu cầu của đề bài với hiện trạng web (CSDL, backend API, frontend).

---

## A. Yêu cầu tối thiểu về CSDL

| # | Yêu cầu | Trạng thái | Ghi chú |
|---|--------|------------|--------|
| 1 | Thông tin: công ty thuê, văn phòng cho thuê, nhân viên tòa nhà, nhân viên công ty thuê, dịch vụ trong tòa nhà | ✅ Đủ | Bảng: `companies`, `offices`, `building_employees`, `company_employees`, `services` (+ bảng liên kết). |
| 2 | Tòa nhà chia nhỏ thành văn phòng; vị trí, diện tích khác nhau; giá thuê phụ thuộc vị trí và diện tích | ✅ Đủ | `offices`: `area`, `floor`, `position`, `base_price`. `rent_contracts`: `rent_price` theo từng hợp đồng. |
| 3 | Một công ty có thể thuê nhiều văn phòng; mỗi văn phòng tại một thời điểm tối đa 1 công ty thuê | ✅ Đủ | Nhiều `rent_contracts` cùng `company_id`; ràng buộc “1 văn phòng 1 công ty” được kiểm tra trong ứng dụng khi tạo/sửa hợp đồng (`check_availability`). |
| 4 | Tổng diện tích thuê của công ty = tổng diện tích các văn phòng công ty đó thuê | ✅ Đủ | Có thể tính từ `rent_contracts` JOIN `offices` (SUM(area)). API `get_monthly_costs` trả `total_area`. |
| 5 | Dịch vụ: vệ sinh, ăn uống, trông giữ xe, bảo vệ/an ninh, bảo trì thiết bị...; công ty không nhất thiết dùng hết | ✅ Đủ | Bảng `services`; `company_monthly_usages`, `employee_daily_usages` theo công ty/dịch vụ. |
| 6 | Một số dịch vụ đơn giá tỉ lệ người và/hoặc diện tích (vd: vệ sinh: &lt;10 người và ≤100 m² cùng giá, +5 người hoặc +10 m² thì +5%) | ⚠️ Một phần | CSDL lưu `base_price`, `price_method` (per_sqm, per_head, fixed). Sample data lưu giá đã tính trong `company_monthly_usages`. **Chưa** có procedure/function tự động tính đơn giá theo đúng công thức đề bài (10 người, 100 m², +5%). |
| 7 | Tiền dịch vụ theo tháng; không dùng hết tháng thì tính theo tỉ lệ ngày đã dùng / tổng ngày tháng | ⚠️ Một phần | Dữ liệu lưu theo tháng (`from_date`, `to_date`, `price`). **Chưa** thấy logic tính prorate (tỉ lệ ngày) trong code khi tính tiền. |
| 8 | Dịch vụ ăn uống, gửi xe: tính theo số nhân viên công ty sử dụng theo từng ngày; nhập đầy đủ theo ngày | ✅ Đủ | Bảng `employee_daily_usages` (employee_id, service_id, usage_date, price); sample data có gửi xe, ăn trưa theo ngày. |
| 9 | Nhân viên không nhất thiết dùng ăn uống/gửi xe mọi ngày | ✅ Đủ | Dữ liệu theo từng `usage_date`; một nhân viên có thể có hoặc không có bản ghi từng ngày. |
| 10 | Nhân viên tòa nhà cung cấp/giám sát dịch vụ; phân cấp quản lý và nhân viên dịch vụ | ✅ Đủ | `building_employees.role`; `service_subscribers` gắn nhân viên với dịch vụ và `service_role_rules` (manager/supervisor/staff). |
| 11 | Lương nhân viên theo vị trí và theo từng loại dịch vụ; tỉ lệ thuận doanh thu dịch vụ; học viên tự nghĩ cách tính | ✅ Đủ | `salary_rules` (bonus_rate), `service_role_rules` (service_id, role, salary_rule_id); repository `get_salaries`: base_salary + (doanh thu dịch vụ × bonus_rate). |
| 12 | Dữ liệu đầy đủ cho ít nhất 2 tháng | ✅ Đủ | Sample data: 12/2025, 01/2026, 02/2026 (≥ 2 tháng). |

---

## B. Yêu cầu tối thiểu về ứng dụng

### B1. Chức năng thêm/xoá/sửa/tìm kiếm (CRUD) với ràng buộc

| Đối tượng | Backend API | Frontend trang CRUD | Ràng buộc thể hiện |
|-----------|-------------|----------------------|---------------------|
| Công ty | ✅ GET/POST/PUT/DELETE, get by id | ✅ Trang Công ty (Companies) | ✅ Mã số thuê unique (kiểm tra khi tạo/sửa). |
| Văn phòng | ✅ GET/POST/PUT/DELETE, get by id | ✅ Trang Văn phòng (Offices) | ✅ area, base_price &gt; 0 (schema + form). |
| Nhân viên tòa nhà | ✅ GET/POST/PUT/DELETE, get by id | ✅ Trang Lương gọi API building-employees; **chưa** có trang CRUD riêng cho nhân viên tòa nhà | — |
| Nhân viên công ty | ❌ Không có API CRUD | ❌ Không có trang CRUD | — |
| Hợp đồng thuê | ✅ GET/POST/PUT/DELETE, list, by company | ❌ Chưa có trang CRUD Hợp đồng (chỉ có contractsAPI.getAll trong client) | ✅ Văn phòng không trùng lịch (check_availability khi tạo/sửa). |
| Dịch vụ tòa nhà | ❌ Không có API CRUD | ❌ Không có trang CRUD | — |

**Kết luận B1:**  
- **Đủ:** Công ty, Văn phòng (backend + frontend + ràng buộc).  
- **Thiếu:**  
  - **Nhân viên công ty:** không API, không trang CRUD.  
  - **Dịch vụ (services):** không API, không trang CRUD.  
  - **Hợp đồng thuê:** có API đủ CRUD và ràng buộc, nhưng **frontend chưa** có trang thêm/sửa/xóa hợp đồng.  
  - **Nhân viên tòa nhà:** có API đủ CRUD, frontend chưa có trang CRUD riêng (chỉ dùng trong báo cáo lương).

---

### B2. Liệt kê công ty + chi phí tháng (tiền thuê + tổng tiền từng loại dịch vụ)

| Yêu cầu | Trạng thái | Ghi chú |
|--------|------------|--------|
| Liệt kê thông tin các công ty | ✅ | Danh sách công ty từ API. |
| Cùng số tiền chi phí một tháng cần trả | ✅ | Trang Chi phí (Costs): chọn tháng/năm, gọi `getMonthlyCosts` từng công ty. |
| Bao gồm tiền thuê mặt bằng (diện tích × đơn giá) | ⚠️ | API trả `rent_cost` = SUM(rent_price) của hợp đồng đang active. Giá thuê đã gắn với văn phòng (có diện tích/vị trí); không tách riêng “diện tích × đơn giá” trên giao diện. |
| Tổng tiền dịch vụ cho từng loại dịch vụ | ✅ | `get_monthly_costs` trả `service_costs` (theo từng dịch vụ). |
| Danh sách công ty sắp xếp theo thứ tự nhất định | ⚠️ | Hiện trả theo thứ tự API (id); có thể sort thêm trên frontend (tên, tổng chi phí...). |

---

### B3. Chi tiết chi phí dịch vụ từng công ty + giá từng lần sử dụng

| Yêu cầu | Trạng thái | Ghi chú |
|--------|------------|--------|
| Chi tiết các chi phí dịch vụ của từng công ty | ✅ | API `GET /companies/{id}/service-details?month=&year=`. |
| Giá tiền từng lần sử dụng dịch vụ | ✅ | Trả `monthly_services` (theo dịch vụ, quantity, price, total) và `daily_services` (employee_name, service_name, usage_date, price). |
| Hiển thị trên web | ⚠️ | API có; cần kiểm tra trang Chi phí/Báo cáo có gọi và hiển thị chi tiết theo công ty hay chưa (vd: chọn 1 công ty rồi xem service-details). |

---

### B4. Nhân viên tòa nhà + lương tháng; đổi vị trí/dịch vụ theo tháng

| Yêu cầu | Trạng thái | Ghi chú |
|--------|------------|--------|
| Liệt kê thông tin nhân viên tòa nhà | ✅ | API `GET /building-employees`. |
| Cùng lương tháng | ✅ | API `GET /building-employees/salaries/monthly?month=&year=`; trang Lương (Salaries) dùng API này. |
| Lương theo vị trí và theo dịch vụ | ✅ | Repository dùng `service_subscribers`, `service_role_rules`, `salary_rules`; lương = base_salary + (doanh thu dịch vụ × bonus_rate). |
| Nhân viên có thể đổi vị trí (bậc công việc) và tên dịch vụ theo tháng | ✅ | `service_subscribers` có `from_date`, `end_date`; query lương theo tháng đã filter theo khoảng thời gian. Schema hỗ trợ đổi dịch vụ/vị trí theo tháng. |

---

### B5. Tổng thu / tổng chi toàn tòa nhà + chi tiết các khoản thu, chi

| Yêu cầu | Trạng thái | Ghi chú |
|--------|------------|--------|
| Hiển thị tổng tiền thu và tổng tiền chi toàn tòa nhà | ✅ | API `GET /reports/building-finance?month=&year=` trả total_revenue, total_expense, net_profit. Trang Báo cáo hiển thị. |
| Chi tiết các khoản thu | ✅ | API `GET /reports/building-finance/details` trả `revenue_details` (invoice, company, amount...). |
| Chi tiết các khoản chi | ✅ | Cùng API trả `expense_details` (nhân viên, lương, bonus...). |

---

### B6. Ràng buộc số lượng bản ghi thể hiện trong ứng dụng

| Ràng buộc | Trạng thái | Ghi chú |
|-----------|------------|--------|
| Mã số thuê (tax_code) unique | ✅ | Kiểm tra khi tạo/sửa công ty (service + repository). |
| Mỗi văn phòng tại một thời điểm tối đa 1 công ty | ✅ | Kiểm tra khi tạo/sửa hợp đồng (`check_availability`). |
| Ràng buộc schema (CHECK, FK, UNIQUE) | ✅ | Trong migration: area &gt; 0, base_price &gt; 0, status enum, end_date &gt; from_date, v.v. |

---

## C. Tóm tắt: đã đủ / chưa đủ

### Đã đáp ứng đủ hoặc về cơ bản đủ

- CSDL: đủ bảng và quan hệ (công ty, văn phòng, nhân viên tòa nhà, nhân viên công ty, dịch vụ, hợp đồng, sử dụng dịch vụ theo tháng/theo ngày).
- Ràng buộc: 1 văn phòng tối đa 1 công ty theo thời gian; tax_code unique; ràng buộc schema.
- Dữ liệu mẫu: ≥ 2 tháng.
- Dịch vụ theo ngày (ăn uống, gửi xe): lưu theo nhân viên theo từng ngày.
- Nhân viên tòa nhà: phân cấp, gắn dịch vụ, lương theo vị trí và doanh thu dịch vụ; đổi vị trí/dịch vụ theo tháng (schema + API lương).
- Ứng dụng: CRUD Công ty, Văn phòng (có ràng buộc); liệt kê công ty + chi phí tháng; chi tiết dịch vụ theo công ty (API); báo cáo tổng thu/chi và chi tiết thu/chi; API lương nhân viên tòa nhà theo tháng.

### Chưa đủ hoặc cần bổ sung

1. **CRUD nhân viên công ty:** Chưa có API và trang thêm/sửa/xóa nhân viên công ty.
2. **CRUD dịch vụ tòa nhà:** Chưa có API và trang thêm/sửa/xóa dịch vụ (services).
3. **Trang CRUD hợp đồng thuê:** Backend đủ (POST/PUT/DELETE + check_availability), frontend chưa có trang tạo/sửa/xóa hợp đồng.
4. **Trang CRUD nhân viên tòa nhà:** Backend đủ, frontend chưa có trang riêng (chỉ dùng trong báo cáo lương).
5. **Đơn giá dịch vụ theo công thức đề bài:** Chưa có logic tính đơn giá vệ sinh theo quy tắc “&lt;10 người và ≤100 m² cùng giá, +5 người hoặc +10 m² thì +5%”.
6. **Tính tiền dịch vụ theo tỉ lệ ngày (không dùng hết tháng):** Chưa thấy logic prorate (ngày dùng / tổng ngày tháng) trong code.
7. **Liệt kê công ty + chi phí:** Có thể bổ sung sắp xếp rõ ràng (vd: theo tên, theo tổng chi phí) và (tùy đề) hiển thị rõ “tiền thuê = diện tích × đơn giá” nếu giảng viên yêu cầu chi tiết.

---

## D. Đề xuất bổ sung để đạt đủ đề bài

1. **Backend:**  
   - API CRUD cho `company_employees`.  
   - API CRUD cho `services` (dịch vụ tòa nhà).

2. **Frontend:**  
   - Trang CRUD Hợp đồng thuê (danh sách, thêm, sửa, xóa; chọn văn phòng/công ty, khoảng ngày; reload sau thao tác).  
   - Trang CRUD Nhân viên tòa nhà (danh sách, thêm, sửa, xóa).  
   - Trang CRUD Nhân viên công ty (khi đã có API).  
   - Trang CRUD Dịch vụ (khi đã có API).  
   - Trang Chi phí: có thể thêm view “chi tiết dịch vụ theo công ty” (gọi `service-details`) và sắp xếp danh sách công ty.

3. **Logic nghiệp vụ (tùy mức độ yêu cầu):**  
   - Hàm/procedure tính đơn giá vệ sinh theo công thức đề bài (10 người, 100 m², +5%).  
   - Tính tiền dịch vụ theo tỉ lệ ngày khi không dùng hết tháng (nếu đề bắt buộc).

---

*Báo cáo kiểm tra đối chiếu với mã nguồn và API hiện tại (schema, back_end, front_end).*
