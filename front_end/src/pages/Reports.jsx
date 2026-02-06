import { useState, useEffect, useCallback } from 'react';
import { TrendingUp, TrendingDown, Calendar, FileText } from 'lucide-react';
import { reportsAPI } from '../api/client';
import { formatCurrency, getCurrentMonthYear } from '../utils/formatters';

const Reports = () => {
  const [report, setReport] = useState(null);
  const [details, setDetails] = useState({ revenue_details: [], expense_details: [] });
  const [loading, setLoading] = useState(true);
  const [month, setMonth] = useState(getCurrentMonthYear().month);
  const [year, setYear] = useState(getCurrentMonthYear().year);
  const [showDetails, setShowDetails] = useState(false);

  // Define fetchReport before useEffect to avoid TDZ error
  const fetchReport = useCallback(async () => {
    setLoading(true);
    try {
      const [reportRes, detailsRes] = await Promise.all([
        reportsAPI.getFinance(month, year),
        reportsAPI.getFinanceDetails(month, year),
      ]);
      setReport(reportRes.data);
      setDetails(detailsRes.data);
    } catch (error) {
      console.error('Error fetching report:', error);
      alert('Lỗi tải báo cáo tài chính');
    } finally {
      setLoading(false);
    }
  }, [month, year]);

  useEffect(() => {
    if (month && year) {
      fetchReport();
    }
  }, [month, year, fetchReport]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-text/60">Không có dữ liệu báo cáo</p>
      </div>
    );
  }

  const isProfit = report.net_profit >= 0;
  const profitPercentage = report.total_revenue > 0
    ? ((report.net_profit / report.total_revenue) * 100).toFixed(1)
    : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-primary">Báo cáo tài chính</h1>
          <p className="text-text/60 mt-2">Báo cáo thu chi tòa nhà theo tháng</p>
        </div>
      </div>

      {/* Month/Year Selector */}
      <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="rpt-month" className="block text-sm font-medium text-text mb-2">Tháng</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary" />
              <select
                id="rpt-month"
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
            <label htmlFor="rpt-year" className="block text-sm font-medium text-text mb-2">Năm</label>
            <input
              id="rpt-year"
              type="number"
              value={year}
              onChange={(e) => setYear(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-linear-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm font-medium">Tổng thu</p>
              <p className="text-3xl font-bold mt-2">{formatCurrency(report.total_revenue)}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <TrendingUp className="w-8 h-8" />
            </div>
          </div>
        </div>

        <div className="bg-linear-to-br from-red-500 to-red-600 rounded-2xl p-6 text-white shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm font-medium">Tổng chi</p>
              <p className="text-3xl font-bold mt-2">{formatCurrency(report.total_expense)}</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              <TrendingDown className="w-8 h-8" />
            </div>
          </div>
        </div>

        <div
          className={`rounded-2xl p-6 text-white shadow-lg ${isProfit ? 'bg-linear-to-br from-primary to-purple-600' : 'bg-red-600'}`}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white/80 text-sm font-medium">
                {isProfit ? 'Lợi nhuận' : 'Lỗ'}
              </p>
              <p className="text-3xl font-bold mt-2">{formatCurrency(Math.abs(report.net_profit))}</p>
              <p className="text-white/80 text-sm mt-1">{profitPercentage}% doanh thu</p>
            </div>
            <div className="bg-white/20 p-3 rounded-xl">
              {isProfit ? <TrendingUp className="w-8 h-8" /> : <TrendingDown className="w-8 h-8" />}
            </div>
          </div>
        </div>
      </div>

      {/* Details Toggle */}
      <div className="flex justify-center">
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="flex items-center space-x-2 px-6 py-3 bg-primary text-white rounded-xl hover:bg-purple-700 transition-colors duration-200 cursor-pointer shadow-lg"
        >
          <FileText className="w-5 h-5" />
          <span className="font-medium">{showDetails ? 'Ẩn chi tiết' : 'Xem chi tiết'}</span>
        </button>
      </div>

      {/* Details Section */}
      {showDetails && (
        <div className="space-y-6">
          {/* Revenue Details */}
          <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
            <h3 className="text-xl font-bold text-green-600 mb-4">Chi tiết thu nhập</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-green-50">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-green-800">Công ty</th>
                    <th className="px-4 py-3 text-left text-sm font-medium text-green-800">Văn phòng</th>
                    <th className="px-4 py-3 text-right text-sm font-medium text-green-800">Thuê VP</th>
                    <th className="px-4 py-3 text-right text-sm font-medium text-green-800">DV Tháng</th>
                    <th className="px-4 py-3 text-right text-sm font-medium text-green-800">DV Ngày</th>
                    <th className="px-4 py-3 text-right text-sm font-medium text-green-800">Tổng thu</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-green-100">
                  {details.revenue_details.map((detail, index) => (
                    <tr key={index} className="hover:bg-green-50 transition-colors duration-200">
                      <td className="px-4 py-3 text-sm text-text">{detail.company_name}</td>
                      <td className="px-4 py-3 text-sm text-text/80">{detail.office_name}</td>
                      <td className="px-4 py-3 text-sm text-right text-text">{formatCurrency(detail.rent_cost)}</td>
                      <td className="px-4 py-3 text-sm text-right text-text">{formatCurrency(detail.monthly_service_cost)}</td>
                      <td className="px-4 py-3 text-sm text-right text-text">{formatCurrency(detail.daily_service_cost)}</td>
                      <td className="px-4 py-3 text-sm text-right font-medium text-green-600">
                        {formatCurrency(detail.total_revenue)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Expense Breakdown */}
          <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
            <h3 className="text-xl font-bold text-red-600 mb-4">Chi tiết chi phí</h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center p-4 bg-red-50 rounded-lg">
                <span className="text-text font-medium">Tổng chi lương nhân viên</span>
                <span className="text-lg font-bold text-red-600">{formatCurrency(report.total_expense)}</span>
              </div>
              <p className="text-sm text-text/60 px-4">
                Bao gồm lương cơ bản và thưởng cho toàn bộ nhân viên quản lý tòa nhà
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;
