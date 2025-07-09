import { Sidebar } from './ui/sidebar';
import { Link, useLocation } from 'react-router-dom';
import { Home, ListChecks, BarChart3, WalletCards, X, Settings } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useSidebar } from './ui/sidebar';

const items = [
  { to: '/app', label: 'Home', icon: Home },
  { to: '/app/chores', label: 'Chores', icon: ListChecks },
  { to: '/app/assets', label: 'Assets', icon: BarChart3 },
  { to: '/app/transactions', label: 'Transactions', icon: WalletCards },
  { to: '/app/exchange', label: 'Exchange', icon: WalletCards },
  { to: '/app/admin', label: 'Admin', icon: Settings },
];

export function AppSidebar() {
  const { pathname } = useLocation();
  const { setOpen } = useSidebar();
  return (
    <Sidebar>
      <div className="flex h-full flex-col gap-2 p-4">
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">FamPlus</h1>
          <button
            type="button"
            className="rounded-md p-1 lg:hidden hover:bg-accent"
            onClick={() => setOpen(false)}
          >
            <X className="h-5 w-5" />
          </button>
        </div>
        <nav className="flex-1 space-y-1">
          {items.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              className={cn(
                'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground',
                pathname === to && 'bg-primary text-primary-foreground',
              )}
              onClick={() => setOpen(false)}
            >
              <Icon className="h-4 w-4" />
              <span>{label}</span>
            </Link>
          ))}
        </nav>
        <p className="text-xs text-muted-foreground">v0.1.0</p>
      </div>
    </Sidebar>
  );
}

export default AppSidebar; 