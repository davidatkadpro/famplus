import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../../lib/api';
import { Select } from '@/components/ui/select';
import { ResponsiveTable } from '@/components/ui/responsive-table';

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

  const { data: categories } = useQuery<Category[]>({
    queryKey: ['categories'],
    queryFn: async () => {
      const res = await api.get('/categories/');
      return res.data as Category[];
    },
  });

  const {
    data: transactions,
    isLoading,
  } = useQuery<Transaction[]>({
    queryKey: ['transactions', categoryFilter],
    queryFn: async () => {
      const res = await api.get('/transactions/', {
        params: categoryFilter === 'all' ? {} : { category: categoryFilter },
      });
      return res.data as Transaction[];
    },
  });

  const updateCategory = useMutation({
    mutationFn: ({ id, category }: { id: number; category: number | null }) =>
      api.patch(`/transactions/${id}/`, { category }),
    onSuccess: () =>
      queryClient.invalidateQueries({ queryKey: ['transactions', categoryFilter] }),
  });

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Transaction Ledger</h1>
      <div className="mb-4">
        <label className="mr-2">Filter by Category:</label>
        <Select
          value={categoryFilter as string}
          onChange={(e) =>
            setCategoryFilter(
              (e.target as HTMLSelectElement).value === 'all'
                ? 'all'
                : Number((e.target as HTMLSelectElement).value),
            )
          }
          className="w-40"
        >
          <option value="all">All</option>
          {categories?.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </Select>
      </div>
      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <ResponsiveTable
          data={transactions ?? []}
          columns={[
            {
              header: 'ID',
              cell: (tx) => tx.id,
              mobileLabel: 'ID',
            },
            {
              header: 'Description',
              cell: (tx) => tx.description,
            },
            {
              header: 'Amount',
              cell: (tx) => tx.amount,
            },
            {
              header: 'Category',
              cell: (tx) => (
                <Select
                  value={(tx.category ?? '').toString()}
                  onChange={(e) =>
                    updateCategory.mutate({
                      id: tx.id,
                      category: (e.target as HTMLSelectElement).value
                        ? Number((e.target as HTMLSelectElement).value)
                        : null,
                    })
                  }
                  className="w-32"
                >
                  <option value="">None</option>
                  {categories?.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </Select>
              ),
            },
          ]}
        />
      )}
    </div>
  );
}
