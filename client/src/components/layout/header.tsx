import { Menu, Bell, User } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface HeaderProps {
  toggleSidebar: () => void;
}

export function Header({ toggleSidebar }: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 h-16 border-b bg-white shadow-sm">
      <div className="flex h-full items-center justify-between px-4">
        <div className="flex items-center">
          <Button 
            variant="ghost" 
            size="icon"
            onClick={toggleSidebar}
            className="mr-4 text-slate-700 hover:bg-sky-50"
          >
            <Menu className="h-5 w-5" />
          </Button>
        </div>
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="icon" className="text-slate-700 hover:bg-sky-50">
            <Bell className="h-5 w-5" />
          </Button>
          <Button variant="ghost" size="icon" className="text-slate-700 hover:bg-sky-50">
            <User className="h-5 w-5" />
          </Button>
        </div>
      </div>
    </header>
  );
}