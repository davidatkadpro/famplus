import { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  CategoryScale,
  Chart as ChartJS,
  LineElement,
  LinearScale,
  PointElement,
  TimeScale,
  Tooltip,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import { useQuery } from '@tanstack/react-query';
import { api } from '../../lib/api';

interface Asset {
  id: number;
  name: string;
  symbol: string;
  current_price: string | null;
}

interface Price {
  id: number;
  asset: number;
  value: string;
  timestamp: string;
}

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  TimeScale,
  Tooltip,
);

export default function AssetPortfolio() {
  const [selected, setSelected] = useState<number | null>(null);

  const { data: assets, isLoading } = useQuery<Asset[]>(
    ['assets'],
    async () => {
      const res = await api.get('/assets/');
      return res.data as Asset[];
    },
  );

  const { data: prices } = useQuery<Price[]>(['prices', selected], async () => {
    if (!selected) return [] as Price[];
    const res = await api.get('/asset-prices/', {
      params: { asset: selected },
    });
    return res.data as Price[];
  });

  const chartData = {
    labels: prices?.map((p) => p.timestamp) ?? [],
    datasets: [
      {
        label: 'Price',
        data: prices?.map((p) => p.value) ?? [],
        borderColor: 'rgb(37, 99, 235)',
        backgroundColor: 'rgba(37, 99, 235, 0.4)',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    parsing: false,
    scales: {
      x: {
        type: 'time' as const,
        time: { unit: 'day' as const },
      },
    },
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Asset Portfolio</h1>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table className="min-w-full border mb-4">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">Symbol</th>
              <th className="p-2 text-left">Name</th>
              <th className="p-2 text-left">Current Price</th>
            </tr>
          </thead>
          <tbody>
            {assets?.map((asset) => (
              <tr
                key={asset.id}
                className="border-t hover:bg-gray-50 cursor-pointer"
                onClick={() => setSelected(asset.id)}
              >
                <td className="p-2">{asset.symbol}</td>
                <td className="p-2">{asset.name}</td>
                <td className="p-2">{asset.current_price ?? '–'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {selected && prices && prices.length > 0 && (
        <div className="w-full max-w-xl">
          <Line data={chartData} options={chartOptions} />
        </div>
      )}
    </div>
  );
}
