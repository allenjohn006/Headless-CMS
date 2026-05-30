import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom';
import { LayoutDashboard, Database, FileText, Settings as SettingsIcon, Image as ImageIcon, LogOut, AlertCircle, Loader } from 'lucide-react';
import './index.css';
import { useAuth } from './contexts/AuthContext';
import { LoginPage } from './pages/LoginPage';
import { collectionsAPI, contentAPI, mediaAPI } from './api/client';

// Protected route wrapper
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();
  return token ? <>{children}</> : <Navigate to="/login" />;
}

function Sidebar() {
  const location = useLocation();
  const { user, logout } = useAuth();
  const isActive = (path: string) => location.pathname === path ? 'active' : '';

  return (
    <div className="sidebar">
      <div className="flex items-center gap-2" style={{ marginBottom: '2rem', padding: '0 1rem' }}>
        <div style={{ width: '32px', height: '32px', background: 'var(--accent-primary)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', color: 'white' }}>
          AE
        </div>
        <h2 style={{ fontSize: '1.2rem', margin: 0 }}>Antigravity Engine</h2>
      </div>
      
      {user && (
        <div style={{ padding: '0.5rem 1rem', marginBottom: '1rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          <strong>{user.email}</strong> ({user.role})
        </div>
      )}
      
      <nav>
        <Link to="/dashboard" className={`nav-item ${isActive('/dashboard')}`}>
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
          <SettingsIcon size={20} /> Settings
        </Link>
        <button 
          onClick={logout}
          className="nav-item"
          style={{ border: 'none', background: 'none', cursor: 'pointer', width: '100%', textAlign: 'left', color: 'inherit' }}
        >
          <LogOut size={20} /> Logout
        </button>
      </div>
    </div>
  );
}

function Dashboard() {
  const [stats, setStats] = useState({ collections: 0, content: 0, media: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const collectionsRes = await collectionsAPI.getAll();
        setStats({
          collections: collectionsRes.data.length || 0,
          content: Math.floor(Math.random() * 100),
          media: Math.floor(Math.random() * 50),
        });
      } catch (err) {
        console.error('Failed to load dashboard stats', err);
      } finally {
        setLoading(false);
      }
    };
    loadStats();
  }, []);

  return (
    <div>
      <h1 style={{ marginBottom: '2rem' }}>Dashboard</h1>
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <Loader size={32} style={{ animation: 'spin 1s linear infinite' }} />
        </div>
      ) : (
        <div className="grid grid-cols-3">
          <div className="card glass-panel flex flex-col gap-2">
            <Database size={32} color="var(--accent-primary)" />
            <h3>Total Collections</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.collections}</p>
          </div>
          <div className="card glass-panel flex flex-col gap-2">
            <FileText size={32} color="var(--success)" />
            <h3>Published Content</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.content}</p>
          </div>
          <div className="card glass-panel flex flex-col gap-2">
            <ImageIcon size={32} color="#f59e0b" />
            <h3>Media Assets</h3>
            <p style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.media}</p>
          </div>
        </div>
      )}
    </div>
  );
}

function SchemaBuilder() {
  const [collections, setCollections] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newCollection, setNewCollection] = useState({ name: '', slug: '', description: '' });
  const [showForm, setShowForm] = useState(false);

  const loadCollections = async () => {
    setLoading(true);
    try {
      const res = await collectionsAPI.getAll();
      setCollections(res.data);
      setError(null);
    } catch (err: any) {
      setError('Failed to load collections');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCollections();
  }, []);

  const handleCreateCollection = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await collectionsAPI.create(newCollection);
      setNewCollection({ name: '', slug: '', description: '' });
      setShowForm(false);
      loadCollections();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create collection');
    }
  };

  const handleDeleteCollection = async (id: string) => {
    if (confirm('Are you sure? This will delete the collection and all its content.')) {
      try {
        await collectionsAPI.delete(id);
        loadCollections();
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to delete collection');
      }
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <h1>Schema Builder</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ New Collection'}
        </button>
      </div>

      {error && (
        <div className="card glass-panel" style={{ background: 'rgba(255, 0, 0, 0.1)', padding: '1rem', marginBottom: '1rem', border: '1px solid rgba(255, 0, 0, 0.3)', borderRadius: '8px', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <AlertCircle size={20} color="red" />
          <span>{error}</span>
        </div>
      )}

      {showForm && (
        <div className="card glass-panel" style={{ marginBottom: '2rem', padding: '1.5rem' }}>
          <h3 style={{ marginBottom: '1rem' }}>Create New Collection</h3>
          <form onSubmit={handleCreateCollection}>
            <div style={{ display: 'grid', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Name</label>
                <input
                  type="text"
                  value={newCollection.name}
                  onChange={(e) => setNewCollection({ ...newCollection, name: e.target.value })}
                  placeholder="e.g., Blog Posts"
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--bg-secondary)' }}
                  required
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Slug</label>
                <input
                  type="text"
                  value={newCollection.slug}
                  onChange={(e) => setNewCollection({ ...newCollection, slug: e.target.value })}
                  placeholder="e.g., blog-posts"
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--bg-secondary)' }}
                  required
                />
              </div>
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Description</label>
                <input
                  type="text"
                  value={newCollection.description}
                  onChange={(e) => setNewCollection({ ...newCollection, description: e.target.value })}
                  placeholder="Optional"
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--bg-secondary)' }}
                />
              </div>
            </div>
            <button type="submit" className="btn btn-primary">Create Collection</button>
          </form>
        </div>
      )}
      
      <div className="card glass-panel">
        <h3 style={{ marginBottom: '1rem' }}>Collections ({collections.length})</h3>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            <Loader size={24} style={{ animation: 'spin 1s linear infinite', margin: '0 auto' }} />
          </div>
        ) : collections.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '2rem' }}>No collections yet. Create one to get started!</p>
        ) : (
          <div className="flex flex-col gap-2">
            {collections.map(c => (
              <div key={c.id} className="flex justify-between items-center" style={{ padding: '1rem', border: '1px solid var(--border)', borderRadius: '8px', background: 'rgba(255,255,255,0.02)' }}>
                <div>
                  <strong style={{ display: 'block', fontSize: '1.1rem' }}>{c.name}</strong>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>/{c.slug}</span>
                  {c.description && <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', margin: '0.25rem 0 0 0' }}>{c.description}</p>}
                </div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button className="btn btn-secondary">Edit Fields</button>
                  <button 
                    className="btn"
                    style={{ background: 'rgba(255, 0, 0, 0.1)', color: 'red', border: '1px solid rgba(255, 0, 0, 0.3)' }}
                    onClick={() => handleDeleteCollection(c.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function ContentEditor() {
  const [collections, setCollections] = useState<any[]>([]);
  const [selectedCollection, setSelectedCollection] = useState<string | null>(null);
  const [content, setContent] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCollections = async () => {
      try {
        const res = await collectionsAPI.getAll();
        setCollections(res.data);
        if (res.data.length > 0) {
          setSelectedCollection(res.data[0].slug);
        }
      } catch (err) {
        setError('Failed to load collections');
      }
    };
    loadCollections();
  }, []);

  useEffect(() => {
    if (selectedCollection) {
      const loadContent = async () => {
        setLoading(true);
        try {
          const res = await contentAPI.getByCollection(selectedCollection);
          setContent(res.data);
          setError(null);
        } catch (err: any) {
          setError('Failed to load content');
        } finally {
          setLoading(false);
        }
      };
      loadContent();
    }
  }, [selectedCollection]);

  const handleDeleteContent = async (contentId: string) => {
    if (confirm('Are you sure you want to delete this content?')) {
      try {
        if (selectedCollection) {
          await contentAPI.delete(selectedCollection, contentId);
          setContent(content.filter(c => c.id !== contentId));
        }
      } catch (err: any) {
        setError('Failed to delete content');
      }
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <h1>Content Editor</h1>
        <button className="btn btn-primary">Create Entry</button>
      </div>

      {error && (
        <div className="card glass-panel" style={{ background: 'rgba(255, 0, 0, 0.1)', padding: '1rem', marginBottom: '1rem', border: '1px solid rgba(255, 0, 0, 0.3)', borderRadius: '8px', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <AlertCircle size={20} color="red" />
          <span>{error}</span>
        </div>
      )}

      <div className="card glass-panel" style={{ marginBottom: '2rem' }}>
        <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>Select Collection</label>
        <select 
          value={selectedCollection || ''} 
          onChange={(e) => setSelectedCollection(e.target.value)}
          style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--bg-secondary)' }}
        >
          <option value="">-- Choose a collection --</option>
          {collections.map(c => (
            <option key={c.id} value={c.slug}>{c.name}</option>
          ))}
        </select>
      </div>

      <div className="card glass-panel">
        {!selectedCollection ? (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '3rem 0' }}>
            Select a collection from the dropdown to manage its content.
          </p>
        ) : loading ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <Loader size={24} style={{ animation: 'spin 1s linear infinite', margin: '0 auto' }} />
          </div>
        ) : content.length === 0 ? (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '3rem 0' }}>
            No content yet. Create an entry to get started!
          </p>
        ) : (
          <div className="flex flex-col gap-2">
            {content.map(item => (
              <div key={item.id} style={{ padding: '1rem', border: '1px solid var(--border)', borderRadius: '8px', background: 'rgba(255,255,255,0.02)' }}>
                <div style={{ marginBottom: '0.5rem' }}>
                  <strong>{item.id.slice(0, 8)}</strong>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginLeft: '0.5rem' }}>Status: {item.status || 'Draft'}</span>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                  <button className="btn btn-secondary">Edit</button>
                  <button 
                    className="btn"
                    style={{ background: 'rgba(255, 0, 0, 0.1)', color: 'red', border: '1px solid rgba(255, 0, 0, 0.3)' }}
                    onClick={() => handleDeleteContent(item.id)}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function MediaLibrary() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    try {
      await mediaAPI.upload(file);
      setError(null);
    } catch (err: any) {
      setError('Failed to upload media');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center" style={{ marginBottom: '2rem' }}>
        <h1>Media Library</h1>
        <label className="btn btn-primary">
          Upload Media
          <input type="file" onChange={handleUpload} style={{ display: 'none' }} accept="image/*" />
        </label>
      </div>

      {error && (
        <div className="card glass-panel" style={{ background: 'rgba(255, 0, 0, 0.1)', padding: '1rem', marginBottom: '1rem', border: '1px solid rgba(255, 0, 0, 0.3)', borderRadius: '8px', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <AlertCircle size={20} color="red" />
          <span>{error}</span>
        </div>
      )}

      <div className="card glass-panel">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem' }}>
            <Loader size={24} style={{ animation: 'spin 1s linear infinite', margin: '0 auto' }} />
          </div>
        ) : (
          <p style={{ color: 'var(--text-secondary)', textAlign: 'center', padding: '3rem 0' }}>
            No media yet. Upload images to get started!
          </p>
        )}
      </div>
    </div>
  );
}

function Settings() {
  const { user } = useAuth();

  return (
    <div>
      <h1 style={{ marginBottom: '2rem' }}>Settings</h1>
      
      <div className="card glass-panel">
        <h3 style={{ marginBottom: '1rem' }}>Account Information</h3>
        <div style={{ display: 'grid', gap: '1rem' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Email</label>
            <input type="text" value={user?.email || ''} disabled style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--bg-secondary)' }} />
          </div>
          <div>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>Role</label>
            <input type="text" value={user?.role || ''} disabled style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--bg-secondary)' }} />
          </div>
        </div>
      </div>
    </div>
  );
}

function AppLayout() {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/schema" element={<SchemaBuilder />} />
          <Route path="/content" element={<ContentEditor />} />
          <Route path="/media" element={<MediaLibrary />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/dashboard" />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route 
          path="/*" 
          element={
            <ProtectedRoute>
              <AppLayout />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;
