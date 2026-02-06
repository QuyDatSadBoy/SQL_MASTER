import { Link, useLocation } from 'react-router-dom';
import { Building2, Users, DollarSign, FileText, BarChart3, Home } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', icon: Home, label: 'Tổng quan' },
    { path: '/offices', icon: Building2, label: 'Văn phòng' },
    { path: '/companies', icon: Users, label: 'Công ty' },
    { path: '/costs', icon: DollarSign, label: 'Chi phí' },
    { path: '/salaries', icon: FileText, label: 'Lương' },
    { path: '/reports', icon: BarChart3, label: 'Báo cáo' },
  ];

  return (
    <nav className="fixed top-4 left-4 right-4 bg-white/90 backdrop-blur-lg border border-purple-100 rounded-2xl shadow-xl z-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-2">
            <Building2 className="w-8 h-8 text-primary" />
            <span className="text-xl font-bold text-primary">Office Manager</span>
          </div>

          <div className="flex space-x-1">
            {navItems.map(({ path, icon: Icon, label }) => (
              <Link
                key={path}
                to={path}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 cursor-pointer ${
                  location.pathname === path
                    ? 'bg-primary text-white'
                    : 'text-text hover:bg-purple-50'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
