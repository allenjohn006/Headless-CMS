import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Database, FileText, Settings, Image as ImageIcon } from 'lucide-react';
import './index.css';

// Simple API mock for preview purposes
const api = {
  getCollections: () => Promise.resolve([
    { id: '1', name: 'Blog Posts', slug: 'posts', fields: [] },
    { id: '2', name: 'Products', slug: 'products', fields: [] }
  ]),
};

function Sidebar() {
  const location = useLocation();
  const isActive = (path: str) => location.pathname === path ? 'active' : '';

  return (
    <div className="sidebar">
      <div className="flex items-center gap-2" style={{ marginBottom: '2rem', padding: '0 1rem' }}>
        <div style={{ width: '32px', height: '32px', background: 'var(--accent-primary)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: 'white' }}>
          AE
        </div>
        <h2 style={{ fontSize: '1.2rem', margin: 0 }}>Antigravity Engine</h2>
      </div>
      
      <nav>
        <Link to="/" className={`nav-item ${isActive('/')}`}>
          <LayoutDashboard size={20} /> Dashboard
        </Link>
        <Link to="/schema" className={`nav-item ${isActive('/schema')}`}>
          <Database size={20} /> Schema Builder
        </Link>
        <Link to="/content" className={`nav-item ${isActive('/content')}`}>
          <FileText size={20} /> Content Editor
        </Link>
        <Link to="/media" className={`nav-item ${isActive('/media')}`}>
          <ImageIcon size={20} /> Media Library
        </Link>
      </nav>

      <div style={{ marginTop: 'auto' }}>
        <Link to="/settings" className={`nav-item ${isActive('/settings')}`}>
          <Settings size={20} /> Settings
        </Link>
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <div>
      <h1 style={{ marginBottom: '2rem' }}>Dashboard</h1>
      <div className="grid grid-cols-3">
        <div className="card glass-panel flex flex-col gap-2">
          <Database size={32} color="var(--accent-primary)" />
          <h3>Total Collections</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>12</p>
        </div>
        <div className="card glass-panel flex flex-col gap-2">
          <FileText size={32} color="var(--success)" />
          <h3>Published Content</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>348</p>
        </div>
        <div className="card glass-panel flex flex-col gap-2">
          <ImageIcon size={32} color="#f59e0b" />
          <h3>Media Assets</h3>
          <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>1,024</p>
        </div>
      </div>
    </div>
  );
}

function SchemaBuilder() {
  const [collections, setCollections] = useState<any[]>([]);

  useEffect(() => {
    api.getCollections().then(setCollections);
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <h1>Schema Builder</h1>
        <button className="btn btn-primary">+ New Collection</button>
      </div>
      
      <div className="card glass-panel">
        <h3 style={{ marginBottom: '1rem' }}>Collections</h3>
        <div className="flex flex-col gap-2">
          {collections.map(c => (
            <div key={c.id} className="flex justify-between items-center" style={{ padding: '1rem', border: '1px solid var(--border)', borderRadius: '8px', background: 'rgba(255,255,255,0.02)' }}>
              <div>
                <strong style={{ display: 'block', fontSize: '1.1rem' }}>{c.name}</strong>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>/{c.slug}</span>
              </div>
              <button className="btn btn-secondary">Edit Fields</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function ContentEditor() {
  return (
    <div>
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <h1>Content Editor</h1>
        <button className="btn btn-primary">Create Entry</button>
      </div>
      
      <div className="card glass-panel">
        <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '3rem 0' }}>
          Select a collection from the sidebar to manage its content.
        </p>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="dashboard-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/schema" element={<SchemaBuilder />} />
            <Route path="/content" element={<ContentEditor />} />
            <Route path="*" element={<h1 style={{color: 'var(--text-secondary)'}}>404 / Under Construction</h1>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
