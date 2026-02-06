import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Users, Phone, Mail } from 'lucide-react';
import { companiesAPI } from '../api/client';

const Companies = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingCompany, setEditingCompany] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    tax_code: '',
    field: '',
    phone: '',
    email: '',
  });

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await companiesAPI.getAll();
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies:', error);
      alert('Lỗi tải danh sách công ty');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCompany) {
        await companiesAPI.update(editingCompany.id, formData);
        alert('Cập nhật công ty thành công!');
      } else {
        await companiesAPI.create(formData);
        alert('Thêm công ty thành công!');
      }
      setShowModal(false);
      setEditingCompany(null);
      setFormData({ name: '', tax_code: '', field: '', phone: '', email: '' });
      fetchCompanies();
    } catch (error) {
      console.error('Error saving company:', error);
      alert('Lỗi lưu công ty');
    }
  };

  const handleEdit = (company) => {
    setEditingCompany(company);
    setFormData({
      name: company.name,
      tax_code: company.tax_code,
      field: company.field || '',
      phone: company.phone || '',
      email: company.email || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('Bạn có chắc muốn xóa công ty này?')) return;
    try {
      await companiesAPI.delete(id);
      alert('Xóa công ty thành công!');
      fetchCompanies();
    } catch (error) {
      console.error('Error deleting company:', error);
      alert('Lỗi xóa công ty');
    }
  };

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
          <h1 className="text-4xl font-bold text-primary">Công ty</h1>
          <p className="text-text/60 mt-2">Quản lý danh sách công ty thuê văn phòng</p>
        </div>
        <button
          onClick={() => {
            setEditingCompany(null);
            setFormData({ name: '', tax_code: '', field: '', phone: '', email: '' });
            setShowModal(true);
          }}
          className="flex items-center space-x-2 bg-primary text-white px-6 py-3 rounded-xl hover:bg-purple-700 transition-colors duration-200 cursor-pointer shadow-lg"
        >
          <Plus className="w-5 h-5" />
          <span className="font-medium">Thêm công ty</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {companies.map((company) => (
          <div
            key={company.id}
            className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg hover:shadow-xl transition-all duration-300"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="bg-blue-50 p-3 rounded-xl">
                  <Users className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-text">{company.name}</h3>
                  <p className="text-sm text-text/60">MST: {company.tax_code}</p>
                </div>
              </div>
            </div>

            <div className="space-y-2 text-sm text-text/80">
              {company.field && (
                <p>
                  <span className="font-medium">Lĩnh vực:</span> {company.field}
                </p>
              )}
              {company.phone && (
                <div className="flex items-center space-x-2">
                  <Phone className="w-4 h-4 text-primary" />
                  <span>{company.phone}</span>
                </div>
              )}
              {company.email && (
                <div className="flex items-center space-x-2">
                  <Mail className="w-4 h-4 text-primary" />
                  <span>{company.email}</span>
                </div>
              )}
            </div>

            <div className="flex space-x-2 mt-4 pt-4 border-t border-purple-100">
              <button
                onClick={() => handleEdit(company)}
                className="flex items-center justify-center space-x-1 flex-1 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors duration-200 cursor-pointer"
              >
                <Edit className="w-4 h-4" />
                <span className="text-sm font-medium">Sửa</span>
              </button>
              <button
                onClick={() => handleDelete(company.id)}
                className="flex items-center justify-center space-x-1 flex-1 px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors duration-200 cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
                <span className="text-sm font-medium">Xóa</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold text-primary mb-6">
              {editingCompany ? 'Sửa công ty' : 'Thêm công ty mới'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text mb-2">Tên công ty</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Công ty ABC"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text mb-2">Mã số thuế</label>
                <input
                  type="text"
                  required
                  value={formData.tax_code}
                  onChange={(e) => setFormData({ ...formData, tax_code: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="0123456789"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text mb-2">Lĩnh vực</label>
                <input
                  type="text"
                  value={formData.field}
                  onChange={(e) => setFormData({ ...formData, field: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Công nghệ thông tin"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text mb-2">Số điện thoại</label>
                <input
                  type="text"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="0123456789"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text mb-2">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="contact@company.com"
                />
              </div>
              <div className="flex space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2 border border-purple-200 text-text rounded-lg hover:bg-purple-50 transition-colors duration-200 cursor-pointer"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-purple-700 transition-colors duration-200 cursor-pointer"
                >
                  {editingCompany ? 'Cập nhật' : 'Thêm'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Companies;
