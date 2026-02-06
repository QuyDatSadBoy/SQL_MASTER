import { useState, useEffect, useCallback } from 'react';
import { Search, DollarSign, Calendar } from 'lucide-react';
import { employeesAPI } from '../api/client';
import { formatCurrency, getCurrentMonthYear } from '../utils/formatters';

const Salaries = () => {
  const [salaries, setSalaries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [month, setMonth] = useState(getCurrentMonthYear().month);
  const [year, setYear] = useState(getCurrentMonthYear().year);
  const [searchQuery, setSearchQuery] = useState('');

  // Define fetchSalaries before useEffect to avoid TDZ error
  const fetchSalaries = useCallback(async () => {
    setLoading(true);
    try {
      const response = await employeesAPI.getSalaries(month, year);
      setSalaries(response.data);
    } catch (error) {
      console.error('Error fetching salaries:', error);
      alert('Lỗi tải dữ liệu lương');
    } finally {
      setLoading(false);
    }
  }, [month, year]);

  useEffect(() => {
    if (month && year) {
      fetchSalaries();
    }
  }, [month, year, fetchSalaries]);

  const filteredSalaries = salaries.filter((salary) =>
    salary.full_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalBaseSalary = filteredSalaries.reduce((sum, s) => sum + s.base_salary, 0);
  const totalBonus = filteredSalaries.reduce((sum, s) => sum + (s.total_salary - s.base_salary), 0);
  const totalSalary = filteredSalaries.reduce((sum, s) => sum + s.total_salary, 0);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-primary">Lương nhân viên</h1>
          <p className="text-text/60 mt-2">Xem lương nhân viên quản lý tòa nhà</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="sal-month" className="block text-sm font-medium text-text mb-2">Tháng</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary" />
              <select
                id="sal-month"
                value={month}
                onChange={(e) => setMonth(parseInt(e.target.value))}
                className="w-full pl-10 pr-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent cursor-pointer"
              >
                {[...Array(12)].map((_, i) => (
                  <option key={i + 1} value={i + 1}>
                    Tháng {i + 1}
                  </option>
                ))}
              </select>
            </div>
          </div>
          <div>
            <label htmlFor="sal-year" className="block text-sm font-medium text-text mb-2">Năm</label>
            <input
              id="sal-year"
              type="number"
              value={year}
              onChange={(e) => setYear(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <div>
            <label htmlFor="sal-search" className="block text-sm font-medium text-text mb-2">Tìm nhân viên</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary" />
              <input
                id="sal-search"
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Nhập tên nhân viên..."
                className="w-full pl-10 pr-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
          <p className="text-sm text-text/60 font-medium">Tổng lương cơ bản</p>
          <p className="text-2xl font-bold text-text mt-2">{formatCurrency(totalBaseSalary)}</p>
        </div>
        <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
          <p className="text-sm text-text/60 font-medium">Tổng thưởng</p>
          <p className="text-2xl font-bold text-green-600 mt-2">{formatCurrency(totalBonus)}</p>
        </div>
        <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
          <p className="text-sm text-text/60 font-medium">Tổng lương thực nhận</p>
          <p className="text-2xl font-bold text-primary mt-2">{formatCurrency(totalSalary)}</p>
        </div>
      </div>

      {/* Salaries Table */}
      <div className="bg-white rounded-2xl border border-purple-100 shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-primary text-white">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium">Nhân viên</th>
                <th className="px-6 py-4 text-left text-sm font-medium">Vị trí</th>
                <th className="px-6 py-4 text-right text-sm font-medium">Lương cơ bản</th>
                <th className="px-6 py-4 text-right text-sm font-medium">Thưởng</th>
                <th className="px-6 py-4 text-right text-sm font-medium">Tổng lương</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-purple-100">
              {filteredSalaries.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-12 text-center text-text/60">
                    Không có dữ liệu lương cho tháng này
                  </td>
                </tr>
              ) : (
                filteredSalaries.map((salary) => (
                  <tr key={salary.employee_id} className="hover:bg-purple-50 transition-colors duration-200">
                    <td className="px-6 py-4">
                      <div>
                        <p className="font-medium text-text">{salary.full_name}</p>
                        <p className="text-sm text-text/60">ID: {salary.employee_id}</p>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-text/80">{salary.role}</td>
                    <td className="px-6 py-4 text-right font-medium text-text">
                      {formatCurrency(salary.base_salary)}
                    </td>
                    <td className="px-6 py-4 text-right font-medium text-green-600">
                      {formatCurrency(salary.total_salary - salary.base_salary)}
                    </td>
                    <td className="px-6 py-4 text-right font-bold text-primary">
                      {formatCurrency(salary.total_salary)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Salaries;
