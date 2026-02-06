# Chi tiết Frontend — Quản lý Tòa nhà Văn phòng

**Stack**: React 19 + Vite 7 + Tailwind CSS v4 + Axios  
**Dev server**: http://localhost:5173  
**Backend API**: http://localhost:8222

---

## 1. Công nghệ chi tiết

| Thành phần | Công nghệ | Phiên bản | Mục đích |
| ---------- | --------- | --------- | -------- |
| Build tool | Vite | 7.3 | Dev server + HMR + production build |
| UI Library | React | 19.2 | Component-based UI |
| CSS Framework | Tailwind CSS v4 | 4.1 | Utility-first CSS (qua plugin @tailwindcss/vite) |
| HTTP Client | Axios | 1.13 | Gọi API backend |
| Routing | React Router DOM | 7.13 | Client-side routing (6 routes) |
| Icons | Lucide React | 0.563 | SVG icons (Building2, Users, Plus, Edit, Trash2...) |
| Font | Plus Jakarta Sans | — | Google Fonts (300–700 weight) |

### Tailwind CSS v4 — Cách cấu hình

Tailwind v4 **không** dùng PostCSS hay `tailwind.config.js`. Thay vào đó:

- Plugin Vite: `@tailwindcss/vite` trong `vite.config.js`.
- CSS: `@import "tailwindcss"` + `@theme {}` block trong `src/index.css`.
- Gradient: dùng `bg-linear-to-br` (v4) thay vì `bg-gradient-to-br` (v3).

```css
/* src/index.css */
@import "tailwindcss";

@theme {
  --font-sans: 'Plus Jakarta Sans', sans-serif;
  --color-primary: #7C3AED;
  --color-secondary: #A78BFA;
  --color-cta: #F97316;
  --color-background: #FAF5FF;
  --color-text: #4C1D95;
}
```

---

## 2. Cấu trúc code chi tiết

```text
front_end/
├── index.html              # HTML entry (lang="vi")
├── vite.config.js          # Vite + React + Tailwind plugins
├── package.json
├── eslint.config.js
└── src/
    ├── main.jsx            # ReactDOM.createRoot + import index.css
    ├── index.css           # @import "tailwindcss" + @theme + @layer base
    ├── App.jsx             # BrowserRouter → Routes → 6 pages via Layout
    │
    ├── api/
    │   └── client.js       # Axios instance + 5 API modules:
    │                        #   officesAPI   (getAll, getById, create, update, delete)
    │                        #   companiesAPI (+ getMonthlyCosts, getServiceDetails)
    │                        #   employeesAPI (getAll, getSalaries)
    │                        #   contractsAPI (getAll)
    │                        #   reportsAPI   (getFinance, getFinanceDetails)
    │
    ├── components/
    │   ├── Layout.jsx      # <Navbar /> + <Outlet /> với min-h-screen + padding
    │   └── Navbar.jsx      # 6 links (Tổng quan, Văn phòng, Công ty, Chi phí, Lương, Báo cáo)
    │                        # Fixed top, backdrop-blur, floating style
    │
    ├── pages/
    │   ├── Dashboard.jsx   # Trang chủ — 4 stat cards + welcome banner
    │   ├── Offices.jsx     # CRUD văn phòng — table + modal form
    │   ├── Companies.jsx   # CRUD công ty — cards + modal form
    │   ├── Costs.jsx       # Chi phí tháng — filters + summary + breakdown
    │   ├── Salaries.jsx    # Lương NV — table + search + summary cards
    │   └── Reports.jsx     # Thu chi tòa nhà — 3 cards + detail tables
    │
    └── utils/
        └── formatters.js   # formatCurrency (VND), formatDate, formatNumber
```

---

## 3. Các trang & chức năng

### 3.1 Dashboard (`/`)

- **4 stat cards**: Văn phòng (count), Công ty (count), Doanh thu, Lợi nhuận.
- **Welcome banner**: gradient `bg-linear-to-br from-primary to-purple-600`.
- **Data**: Gọi `officesAPI.getAll()`, `companiesAPI.getAll()`, `reportsAPI.getFinance()`.

### 3.2 Văn phòng (`/offices`)

- **Hiển thị**: 6 cards — tên, tầng, diện tích, vị trí, giá/tháng.
- **CRUD**: Thêm (nút +) / Sửa (icon Edit) / Xóa (icon Trash2 + confirm).
- **Modal form**: name, area, floor, position, base_price.
- **Format**: giá VND ("15.000.000 ₫/tháng").

### 3.3 Công ty (`/companies`)

- **Hiển thị**: 3 cards — tên, mã số thuế, email, địa chỉ.
- **CRUD**: Thêm / Sửa / Xóa (giống Offices).
- **Modal form**: name, tax_code, email, address.

### 3.4 Chi phí tháng (`/costs`)

- **Bộ lọc**: Tháng (1–12), Năm, Công ty (combobox).
- **Summary card**: Tổng chi phí tất cả công ty (gradient).
- **Breakdown**: Từng công ty — tiền thuê + dịch vụ + tổng. Sắp xếp theo tổng chi phí.
- **API**: `companiesAPI.getMonthlyCosts()` cho từng company.

### 3.5 Lương nhân viên (`/salaries`)

- **Bộ lọc**: Tháng, Năm, Tìm kiếm theo tên.
- **Table**: STT, Tên, Vai trò, Lương cơ bản, Bonus rate, Doanh thu, Tổng lương.
- **Summary cards**: Tổng lương cơ bản, Tổng thưởng, Tổng lương thực nhận.
- **API**: `employeesAPI.getSalaries(month, year)`.

### 3.6 Báo cáo tài chính (`/reports`)

- **Bộ lọc**: Tháng, Năm.
- **3 summary cards**: Tổng thu (green), Tổng chi (red), Lợi nhuận (purple) + % doanh thu.
- **"Xem chi tiết" button**: Toggle hiển thị 2 bảng chi tiết.
  - Chi tiết thu nhập (revenue_details).
  - Chi tiết chi phí (expense_details).
- **API**: `reportsAPI.getFinance()` + `reportsAPI.getFinanceDetails()`.

---

## 4. Design System

### Bảng màu (Tailwind @theme)

| Token | Hex | Sử dụng |
| ----- | --- | ------- |
| primary | #7C3AED | Navbar, buttons, headings, gradients |
| secondary | #A78BFA | Hover states, secondary elements |
| cta | #F97316 | Call-to-action buttons (Thêm, Sửa) |
| background | #FAF5FF | Nền trang |
| text | #4C1D95 | Văn bản chính |

### Font

- **Plus Jakarta Sans**: 300 (light), 400 (regular), 500 (medium), 600 (semi-bold), 700 (bold).
- Load qua `@import url()` trong `index.css`.

### Icons

- **Lucide React**: SVG-based, tree-shakeable.
- Các icon dùng: Building2, Users, DollarSign, TrendingUp, Plus, Edit, Trash2, Search, Phone, Mail, MapPin, Eye, EyeOff.

### Gradient

- Dùng `bg-linear-to-br` (Tailwind v4 syntax).
- Ví dụ: `bg-linear-to-br from-primary to-purple-600`.

---

## 5. API Client (`src/api/client.js`)

```javascript
// Base URL
const API_BASE_URL = 'http://localhost:8222/api';

// 5 modules:
officesAPI    → getAll, getById, create, update, delete
companiesAPI  → getAll, getById, create, update, delete,
                getMonthlyCosts(id, month, year),
                getServiceDetails(id, month, year)
employeesAPI  → getAll, getSalaries(month, year)
contractsAPI  → getAll
reportsAPI    → getFinance(month, year), getFinanceDetails(month, year)
```

---

## 6. Utility Functions (`src/utils/formatters.js`)

| Function | Input | Output | Ví dụ |
| -------- | ----- | ------ | ----- |
| formatCurrency(value) | number | string (VND) | `15000000` → `"15.000.000 ₫"` |
| formatDate(date) | string | string (DD/MM/YYYY) | `"2026-01-15"` → `"15/01/2026"` |
| formatNumber(value) | number | string | `1500.5` → `"1.500,5"` |

---

## 7. Accessibility

- Tất cả form fields có `id` + `<label htmlFor>` matching.
- Semantic HTML: `<nav>`, `<main>`, `<h1>`–`<h3>`, `<table>`.
- `lang="vi"` trên `<html>`.
- Console: 0 errors, 0 warnings trên cả 6 trang.

---

## 8. Kết quả kiểm thử

| Trang | Route | Kết quả | Console |
| ----- | ----- | ------- | ------- |
| Tổng quan | / | PASS | 0 errors |
| Văn phòng | /offices | PASS | 0 errors |
| Công ty | /companies | PASS | 0 errors |
| Chi phí | /costs | PASS | 0 errors |
| Lương | /salaries | PASS | 0 errors |
| Báo cáo | /reports | PASS | 0 errors |

- **Navigation**: 6/6 links hoạt động đúng.
- **Screenshots**: `test/frontend/screenshots/01_dashboard.png` → `06_reports.png`.
- Chi tiết: `test/frontend/REPORT.md`.

---

## 9. Bugs đã fix

| Bug | File | Giải pháp |
| --- | ---- | --------- |
| `bg-gradient-to-br` → lỗi Tailwind v4 | Dashboard, Costs, Reports | Đổi thành `bg-linear-to-br` |
| `details.map is not a function` | Reports.jsx | API trả object, không phải array. Đổi state + `.revenue_details.map()` |
| "Vănphòng" (thiếu space) | Navbar.jsx | Đổi thành "Văn phòng" |
| Accessibility warnings (label/id) | Costs, Salaries, Reports | Thêm `id` + `htmlFor` cho 8 form fields |

---

## 10. Cài đặt & Chạy

```bash
cd front_end
npm install
npm run dev        # → http://localhost:5173
npm run build      # → dist/
npm run preview    # Preview bản build
```

> Backend phải chạy trước tại http://localhost:8222.
