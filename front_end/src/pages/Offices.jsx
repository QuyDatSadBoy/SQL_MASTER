import { useState, useEffect } from 'react';
import { Plus, Edit, Trash2, Building2 } from 'lucide-react';
import { officesAPI } from '../api/client';
import { formatCurrency, formatNumber } from '../utils/formatters';

const Offices = () => {
  const [offices, setOffices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingOffice, setEditingOffice] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    area: '',
    floor: '',
    position: '',
    base_price: '',
  });

  useEffect(() => {
    fetchOffices();
  }, []);

  const fetchOffices = async () => {
    try {
      const response = await officesAPI.getAll();
      setOffices(response.data);
    } catch (error) {
      console.error('Error fetching offices:', error);
      alert('Lỗi tải danh sách văn phòng');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingOffice) {
        await officesAPI.update(editingOffice.id, formData);
        alert('Cập nhật văn phòng thành công!');
      } else {
        await officesAPI.create(formData);
        alert('Thêm văn phòng thành công!');
      }
      setShowModal(false);
      setEditingOffice(null);
      setFormData({ name: '', area: '', floor: '', position: '', base_price: '' });
      fetchOffices();
    } catch (error) {
      console.error('Error saving office:', error);
      alert('Lỗi lưu văn phòng');
    }
  };

  const handleEdit = (office) => {
    setEditingOffice(office);
    setFormData({
      name: office.name,
      area: office.area,
      floor: office.floor,
      position: office.position || '',
      base_price: office.base_price,
    });
    setShowModal(true);
  };

  const handleDelete = async (id) => {
    if (!confirm('Bạn có chắc muốn xóa văn phòng này?')) return;
    try {
      await officesAPI.delete(id);
      alert('Xóa văn phòng thành công!');
      fetchOffices();
    } catch (error) {
      console.error('Error deleting office:', error);
      alert('Lỗi xóa văn phòng');
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
          <h1 className="text-4xl font-bold text-primary">Văn phòng</h1>
          <p className="text-text/60 mt-2">Quản lý danh sách văn phòng cho thuê</p>
        </div>
        <button
          onClick={() => {
            setEditingOffice(null);
            setFormData({ name: '', area: '', floor: '', position: '', base_price: '' });
            setShowModal(true);
          }}
          className="flex items-center space-x-2 bg-primary text-white px-6 py-3 rounded-xl hover:bg-purple-700 transition-colors duration-200 cursor-pointer shadow-lg"
        >
          <Plus className="w-5 h-5" />
          <span className="font-medium">Thêm văn phòng</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {offices.map((office) => (
          <div
            key={office.id}
            className="bg-white rounded-2xl p-6 border border-purple-100 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="bg-primary/10 p-3 rounded-xl">
                  <Building2 className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-text">{office.name}</h3>
                  <p className="text-sm text-text/60">Tầng {office.floor}</p>
                </div>
              </div>
            </div>

            <div className="space-y-2 text-sm text-text/80">
              <p>
                <span className="font-medium">Diện tích:</span> {formatNumber(office.area)} m²
              </p>
              {office.position && (
                <p>
                  <span className="font-medium">Vị trí:</span> {office.position}
                </p>
              )}
              <p className="text-lg font-bold text-primary mt-3">
                {formatCurrency(office.base_price)}/tháng
              </p>
            </div>

            <div className="flex space-x-2 mt-4 pt-4 border-t border-purple-100">
              <button
                onClick={() => handleEdit(office)}
                className="flex items-center justify-center space-x-1 flex-1 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors duration-200 cursor-pointer"
              >
                <Edit className="w-4 h-4" />
                <span className="text-sm font-medium">Sửa</span>
              </button>
              <button
                onClick={() => handleDelete(office.id)}
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
              {editingOffice ? 'Sửa văn phòng' : 'Thêm văn phòng mới'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-text mb-2">Tên văn phòng</label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="P101"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-text mb-2">Diện tích (m²)</label>
                  <input
                    type="number"
                    step="0.01"
                    required
                    value={formData.area}
                    onChange={(e) => setFormData({ ...formData, area: e.target.value })}
                    className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-text mb-2">Tầng</label>
                  <input
                    type="number"
                    required
                    value={formData.floor}
                    onChange={(e) => setFormData({ ...formData, floor: e.target.value })}
                    className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-text mb-2">Vị trí</label>
                <input
                  type="text"
                  value={formData.position}
                  onChange={(e) => setFormData({ ...formData, position: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="Góc tầng 1"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-text mb-2">Giá thuê (VNĐ/tháng)</label>
                <input
                  type="number"
                  required
                  value={formData.base_price}
                  onChange={(e) => setFormData({ ...formData, base_price: e.target.value })}
                  className="w-full px-4 py-2 border border-purple-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
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
                  {editingOffice ? 'Cập nhật' : 'Thêm'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Offices;
