import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Offices from './pages/Offices';
import Companies from './pages/Companies';
import Costs from './pages/Costs';
import Salaries from './pages/Salaries';
import Reports from './pages/Reports';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="offices" element={<Offices />} />
          <Route path="companies" element={<Companies />} />
          <Route path="costs" element={<Costs />} />
          <Route path="salaries" element={<Salaries />} />
          <Route path="reports" element={<Reports />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
