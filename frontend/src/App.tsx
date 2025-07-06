import { Route, Routes, Link } from 'react-router-dom';

const Home = () => (
  <div className="p-4">
    <h1 className="text-xl font-bold">FamPlus</h1>
    <p className="mt-2">Frontend is ready!</p>
  </div>
);

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
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
