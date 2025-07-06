import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../../lib/api';

interface Transaction {
  id: number;
  description: string;
  amount: string;
  debit_account: number;
  credit_account: number;
  category: number | null;
}

interface Category {
  id: number;
  name: string;
}

export default function TransactionLedger() {
  const queryClient = useQueryClient();
  const [categoryFilter, setCategoryFilter] = useState<number | 'all'>('all');

  const { data: categories } = useQuery<Category[]>(
    ['categories'],
    async () => {
      const res = await api.get('/categories/');
      return res.data as Category[];
    },
  );

  const { data: transactions, isLoading } = useQuery<Transaction[]>(
    ['transactions', categoryFilter],
    async () => {
      const res = await api.get('/transactions/', {
        params: categoryFilter === 'all' ? {} : { category: categoryFilter },
      });
      return res.data as Transaction[];
    },
  );

  const updateCategory = useMutation(
    ({ id, category }: { id: number; category: number | null }) =>
      api.patch(`/transactions/${id}/`, { category }),
    {
      onSuccess: () =>
        queryClient.invalidateQueries(['transactions', categoryFilter]),
    },
  );

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Transaction Ledger</h1>
      <div className="mb-4">
        <label className="mr-2">Filter by Category:</label>
        <select
          value={categoryFilter}
          onChange={(e) =>
            setCategoryFilter(
              e.target.value === 'all' ? 'all' : Number(e.target.value),
            )
          }
          className="border px-2 py-1"
        >
          <option value="all">All</option>
          {categories?.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
      </div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 text-left">ID</th>
              <th className="p-2 text-left">Description</th>
              <th className="p-2 text-left">Amount</th>
              <th className="p-2 text-left">Category</th>
            </tr>
          </thead>
          <tbody>
            {transactions?.map((tx) => (
              <tr key={tx.id} className="border-t">
                <td className="p-2">{tx.id}</td>
                <td className="p-2">{tx.description}</td>
                <td className="p-2">{tx.amount}</td>
                <td className="p-2">
                  <select
                    value={tx.category ?? ''}
                    onChange={(e) =>
                      updateCategory.mutate({
                        id: tx.id,
                        category: e.target.value
                          ? Number(e.target.value)
                          : null,
                      })
                    }
                    className="border px-2 py-1"
                  >
                    <option value="">None</option>
                    {categories?.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.name}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
