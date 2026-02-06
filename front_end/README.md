# Frontend - Hệ thống Quản lý Tòa nhà Văn phòng

**Sinh viên**: Trần Quý Đạt — PTIT  
**Đề tài 7**: Xây dựng Hệ CSDL quản lý một Tòa nhà văn phòng

---

## Đề bài

Xây dựng hệ CSDL quản lý một Tòa nhà văn phòng, bao gồm:

- **Văn phòng cho thuê**: Tòa nhà chia thành nhiều văn phòng với vị trí, diện tích và giá thuê khác nhau.
- **Công ty thuê**: Một công ty có thể thuê nhiều văn phòng; mỗi văn phòng tại một thời điểm chỉ do tối đa 1 công ty thuê.
- **Dịch vụ**: Vệ sinh, ăn uống, trông xe, bảo vệ, bảo trì thiết bị... Đơn giá một số dịch vụ tỉ lệ theo số người và/hoặc diện tích thuê (ví dụ: dưới 10 người & ≤ 100m² = mức giá cơ bản, cứ thêm 5 người hoặc 10m² → +5%). Dịch vụ ăn uống, gửi xe tính theo nhân viên từng ngày.
- **Nhân viên tòa nhà**: Phân cấp quản lý và nhân viên dịch vụ. Lương tỉ lệ thuận với doanh thu của dịch vụ mà họ phụ trách.
- **Ứng dụng**: CRUD các đối tượng, liệt kê chi phí công ty theo tháng, chi tiết dịch vụ, lương nhân viên, tổng thu chi tòa nhà.

---

## Công nghệ

| Thành phần | Công nghệ |
| ---------- | --------- |
| Framework | React 19 + Vite 7 |
| CSS | Tailwind CSS v4 (plugin `@tailwindcss/vite`) |
| HTTP Client | Axios |
| Routing | React Router DOM v7 |
| Icons | Lucide React (SVG) |
| Font | Plus Jakarta Sans (Google Fonts) |

---

## Cấu trúc

```text
front_end/
├── index.html
├── vite.config.js
├── package.json
└── src/
    ├── main.jsx              # Entry point
    ├── index.css             # Tailwind + theme colors
    ├── App.jsx               # Router (6 routes)
    ├── api/
    │   └── client.js         # Axios API client (all endpoints)
    ├── components/
    │   ├── Layout.jsx        # Layout chung (Navbar + Outlet)
    │   └── Navbar.jsx        # Thanh điều hướng
    ├── pages/
    │   ├── Dashboard.jsx     # Tổng quan (thống kê)
    │   ├── Offices.jsx       # CRUD Văn phòng
    │   ├── Companies.jsx     # CRUD Công ty
    │   ├── Costs.jsx         # Chi phí công ty theo tháng
    │   ├── Salaries.jsx      # Lương nhân viên tòa nhà
    │   └── Reports.jsx       # Báo cáo thu chi tòa nhà
    └── utils/
        └── formatters.js     # Format VND, ngày tháng, số
```

---

## Cài đặt & Chạy

```bash
# 1. Cài dependencies
cd front_end
npm install

# 2. Chạy dev server
npm run dev
```

Dev server sẽ chạy tại `http://localhost:5173`.

> Backend API phải chạy trước tại `http://localhost:8222` (xem hướng dẫn ở root README).

---

## Các trang

| Trang | Route | Chức năng |
| ----- | ----- | --------- |
| Tổng quan | `/` | Thống kê văn phòng, công ty, doanh thu |
| Văn phòng | `/offices` | CRUD văn phòng (tên, diện tích, tầng, giá) |
| Công ty | `/companies` | CRUD công ty (tên, mã số thuế, email) |
| Chi phí | `/costs` | Chi phí thuê + dịch vụ của từng công ty theo tháng |
| Lương | `/salaries` | Lương nhân viên tòa nhà (base + bonus) |
| Báo cáo | `/reports` | Tổng thu, tổng chi, lợi nhuận, chi tiết các khoản |

---

## Build Production

```bash
npm run build    # Output: dist/
npm run preview  # Preview bản build
```
