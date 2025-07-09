import { useState } from 'react';
import { ChoresAdmin } from './ChoresAdmin';
import { AccountsAdmin } from './AccountsAdmin';
import { Button } from '@/components/ui/button';

type Tab = 'chores' | 'accounts';

export default function AdminPage() {
  const [tab, setTab] = useState<Tab>('chores');
  return (
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">Family Admin</h1>
      <div className="flex gap-2">
        <Button variant={tab === 'chores' ? 'default' : 'secondary'} onClick={() => setTab('chores')}>
          Chores
        </Button>
        <Button variant={tab === 'accounts' ? 'default' : 'secondary'} onClick={() => setTab('accounts')}>
          Accounts
        </Button>
      </div>
      {tab === 'chores' && <ChoresAdmin />}
      {tab === 'accounts' && <AccountsAdmin />}
    </div>
  );
} 