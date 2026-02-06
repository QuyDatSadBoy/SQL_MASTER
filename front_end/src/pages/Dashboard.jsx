import { useState, useEffect } from 'react';
import { Building2, Users, DollarSign, TrendingUp } from 'lucide-react';
import { officesAPI, companiesAPI, reportsAPI } from '../api/client';
import { formatCurrency, getCurrentMonthYear } from '../utils/formatters';

const Dashboard = () => {
  const [stats, setStats] = useState({
    offices: 0,
    companies: 0,
    revenue: 0,
    profit: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const { month, year } = getCurrentMonthYear();
      const [officesRes, companiesRes, financeRes] = await Promise.all([
        officesAPI.getAll(),
        companiesAPI.getAll(),
        reportsAPI.getFinance(month, year),
      ]);

      setStats({
        offices: officesRes.data.length,
        companies: companiesRes.data.length,
        revenue: financeRes.data.total_revenue,
        profit: financeRes.data.net_profit,
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    {
      icon: Building2,
      label: 'Văn phòng',
      value: stats.offices,
      color: 'bg-purple-500',
    },
    {
      icon: Users,
      label: 'Công ty',
      value: stats.companies,
      color: 'bg-blue-500',
    },
    {
      icon: DollarSign,
      label: 'Doanh thu',
      value: formatCurrency(stats.revenue),
      color: 'bg-green-500',
    },
    {
      icon: TrendingUp,
      label: 'Lợi nhuận',
      value: formatCurrency(stats.profit),
      color: 'bg-orange-500',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-primary">Tổng quan</h1>
          <p className="text-text/60 mt-2">Hệ thống quản lý tòa nhà văn phòng</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => {
          const IconComponent = card.icon;
          return (
            <div
              key={index}
              className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-text/60 font-medium">{card.label}</p>
                  <p className="text-2xl font-bold text-text mt-2">{card.value}</p>
                </div>
                <div className={`${card.color} p-3 rounded-xl`}>
                  <IconComponent className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-linear-to-br from-primary to-purple-600 rounded-2xl p-8 text-white shadow-lg">
        <h2 className="text-2xl font-bold mb-4">Chào mừng đến với Office Manager</h2>
        <p className="text-white/90 text-lg">
          Quản lý văn phòng, công ty, hợp đồng và tài chính một cách hiệu quả
        </p>
      </div>
    </div>
  );
};

export default Dashboard;
