import { SidebarProvider } from '../ui/sidebar';
import { AppSidebar } from '../app-sidebar';
import { TopBar } from '../top-bar';
import { ThemeToggle } from '../ThemeToggle';
import { Outlet } from 'react-router-dom';

export function AppLayout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <div className="flex min-h-screen flex-col lg:pl-64">
        <TopBar />
        <main className="flex-1 px-4 py-6 lg:px-6 lg:py-8">
          <Outlet />
        </main>
        <ThemeToggle />
      </div>
    </SidebarProvider>
  );
} 