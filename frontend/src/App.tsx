import { Route, Routes, Link } from 'react-router-dom';
import { ChoreDashboard } from './features/chores';
import { TransactionLedger } from './features/transactions';

const Home = () => (
  <div className="p-4">
    <h1 className="text-xl font-bold">FamPlus</h1>
    <p className="mt-2">Frontend is ready!</p>
    <p className="mt-2">
      <Link to="/chores" className="underline text-blue-600">
        Go to Chores
      </Link>
    </p>
    <p className="mt-2">
      <Link to="/transactions" className="underline text-blue-600">
        Go to Transactions
      </Link>
    </p>
  </div>
);

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/chores" element={<ChoreDashboard />} />
      <Route path="/transactions" element={<TransactionLedger />} />
      <Route
        path="*"
        element={
          <div className="p-4">
            Page not found. <Link to="/">Go Home</Link>
          </div>
        }
      />
    </Routes>
  );
}
