import axios from 'axios';

const API_BASE_URL = 'http://localhost:8222/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Offices
export const officesAPI = {
  getAll: (params) => api.get('/offices', { params }),
  getById: (id) => api.get(`/offices/${id}`),
  create: (data) => api.post('/offices', data),
  update: (id, data) => api.put(`/offices/${id}`, data),
  delete: (id) => api.delete(`/offices/${id}`),
};

// Companies
export const companiesAPI = {
  getAll: (params) => api.get('/companies', { params }),
  getById: (id) => api.get(`/companies/${id}`),
  create: (data) => api.post('/companies', data),
  update: (id, data) => api.put(`/companies/${id}`, data),
  delete: (id) => api.delete(`/companies/${id}`),
  getMonthlyCosts: (companyId, month, year) =>
    api.get(`/companies/${companyId}/monthly-costs`, { params: { month, year } }),
  getServiceDetails: (id, month, year) =>
    api.get(`/companies/${id}/service-details`, { params: { month, year } }),
};

// Building Employees
export const employeesAPI = {
  getAll: (params) => api.get('/building-employees', { params }),
  getSalaries: (month, year) =>
    api.get('/building-employees/salaries/monthly', { params: { month, year } }),
};

// Contracts
export const contractsAPI = {
  getAll: (params) => api.get('/contracts', { params }),
};

// Reports
export const reportsAPI = {
  getFinance: (month, year) =>
    api.get('/reports/building-finance', { params: { month, year } }),
  getFinanceDetails: (month, year) =>
    api.get('/reports/building-finance/details', { params: { month, year } }),
};

export default api;
