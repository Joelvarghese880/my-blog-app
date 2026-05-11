import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../api';
import { useAuth } from '../context/AuthContext';
import { Trash2, Edit } from 'lucide-react';

interface Post {
  id: number;
  title: string;
  content: string;
  author: {
    id: number;
    username: string;
  };
}

const Home = () => {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, isAuthenticated } = useAuth();

  const fetchPosts = async () => {
    try {
      const res = await api.get('/api/posts');
      setPosts(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this post?')) return;
    try {
      await api.delete(`/api/posts/${id}`);
      setPosts(posts.filter(p => p.id !== id));
    } catch (err) {
      console.error(err);
      alert('Failed to delete post');
    }
  };

  if (loading) return <div style={{ textAlign: 'center', marginTop: '4rem' }}>Loading posts...</div>;

  return (
    <div className="animate-fade-in">
      <h1 style={{ marginBottom: '2rem' }}>Latest Posts</h1>
      {posts.length === 0 ? (
        <div className="glass" style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          No posts found. Be the first to write one!
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '1.5rem' }}>
          {posts.map(post => (
            <div key={post.id} className="glass card" style={{ position: 'relative' }}>
              {isAuthenticated && user?.id === post.author.id && (
                <div style={{ position: 'absolute', top: '1.5rem', right: '1.5rem', display: 'flex', gap: '0.5rem' }}>
                  <Link to={`/edit/${post.id}`} className="btn btn-outline" style={{ padding: '0.5rem', color: 'var(--accent-color)' }}>
                    <Edit size={16} />
                  </Link>
                  <button onClick={() => handleDelete(post.id)} className="btn btn-outline" style={{ padding: '0.5rem', color: 'var(--danger-color)' }}>
                    <Trash2 size={16} />
                  </button>
                </div>
              )}
              <h2 style={{ color: 'var(--accent-color)', marginBottom: '0.5rem', paddingRight: '4rem' }}>{post.title}</h2>
              <p style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', marginBottom: '1rem' }}>
                By @{post.author.username}
              </p>
              <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>{post.content}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Home;
