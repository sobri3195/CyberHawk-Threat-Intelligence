import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Shield, 
  Activity, 
  Search, 
  BarChart3, 
  Menu, 
  X,
  Globe,
  AlertTriangle
} from 'lucide-react';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const navItems = [
    { path: '/dashboard', icon: Activity, label: 'Dashboard' },
    { path: '/crawler', icon: Search, label: 'Crawler' },
    { path: '/threats', icon: AlertTriangle, label: 'Threat List' },
    { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  ];

  return (
    <div className="layout">
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="logo">
            <Shield size={32} className="logo-icon" />
            {sidebarOpen && (
              <div className="logo-text">
                <h1>TNI AU</h1>
                <p>Threat Intel</p>
              </div>
            )}
          </div>
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => 
                `nav-item ${isActive ? 'active' : ''}`
              }
            >
              <item.icon size={20} />
              {sidebarOpen && <span>{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="status-indicator">
            <Globe size={16} />
            {sidebarOpen && (
              <div>
                <div className="status-label">System Status</div>
                <div className="status-value online">Online</div>
              </div>
            )}
          </div>
        </div>
      </aside>

      <main className="main-content">
        <div className="content-wrapper">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;
