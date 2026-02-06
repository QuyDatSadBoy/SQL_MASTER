import { useState, useEffect, useCallback } from 'react';
import { Search, DollarSign, Calendar } from 'lucide-react';
import { companiesAPI } from '../api/client';
import { formatCurrency, getCurrentMonthYear } from '../utils/formatters';

const Costs = () => {
  const [costs, setCosts] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [month, setMonth] = useState(getCurrentMonthYear().month);
  const [year, setYear] = useState(getCurrentMonthYear().year);
  const [selectedCompany, setSelectedCompany] = useState('');

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
              className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-xl font-bold text-text">{cost.company_name}</h3>
                  <p className="text-sm text-text/60 mt-1">MST: {cost.tax_code}</p>

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
    </div>
  );
};

export default Costs;
