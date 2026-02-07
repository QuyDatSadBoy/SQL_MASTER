# Báo cáo tổng quan ứng dụng Web — Hệ thống Quản lý Tòa nhà Văn phòng

---

## 1. Tổng quan ứng dụng

Ứng dụng Web **Office Manager** (Hệ thống quản lý tòa nhà văn phòng) gồm **4 màn hình chính**:

| Màn hình | Mô tả |
|----------|--------|
| **Trang chủ** | Hiển thị tổng quan hệ thống: số lượng bản ghi của một số bảng (văn phòng, công ty, hợp đồng, nhân viên tòa nhà) và thống kê doanh thu, lợi nhuận theo tháng. |
| **Quản lý CRUD** | Trang để thêm, xem, sửa, xóa dữ liệu các bảng (văn phòng, công ty, chi phí, lương, v.v.). |
| **Báo cáo & Thống kê** | Hiển thị các báo cáo nghiệp vụ: người dùng chọn loại báo cáo, điền thông tin (tháng/năm, công ty…), hệ thống trả về kết quả tương ứng. |
| **Truy vấn SQL** | Cho phép tương tác với cơ sở dữ liệu (thực thi câu lệnh SQL) mà không cần mở phần mềm quản lý CSDL riêng (PostgreSQL/pgAdmin). |

---

## 2. Quản lý CRUD

- **Dropdown chọn bảng:** Ứng dụng hiện có các trang CRUD riêng theo từng đối tượng: Văn phòng (`/offices`), Công ty (`/companies`), Chi phí (`/costs`), Lương (`/salaries`). Có thể mở rộng thành một màn CRUD thống nhất với dropdown chọn bảng (offices, companies, contracts, building-employees, …).
- **Nút Reload:** Mỗi trang CRUD có chức năng tải lại dữ liệu (gọi API lấy danh sách mới nhất). Sau khi thêm, sửa hoặc xóa, người dùng có thể bấm nút reload (hoặc danh sách tự cập nhật sau thao tác thành công) để xem dữ liệu mới nhất trong CSDL.
- **Màn thêm dữ liệu:** Mỗi trang CRUD có form thêm mới (modal hoặc form riêng): nhập đầy đủ thông tin theo bảng (ví dụ văn phòng: tên, diện tích, tầng, vị trí, giá thuê; công ty: tên, mã số thuế, email, địa chỉ). Gửi lên API (POST), sau đó reload danh sách để hiển thị bản ghi vừa thêm.

---

## 3. Báo cáo & Thống kê

- Người dùng chọn **một trong các loại báo cáo** có sẵn (tương ứng các API/procedure phía backend).
- **Điền các thông tin cần thiết** (ví dụ: tháng, năm; hoặc mã công ty kèm tháng/năm).
- Hệ thống gọi API và **trả về kết quả tương ứng** (bảng số liệu, tổng thu, tổng chi, lợi nhuận, chi tiết dịch vụ, lương nhân viên, v.v.).

**Các báo cáo hiện có (theo API backend):**

| STT | Loại báo cáo | Thông tin cần nhập | Kết quả trả về |
|-----|--------------|--------------------|----------------|
| 1 | Chi phí tháng của công ty | Mã công ty, tháng, năm | Tổng chi phí tháng của công ty (thuê văn phòng + dịch vụ). |
| 2 | Chi tiết dịch vụ công ty | Mã công ty, tháng, năm | Chi tiết từng dịch vụ (vệ sinh, an ninh, gửi xe, ăn trưa, bảo trì…) và số tiền. |
| 3 | Lương nhân viên tòa nhà | Tháng, năm | Danh sách nhân viên tòa nhà và lương tháng (lương cơ bản + thưởng theo dịch vụ). |
| 4 | Tổng thu chi tòa nhà | Tháng, năm | Tổng doanh thu, tổng chi, lợi nhuận (net) của tòa nhà trong tháng. |
| 5 | Chi tiết thu chi tòa nhà | Tháng, năm | Chi tiết các khoản thu (theo nguồn) và các khoản chi (theo danh mục). |

*(Có thể mở rộng thêm 2 báo cáo nữa để đủ 7 procedure theo yêu cầu, ví dụ: báo cáo hợp đồng sắp hết hạn, báo cáo tỷ lệ lấp đầy văn phòng.)*

---

## 4. Truy vấn SQL

- Màn hình **Truy vấn SQL** cho phép người dùng nhập câu lệnh SQL (SELECT, INSERT, UPDATE, DELETE, …) và thực thi trực tiếp trên CSDL.
- **Không cần mở phần mềm quản lý CSDL riêng** (pgAdmin, DBeaver, MySQL Workbench, v.v.): mọi thao tác đọc/ghi có thể thực hiện qua giao diện web (với điều kiện backend cung cấp endpoint an toàn để thực thi SQL và phân quyền phù hợp).

*(Tính năng này có thể triển khai sau: frontend có form nhập SQL, gửi lên API backend, backend thực thi và trả về kết quả hoặc thông báo lỗi.)*

---

## Tóm tắt

- **Trang chủ:** Tổng quan số lượng bảng ghi và thống kê doanh thu/lợi nhuận.
- **Quản lý CRUD:** Dropdown chọn bảng (hoặc các trang CRUD riêng), nút reload, màn thêm/sửa/xóa dữ liệu.
- **Báo cáo & Thống kê:** Chọn loại báo cáo, điền thông tin, xem kết quả (hiện có 5 nhóm báo cáo, có thể mở rộng đủ 7).
- **Truy vấn SQL:** Tương tác với CSDL qua web, không cần mở phần mềm quản lý CSDL riêng.

---

*Báo cáo dựa trên hiện trạng ứng dụng Web (front_end + back_end) — Hệ thống quản lý tòa nhà văn phòng.*
