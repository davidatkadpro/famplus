import { useState, useEffect } from 'react';
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
import { useQuery } from '@tanstack/react-query';
import { api } from '../../lib/api';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ResponsiveTable } from '@/components/ui/responsive-table';

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

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, TimeScale, Tooltip);

export default function AssetPortfolio() {
  const [selected, setSelected] = useState<number | null>(null);

  // Dynamically load date-fns adapter only on this page
  useEffect(() => {
    import('chartjs-adapter-date-fns');
  }, []);

  const { data: assets, isLoading } = useQuery<Asset[]>({
    queryKey: ['assets'],
    queryFn: async () => {
      const res = await api.get('/assets/');
      return res.data as Asset[];
    },
  });

  const { data: prices } = useQuery<Price[]>({
    queryKey: ['prices', selected],
    queryFn: async () => {
      if (!selected) return [] as Price[];
      const res = await api.get('/asset-prices/', { params: { asset: selected } });
      return res.data as Price[];
    },
    enabled: !!selected,
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
    scales: {
      x: {
        type: 'time' as const,
        time: { unit: 'day' as const },
      },
    },
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Assets</h2>
          <div className="flex gap-2">
            <Input placeholder="Search" className="h-8 w-48" />
            <Button size="sm">Add</Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <p>Loading…</p>
        ) : (
          <ResponsiveTable
            data={assets ?? []}
            columns={[
              { header: 'Symbol', cell: (a: Asset) => a.symbol },
              { header: 'Name', cell: (a: Asset) => a.name },
              {
                header: 'Price',
                cell: (a: Asset) => a.current_price ?? '—',
              },
            ]}
            onRowClick={(a: Asset) => setSelected(a.id)}
          />
        )}

        {selected && prices && prices.length > 0 && (
          <div className="mt-6 w-full max-w-xl">
            <Line data={chartData} options={chartOptions} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}
