import { SidebarTrigger } from './ui/sidebar';
import { Button } from './ui/button';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';

export function TopBar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-2 border-b border-border bg-background/60 px-4 backdrop-blur lg:px-6">
      <SidebarTrigger />
      <h2 className="text-lg font-semibold">Dashboard</h2>
      <div className="ml-auto flex items-center gap-2">
        {isAuthenticated && (
          <Button
            size="sm"
            variant="secondary"
            onClick={() => {
              logout();
              navigate('/login');
            }}
          >
            Logout
          </Button>
        )}
      </div>
    </header>
  );
} 