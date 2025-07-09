import { Route, Routes, Navigate, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import { ChoreDashboard } from './features/chores';
import { TransactionLedger } from './features/transactions';
import { AssetPortfolio, VirtualExchange } from './features/assets';
import { FamilyAdmin } from './features/families';
import AdminPage from './features/admin/AdminPage';
import { AppLayout } from './components/layout/AppLayout';
import { RequireAuth } from './components/RequireAuth';

const Home = () => (
  <div className="p-4">
    <h1 className="text-xl font-bold">FamPlus</h1>
    <p className="mt-2">Frontend is ready!</p>
    <p className="mt-2">
      <Link to="/app/chores" className="underline text-blue-600">
        Go to Chores
      </Link>
    </p>
    <p className="mt-2">
      <Link to="/app/transactions" className="underline text-blue-600">
        Go to Transactions
      </Link>
    </p>
    <p className="mt-2">
      <Link to="/app/assets" className="underline text-blue-600">
        Go to Assets
      </Link>
    </p>
    <p className="mt-2">
      <Link to="/app/families" className="underline text-blue-600">
        Go to Families
      </Link>
    </p>
  </div>
);

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/app" replace />} />

      <Route path="/login" element={<LoginPage />} />

      <Route path="/app" element={<AppLayout />}>
        <Route element={<RequireAuth />}>
          <Route index element={<Home />} />
          <Route path="chores" element={<ChoreDashboard />} />
          <Route path="transactions" element={<TransactionLedger />} />
          <Route path="assets" element={<AssetPortfolio />} />
          <Route path="exchange" element={<VirtualExchange />} />
          <Route path="families" element={<FamilyAdmin />} />
          <Route path="admin" element={<AdminPage />} />
        </Route>
      </Route>

      <Route
        path="*"
        element={
          <div className="p-4">
            Page not found. <Link to="/app">Go Home</Link>
          </div>
        }
      />
    </Routes>
  );
}
