import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { Layout, History, LogOut, Plus, Sparkles, ShoppingBag, MapPin, Calendar, ArrowRight } from "lucide-react";
import bg from "../assets/bg.jpg";
import "./design.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function Dashboard() {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    const userName = localStorage.getItem("user_name") || "User";

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (!token) {
            navigate("/auth");
            return;
        }
        fetchHistory(token);
    }, []);

    const fetchHistory = async (token) => {
        try {
            const res = await axios.get(`${API_BASE_URL}/user/history`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setHistory(res.data);
        } catch (err) {
            console.error("Failed to fetch history", err);
            if (err.response?.status === 401) navigate("/auth");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate("/auth");
    };

    return (
        <div className="design-container" style={{ backgroundImage: `url(${bg})`, backgroundAttachment: 'fixed', minHeight: '100vh' }}>
            <div className="overlay"></div>

            <div className="content-wrapper" style={{ maxWidth: '1600px', width: '95%' }}>
                <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px', paddingTop: '20px', width: '100%' }}>
                    <div>
                        <h1 className="design-title" style={{ textAlign: 'left', marginBottom: '5px' }}>Namaste, {userName}!</h1>
                        <p style={{ color: '#aaa' }}>Your Personal Interior Design Dashboard</p>
                    </div>
                    <div style={{ display: 'flex', gap: '15px' }}>
                        <Link to="/design" className="generate-btn" style={{ padding: '10px 25px', borderRadius: '30px', textDecoration: 'none', fontSize: '0.9rem', width: 'auto' }}>
                            <Plus size={18} /> New Design
                        </Link>
                        <button onClick={handleLogout} className="back-btn" style={{ padding: '10px 20px', borderRadius: '30px', background: 'rgba(255,0,0,0.1)', color: '#ff4d4d' }}>
                            <LogOut size={18} /> Logout
                        </button>
                    </div>
                </header>

                <div className="dashboard-grid" style={{ width: '100%' }}>
                    <div className="glass-card full-width" style={{ padding: '40px' }}>
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'gold', marginBottom: '30px' }}>
                            <History size={24} /> Design History
                        </h3>

                        {loading ? (
                            <div style={{ textAlign: 'center', padding: '50px' }}>
                                <div className="animate-spin" style={{ display: 'inline-block' }}><History /></div>
                                <p>Loading your past creations...</p>
                            </div>
                        ) : history.length === 0 ? (
                            <div style={{ textAlign: 'center', padding: '50px', border: '1px dashed #444', borderRadius: '20px' }}>
                                <Sparkles size={40} color="#444" style={{ marginBottom: '15px' }} />
                                <p style={{ color: '#888' }}>You haven't generated any designs yet.</p>
                                <Link to="/design" className="shop-link" style={{ marginTop: '10px', display: 'inline-flex' }}>Start Designing Now</Link>
                            </div>
                        ) : (
                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(400px, 1fr))', gap: '30px' }}>
                                {history.map((item) => (
                                    <div key={item.id} className="plan-card-result history-card" style={{ padding: '0', overflow: 'hidden', display: 'flex', flexDirection: 'column', border: '1px solid #333', background: 'rgba(0,0,0,0.5)' }}>
                                        <div style={{ height: '220px', position: 'relative' }}>
                                            <img
                                                src={item.image_url || "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?w=800"}
                                                alt="Design"
                                                style={{ width: '100%', height: '100%', objectFit: 'cover', transition: '0.5s' }}
                                                className="history-img"
                                            />
                                            <div style={{ position: 'absolute', bottom: '0', left: '0', right: '0', height: '50%', background: 'linear-gradient(transparent, rgba(0,0,0,0.9))' }}></div>
                                            <div style={{ position: 'absolute', top: '15px', right: '15px', background: 'rgba(212, 175, 55, 0.9)', padding: '6px 12px', borderRadius: '20px', fontSize: '0.7rem', color: 'black', fontWeight: 'bold', textTransform: 'capitalize' }}>
                                                {item.theme.replace(/_/g, ' ')}
                                            </div>
                                        </div>
                                        <div style={{ padding: '25px' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
                                                <div>
                                                    <h4 style={{ margin: '0 0 5px 0', fontSize: '1.25rem', color: 'white', textTransform: 'capitalize' }}>
                                                        {item.space_type.replace(/_/g, ' ')}
                                                    </h4>
                                                    <span style={{ fontSize: '0.8rem', color: '#888', display: 'flex', alignItems: 'center', gap: '6px' }}>
                                                        <Calendar size={14} /> {item.created_at}
                                                    </span>
                                                </div>
                                                <div style={{ textAlign: 'right' }}>
                                                    <div style={{ fontWeight: '800', color: '#d4af37', fontSize: '1.1rem' }}>₹{item.total_cost.toLocaleString()}</div>
                                                    <div style={{ fontSize: '0.75rem', color: '#666' }}>{item.selected_plan} Plan</div>
                                                </div>
                                            </div>

                                            <button
                                                className="shop-link"
                                                style={{ width: '100%', justifyContent: 'center', padding: '12px', fontSize: '0.9rem', fontWeight: 'bold' }}
                                                onClick={() => navigate('/design', { state: { previousResult: item } })}
                                            >
                                                View Transformation <ArrowRight size={16} />
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;
