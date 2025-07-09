import { cn } from '@/lib/utils';

export function RoleBadge({ role }: { role: 'parent' | 'child' | 'guest' }) {
  const color = {
    parent: 'bg-purple-600/20 text-purple-700',
    child: 'bg-green-600/20 text-green-700',
    guest: 'bg-yellow-600/20 text-yellow-700',
  }[role];

  return (
    <span className={cn('rounded px-2 py-0.5 text-xs font-medium', color)}>{role}</span>
  );
} 