import { createContext, useContext, useState, ReactNode } from 'react';
import { cn } from '@/lib/utils';
import { Menu } from 'lucide-react';

interface SidebarContextValue {
  open: boolean;
  toggle: () => void;
  setOpen: (v: boolean) => void;
}

const SidebarContext = createContext<SidebarContextValue | undefined>(undefined);

export function SidebarProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const toggle = () => setOpen((v) => !v);

  return (
    <SidebarContext.Provider value={{ open, toggle, setOpen }}>
      {children}
    </SidebarContext.Provider>
  );
}

export function useSidebar() {
  const ctx = useContext(SidebarContext);
  if (!ctx) throw new Error('useSidebar must be used within SidebarProvider');
  return ctx;
}

export function Sidebar({ className, children }: { className?: string; children: ReactNode }) {
  const { open, setOpen } = useSidebar();
  return (
    <>
      {/* Drawer */}
      <aside
        className={cn(
          'fixed inset-y-0 left-0 z-40 w-64 transform border-r border-border bg-sidebar text-sidebar-foreground transition-transform lg:translate-x-0',
          open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0',
          className,
        )}
      >
        {children}
      </aside>

      {/* Backdrop */}
      <div
        className={cn(
          'fixed inset-0 z-30 bg-black/50 transition-opacity lg:hidden',
          open ? 'opacity-50 pointer-events-auto' : 'opacity-0 pointer-events-none',
        )}
        onClick={() => setOpen(false)}
      />
    </>
  );
}

export function SidebarTrigger({ className }: { className?: string }) {
  const { toggle } = useSidebar();
  return (
    <button
      type="button"
      onClick={toggle}
      className={cn(
        'mr-2 inline-flex h-10 w-10 items-center justify-center rounded-md bg-accent text-accent-foreground transition-colors hover:bg-accent/80 lg:hidden',
        className,
      )}
      aria-label="Toggle sidebar"
    >
      <Menu className="h-5 w-5" />
    </button>
  );
} 