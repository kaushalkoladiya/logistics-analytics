import Link from 'next/link';
import { 
  LayoutDashboard, 
  Truck, 
  Package, 
  BarChart3, 
  CreditCard
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  currentPath: string;
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Shipments', href: '/shipments', icon: Package },
  { name: 'Vehicles', href: '/vehicles', icon: Truck },
  { name: 'Routes', href: '/routes', icon: BarChart3 },
  { name: 'Costs', href: '/costs', icon: CreditCard }
];

export function Sidebar({ isOpen, currentPath }: SidebarProps) {
  return (
    <aside className={cn(
      "fixed left-0 top-0 z-40 h-screen border-r bg-white transition-all duration-300",
      isOpen ? "w-64" : "w-16"
    )}>
      <div className="flex h-16 items-center justify-center border-b">
        {isOpen ? (
          <h1 className="text-xl font-bold text-sky-500">Logistics</h1>
        ) : (
          <span className="text-xl font-bold text-sky-500">L</span>
        )}
      </div>
      
      <nav className={cn(isOpen ? "p-4" : "p-1")}>
        {navigation.map((item) => {
          const isActive = currentPath === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "mb-1 flex items-center rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive 
                  ? "bg-sky-50 text-sky-500" 
                  : "text-slate-700 hover:bg-slate-50",
                !isOpen && "justify-center"
              )}
            >
              <item.icon className={cn("h-5 w-5", !isOpen && "mr-0")} />
              {isOpen && <span className="ml-3">{item.name}</span>}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}