import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import { ResponsiveTable } from '@/components/ui/responsive-table';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';

interface Account {
  id: number;
  name: string;
  type: string;
  owner: number | null;
}

interface Member {
  id: number;
  user: number;
}

export function AccountsAdmin() {
  const qc = useQueryClient();
  const [filter, setFilter] = useState<number | 'all'>('all');
  const [name, setName] = useState('');
  const [type, setType] = useState('asset');
  const [owner, setOwner] = useState<number | ''>('');

  const { data: members } = useQuery<Member[]>({
    queryKey: ['members'],
    queryFn: async () => (await api.get('/family-memberships/')).data,
  });

  const { data: accounts, isLoading } = useQuery<Account[]>({
    queryKey: ['accounts-admin', filter],
    queryFn: async () => {
      const params = filter === 'all' ? {} : { owner: filter };
      return (await api.get('/accounts/', { params })).data;
    },
  });

  const addAccount = useMutation({
    mutationFn: () =>
      api.post('/accounts/', { name, type, owner: owner || null }),
    onSuccess: () => {
      setName('');
      setOwner('');
      qc.invalidateQueries({ queryKey: ['accounts-admin'] });
    },
  });

  const deleteAccount = useMutation({
    mutationFn: (id: number) => api.delete(`/accounts/${id}/`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['accounts-admin'] }),
  });

  return (
    <div className="space-y-4">
      <div className="flex items-end gap-2">
        <Input
          placeholder="Account name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <Select value={type} onChange={(e) => setType((e.target as HTMLSelectElement).value)} className="w-32">
          <option value="asset">Asset</option>
          <option value="expense">Expense</option>
          <option value="liability">Liability</option>
          <option value="equity">Equity</option>
          <option value="revenue">Revenue</option>
        </Select>
        <Select
          value={owner.toString()}
          onChange={(e) => setOwner(Number((e.target as HTMLSelectElement).value))}
          className="w-40"
        >
          <option value="">Family</option>
          {members?.map((m) => (
            <option key={m.id} value={m.user}>
              {m.user}
            </option>
          ))}
        </Select>
        <Button variant="secondary" disabled={!name} onClick={() => addAccount.mutate()}>
          Add
        </Button>
      </div>

      <div>
        <label className="mr-2">Filter:</label>
        <Select
          value={filter.toString()}
          onChange={(e) =>
            setFilter(
              (e.target as HTMLSelectElement).value === 'all'
                ? 'all'
                : Number((e.target as HTMLSelectElement).value),
            )
          }
          className="w-40"
        >
          <option value="all">All</option>
          {members?.map((m) => (
            <option key={m.id} value={m.user}>
              {m.user}
            </option>
          ))}
        </Select>
      </div>

      {isLoading ? (
        <p>Loading…</p>
      ) : (
        <ResponsiveTable
          data={accounts ?? []}
          columns={[
            { header: 'Name', cell: (a: Account) => a.name },
            { header: 'Type', cell: (a: Account) => a.type },
            { header: 'Owner', cell: (a: Account) => a.owner ?? 'Family' },
            {
              header: '',
              cell: (a: Account) => (
                <Button variant="link" size="sm" onClick={() => deleteAccount.mutate(a.id)}>
                  Delete
                </Button>
              ),
              hideOnMobile: true,
            },
          ]}
        />
      )}
    </div>
  );
} 