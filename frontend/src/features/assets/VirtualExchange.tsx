import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { Card, CardHeader, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select } from '@/components/ui/select';
import { Table } from '@/components/ui/table';

interface Asset {
  id: number;
  symbol: string;
}

interface Order {
  id: number;
  asset: number;
  side: 'buy' | 'sell';
  quantity: string;
  price: string;
  remaining: string;
  status: string;
  created_at: string;
}

interface Trade {
  id: number;
  asset: number;
  price: string;
  quantity: string;
  timestamp: string;
}

export default function VirtualExchange() {
  const qc = useQueryClient();
  const [side, setSide] = useState<'buy' | 'sell'>('buy');
  const [assetId, setAssetId] = useState<number | null>(null);
  const [qty, setQty] = useState('');
  const [price, setPrice] = useState('');

  const { data: assets } = useQuery<Asset[]>({
    queryKey: ['assets'],
    queryFn: async () => (await api.get('/assets/')).data,
  });

  const { data: orders } = useQuery<Order[]>({
    queryKey: ['orders', assetId],
    queryFn: async () => (await api.get('/exchange-orders/', { params: { asset: assetId } })).data,
    enabled: assetId != null,
  });

  const { data: trades } = useQuery<Trade[]>({
    queryKey: ['trades', assetId],
    queryFn: async () => (await api.get('/exchange-trades/', { params: { asset: assetId } })).data,
    enabled: assetId != null,
  });

  // order book (all open orders)
  const { data: book } = useQuery<Order[]>({
    queryKey: ['orderbook', assetId],
    queryFn: async () => (await api.get('/exchange-orders/', { params: { asset: assetId, book: 1 } })).data,
    enabled: assetId != null,
    staleTime: 5000,
    refetchInterval: 5000,
  });

  const createOrder = useMutation({
    mutationFn: async () =>
      api.post('/exchange-orders/', {
        asset: assetId,
        side,
        quantity: qty,
        price,
      }),
    onSuccess: () => {
      setQty('');
      qc.invalidateQueries({ queryKey: ['orders'] });
      qc.invalidateQueries({ queryKey: ['trades'] });
    },
  });

  const cancelOrder = useMutation({
    mutationFn: (id: number) => api.patch(`/exchange-orders/${id}/`, { status: 'cancelled' }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['orders'] });
      qc.invalidateQueries({ queryKey: ['orderbook'] });
    },
  });

  return (
    <Card>
      <CardHeader>
        <h2 className="text-lg font-semibold">Virtual Exchange</h2>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap items-end gap-3">
          <Select
            value={(assetId ?? '').toString()}
            onChange={(e) => setAssetId(Number((e.target as HTMLSelectElement).value))}
            className="w-40"
          >
            <option value="">Select Asset</option>
            {assets?.map((a) => (
              <option key={a.id} value={a.id}>
                {a.symbol}
              </option>
            ))}
          </Select>

          <Select
            value={side}
            onChange={(e) => setSide((e.target as HTMLSelectElement).value as 'buy' | 'sell')}
            className="w-28"
          >
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </Select>
          <Input placeholder="Quantity" value={qty} onChange={(e) => setQty(e.target.value)} className="w-28" />
          <Input placeholder="Price" value={price} onChange={(e) => setPrice(e.target.value)} className="w-28" />
          <Button disabled={!assetId || !qty || !price} onClick={() => createOrder.mutate()}>
            Place Order
          </Button>
        </div>

        {orders && (
          <div className="mt-6">
            <h3 className="mb-2 font-medium">My Orders</h3>
            <Table>
              <thead>
                <tr className="border-b bg-muted/50 text-muted-foreground">
                  <th className="px-2 py-1 text-left">Side</th>
                  <th className="px-2 py-1 text-left">Qty</th>
                  <th className="px-2 py-1 text-left">Rem</th>
                  <th className="px-2 py-1 text-left">Price</th>
                  <th className="px-2 py-1 text-left">Status</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((o) => (
                  <tr key={o.id} className="border-b">
                    <td className="px-2 py-1">{o.side}</td>
                    <td className="px-2 py-1">{o.quantity}</td>
                    <td className="px-2 py-1">{o.remaining}</td>
                    <td className="px-2 py-1">{o.price}</td>
                    <td className="px-2 py-1 flex gap-2 items-center">
                      {o.status}
                      {['open', 'partial'].includes(o.status) && (
                        <Button variant="link" size="sm" onClick={() => cancelOrder.mutate(o.id)}>
                          Cancel
                        </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        )}

        {trades && (
          <div className="mt-6">
            <h3 className="mb-2 font-medium">Recent Trades</h3>
            <Table>
              <thead>
                <tr className="border-b bg-muted/50 text-muted-foreground">
                  <th className="px-2 py-1 text-left">Qty</th>
                  <th className="px-2 py-1 text-left">Price</th>
                  <th className="px-2 py-1 text-left">Time</th>
                </tr>
              </thead>
              <tbody>
                {trades.map((t) => (
                  <tr key={t.id} className="border-b">
                    <td className="px-2 py-1">{t.quantity}</td>
                    <td className="px-2 py-1">{t.price}</td>
                    <td className="px-2 py-1">{new Date(t.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        )}

        {book && (
          <div className="mt-10 grid grid-cols-2 gap-8">
            <div>
              <h3 className="mb-2 font-medium text-red-600">Asks (Sell)</h3>
              <Table>
                <thead>
                  <tr className="border-b bg-muted/50 text-muted-foreground">
                    <th className="px-2 py-1 text-left">Price</th>
                    <th className="px-2 py-1 text-left">Qty</th>
                  </tr>
                </thead>
                <tbody>
                  {book
                    .filter((o) => o.side === 'sell')
                    .sort((a, b) => parseFloat(a.price) - parseFloat(b.price))
                    .map((o) => (
                      <tr key={o.id} className="border-b">
                        <td className="px-2 py-1">{o.price}</td>
                        <td className="px-2 py-1">{o.remaining}</td>
                      </tr>
                    ))}
                </tbody>
              </Table>
            </div>
            <div>
              <h3 className="mb-2 font-medium text-green-600">Bids (Buy)</h3>
              <Table>
                <thead>
                  <tr className="border-b bg-muted/50 text-muted-foreground">
                    <th className="px-2 py-1 text-left">Price</th>
                    <th className="px-2 py-1 text-left">Qty</th>
                  </tr>
                </thead>
                <tbody>
                  {book
                    .filter((o) => o.side === 'buy')
                    .sort((a, b) => parseFloat(b.price) - parseFloat(a.price))
                    .map((o) => (
                      <tr key={o.id} className="border-b">
                        <td className="px-2 py-1">{o.price}</td>
                        <td className="px-2 py-1">{o.remaining}</td>
                      </tr>
                    ))}
                </tbody>
              </Table>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
} 