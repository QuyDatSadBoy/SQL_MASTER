import { useState, useEffect, useCallback } from 'react';
import { Search, DollarSign, Calendar, X, FileText, Building2 } from 'lucide-react';
import { companiesAPI } from '../api/client';
import { formatCurrency, formatDate, formatNumber, getCurrentMonthYear } from '../utils/formatters';

/** Parse monthly_services / daily_services từ API (array hoặc JSON string). */
function parseServiceArray(val) {
  if (Array.isArray(val)) return val;
  if (typeof val === 'string') {
    try {
      const p = JSON.parse(val);
      return Array.isArray(p) ? p : [];
    } catch {
      return [];
    }
  }
  return [];
}

const Costs = () => {
  const [costs, setCosts] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [month, setMonth] = useState(getCurrentMonthYear().month);
  const [year, setYear] = useState(getCurrentMonthYear().year);
  const [selectedCompany, setSelectedCompany] = useState('');
  const [detailCompanyId, setDetailCompanyId] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailData, setDetailData] = useState(null);

  // Define fetchCosts before useEffect to avoid TDZ error
  const fetchCosts = useCallback(async () => {
    setLoading(true);
    try {
      // Fetch all companies first
      const companiesRes = await companiesAPI.getAll();
      const companiesList = companiesRes.data;
      
      // Fetch monthly costs for each company
      const costsPromises = companiesList.map(company => 
        companiesAPI.getMonthlyCosts(company.id, month, year)
          .then(res => ({
            company_id: company.id,
            company_name: company.name,
            tax_code: company.tax_code,
            ...res.data
          }))
          .catch(err => {
            console.error(`Error fetching costs for company ${company.id}:`, err);
            return null;
          })
      );
      
      const costsResults = await Promise.all(costsPromises);
      const validCosts = costsResults.filter(cost => cost !== null);
      setCosts(validCosts);
    } catch (error) {
      console.error('Error fetching costs:', error);
      alert('Lỗi tải chi phí tháng');
    } finally {
      setLoading(false);
    }
  }, [month, year]);

  const fetchCompanies = async () => {
    try {
      const response = await companiesAPI.getAll();
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  const handleOpenDetail = useCallback(
    async (companyId) => {
      setDetailCompanyId(companyId);
      setDetailLoading(true);
      setDetailData(null);
      try {
        const res = await companiesAPI.getCostDetail(companyId, month, year);
        setDetailData(res.data || null);
      } catch (error) {
        console.error('Error fetching cost detail:', error);
        setDetailData(null);
      } finally {
        setDetailLoading(false);
      }
    },
    [month, year]
  );

  useEffect(() => {
    fetchCompanies();
  }, []);

  useEffect(() => {
    if (month && year) {
      fetchCosts();
    }
  }, [month, year, fetchCosts]);

  const filteredCosts = selectedCompany
    ? costs.filter((cost) => cost.company_id === parseInt(selectedCompany))
    : costs;

  const totalCost = filteredCosts.reduce((sum, cost) => sum + cost.total_cost, 0);

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
          <h1 className="text-4xl font-bold text-primary">Chi phí tháng</h1>
          <p className="text-text/60 mt-2">Xem chi phí văn phòng và dịch vụ theo tháng</p>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label htmlFor="costs-month" className="block text-sm font-medium text-text mb-2">Tháng</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary" />
              <select
                id="costs-month"
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
            <label htmlFor="costs-year" className="block text-sm font-medium text-text mb-2">Năm</label>
            <input
              id="costs-year"
              type="number"
              value={year}
              onChange={(e) => setYear(parseInt(e.target.value))}
              className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
          <div>
            <label htmlFor="costs-company" className="block text-sm font-medium text-text mb-2">Công ty</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-primary" />
              <select
                id="costs-company"
                value={selectedCompany}
                onChange={(e) => setSelectedCompany(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent cursor-pointer"
              >
                <option value="">Tất cả công ty</option>
                {companies.map((company) => (
                  <option key={company.id} value={company.id}>
                    {company.name}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Summary */}
      <div className="bg-linear-to-br from-primary to-purple-600 rounded-2xl p-6 text-white shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-white/80">Tổng chi phí tháng {month}/{year}</p>
            <p className="text-3xl font-bold mt-2">{formatCurrency(totalCost)}</p>
          </div>
          <div className="bg-white/20 p-4 rounded-xl">
            <DollarSign className="w-8 h-8" />
          </div>
        </div>
      </div>

      {/* Costs List */}
      <div className="space-y-4">
        {filteredCosts.length === 0 ? (
          <div className="bg-white rounded-2xl p-12 border border-purple-100 text-center">
            <p className="text-text/60">Không có dữ liệu chi phí cho tháng này</p>
          </div>
        ) : (
          filteredCosts.map((cost) => (
            <div
              key={cost.company_id}
              role="button"
              tabIndex={0}
              onClick={() => handleOpenDetail(cost.company_id)}
              onKeyDown={(e) => e.key === 'Enter' && handleOpenDetail(cost.company_id)}
              className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-text">{cost.company_name}</h3>
                  <p className="text-sm text-text/60 mt-1">MST: {cost.tax_code}</p>
                  <p className="text-xs text-primary mt-1">Bấm để xem chi tiết hợp đồng và dịch vụ</p>

                  <div className="mt-4 space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-text/80">Tiền thuê văn phòng:</span>
                      <span className="font-medium text-text">{formatCurrency(cost.rent_cost)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-text/80">Dịch vụ:</span>
                      <span className="font-medium text-text">{formatCurrency(cost.total_service_cost)}</span>
                    </div>
                    <div className="flex justify-between pt-2 border-t border-purple-100">
                      <span className="font-medium text-text">Tổng cộng:</span>
                      <span className="font-bold text-lg text-primary">{formatCurrency(cost.total_cost)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal chi tiết: hợp đồng thuê + dịch vụ đã dùng trong tháng */}
      {detailCompanyId != null && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
          onClick={() => setDetailCompanyId(null)}
          role="dialog"
          aria-modal="true"
          aria-labelledby="detail-modal-title"
        >
          <div
            className="bg-white rounded-2xl shadow-xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between p-6 border-b border-purple-100">
              <h2 id="detail-modal-title" className="text-xl font-bold text-primary">
                Chi tiết chi phí tháng {month}/{year}
              </h2>
              <button
                type="button"
                onClick={() => setDetailCompanyId(null)}
                className="p-2 rounded-lg hover:bg-purple-100 text-text focus:outline-none focus:ring-2 focus:ring-primary"
                aria-label="Đóng"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="p-6 overflow-y-auto flex-1 space-y-6">
              {detailLoading ? (
                <div className="flex justify-center py-12">
                  <div className="animate-spin rounded-full h-10 w-10 border-4 border-primary border-t-transparent" />
                </div>
              ) : detailData ? (
                <>
                  {detailData.company && (
                    <p className="text-lg font-semibold text-text">
                      {detailData.company.name}
                      {detailData.company.tax_code && (
                        <span className="text-text/60 font-normal ml-2">MST: {detailData.company.tax_code}</span>
                      )}
                    </p>
                  )}

                  {/* Hợp đồng thuê */}
                  <section>
                    <h3 className="flex items-center gap-2 text-base font-semibold text-text mb-3">
                      <FileText className="w-4 h-4 text-primary" />
                      Hợp đồng thuê văn phòng
                    </h3>
                    {!detailData.contracts?.length ? (
                      <p className="text-sm text-text/60">Không có hợp đồng active trong tháng này.</p>
                    ) : (
                      <div className="border border-purple-100 rounded-xl overflow-hidden">
                        <table className="w-full text-sm">
                          <thead className="bg-purple-50">
                            <tr>
                              <th className="text-left p-3 font-medium text-text">Văn phòng</th>
                              <th className="text-left p-3 font-medium text-text">Từ ngày</th>
                              <th className="text-left p-3 font-medium text-text">Đến ngày</th>
                              <th className="text-right p-3 font-medium text-text">Giá thuê/tháng</th>
                              <th className="text-left p-3 font-medium text-text">Trạng thái</th>
                            </tr>
                          </thead>
                          <tbody>
                            {detailData.contracts.map((c) => (
                              <tr key={c.id} className="border-t border-purple-100">
                                <td className="p-3">
                                  <span className="font-medium">{c.office_name || `VP #${c.office_id}`}</span>
                                </td>
                                <td className="p-3 text-text/80">{formatDate(c.from_date)}</td>
                                <td className="p-3 text-text/80">{formatDate(c.end_date)}</td>
                                <td className="p-3 text-right font-medium">{formatCurrency(c.rent_price)}</td>
                                <td className="p-3">
                                  <span
                                    className={`px-2 py-0.5 rounded text-xs ${
                                      c.status === 'active'
                                        ? 'bg-green-100 text-green-800'
                                        : c.status === 'expired'
                                          ? 'bg-gray-100 text-gray-700'
                                          : 'bg-red-100 text-red-800'
                                    }`}
                                  >
                                    {c.status === 'active' ? 'Đang thuê' : c.status === 'expired' ? 'Hết hạn' : 'Chấm dứt'}
                                  </span>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </section>

                  {/* Dịch vụ (theo tháng + theo ngày gộp một mục) */}
                  {detailData.service_details && (() => {
                    const monthly = parseServiceArray(detailData.service_details.monthly_services);
                    const hasServices = monthly.length > 0;
                    return (
                      <section>
                        <h3 className="flex items-center gap-2 text-base font-semibold text-text mb-3">
                          <Building2 className="w-4 h-4 text-primary" />
                          Dịch vụ (tháng {month}/{year})
                        </h3>
                        {!hasServices ? (
                          <p className="text-sm text-text/60">Không có dịch vụ trong tháng.</p>
                        ) : (
                          <div className="border border-purple-100 rounded-xl overflow-hidden">
                            <table className="w-full text-sm">
                              <thead className="bg-purple-50">
                                <tr>
                                  <th className="text-left p-3 font-medium text-text">Dịch vụ</th>
                                  <th className="text-right p-3 font-medium text-text">Số lượng</th>
                                  <th className="text-right p-3 font-medium text-text">Đơn giá</th>
                                  <th className="text-right p-3 font-medium text-text">Thành tiền</th>
                                </tr>
                              </thead>
                              <tbody>
                                {monthly.map((row, idx) => (
                                  <tr key={idx} className="border-t border-purple-100">
                                    <td className="p-3 font-medium">{row.service_name}</td>
                                    <td className="p-3 text-right">{formatNumber(row.quantity)}</td>
                                    <td className="p-3 text-right">{formatCurrency(row.unit_price)}</td>
                                    <td className="p-3 text-right font-medium">{formatCurrency(row.total_cost)}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        )}
                      </section>
                    );
                  })()}
                </>
              ) : (
                <p className="text-text/60">Không tải được chi tiết.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Costs;
