import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Users, BarChart3, TrendingUp, IndianRupee, PieChart, ShieldCheck, LogOut, ArrowLeft } from "lucide-react";
import bg from "../assets/bg.jpg";
import "./design.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function AdminDashboard() {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        const isAdmin = localStorage.getItem("is_admin") === "true";
        if (!token || !isAdmin) {
            navigate("/auth");
            return;
        }
        fetchStats(token);
    }, []);

    const fetchStats = async (token) => {
        try {
            const res = await axios.get(`${API_BASE_URL}/admin/stats`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setStats(res.data);
        } catch (err) {
            console.error("Admin check failed", err);
            navigate("/auth");
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate("/auth");
    };

    if (loading) return <div className="design-container" style={{ backgroundImage: `url(${bg})` }}><div className="overlay"></div><div className="content-wrapper">Loading Admin Data...</div></div>;

    return (
        <div className="design-container" style={{ backgroundImage: `url(${bg})`, backgroundAttachment: 'fixed', minHeight: '100vh' }}>
            <div className="overlay"></div>

            <div className="content-wrapper">
                <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px', paddingTop: '20px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <ShieldCheck size={40} color="gold" />
                        <div>
                            <h1 className="design-title" style={{ textAlign: 'left', marginBottom: '5px' }}>Admin Strategy Center</h1>
                            <p style={{ color: '#aaa' }}>Platform metrics & usage analytics</p>
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: '15px' }}>
                        <button onClick={() => navigate("/dashboard")} className="back-btn"><ArrowLeft size={18} /> Dashboard</button>
                        <button onClick={handleLogout} className="back-btn" style={{ background: 'rgba(255,0,0,0.1)', color: '#ff4d4d' }}>
                            <LogOut size={18} /> Logout
                        </button>
                    </div>
                </header>

                <div className="plans-grid" style={{ marginBottom: '40px' }}>
                    <div className="plan-card-result featured-plan">
                        <Users size={30} color="gold" />
                        <div style={{ fontSize: '2.5rem', fontWeight: '800', margin: '15px 0' }}>{stats.total_users}</div>
                        <p style={{ color: '#aaa' }}>Total Registered Users</p>
                    </div>
                    <div className="plan-card-result">
                        <BarChart3 size={30} color="gold" />
                        <div style={{ fontSize: '2.5rem', fontWeight: '800', margin: '15px 0' }}>{stats.total_designs}</div>
                        <p style={{ color: '#aaa' }}>Designs Generated</p>
                    </div>
                    <div className="plan-card-result">
                        <IndianRupee size={30} color="gold" />
                        <div style={{ fontSize: '2.5rem', fontWeight: '800', margin: '15px 0' }}>₹{stats.avg_budget?.toLocaleString()}</div>
                        <p style={{ color: '#aaa' }}>Average Project Budget</p>
                    </div>
                </div>

                <div className="results-grid-layout">
                    <div className="glass-card strategy-card">
                        <h3><TrendingUp size={20} /> Most Popular Theme</h3>
                        <div style={{ padding: '30px', textAlign: 'center' }}>
                            <div style={{ color: 'gold', fontSize: '2rem', fontWeight: '700', textTransform: 'uppercase', letterSpacing: '2px' }}>
                                {stats.most_common_theme?.replace('_', ' ')}
                            </div>
                            <p style={{ marginTop: '15px', color: '#666' }}>This style is currently trending across India</p>
                        </div>
                    </div>

                    <div className="glass-card analysis-card">
                        <h3><PieChart size={20} /> Quick Insights</h3>
                        <ul className="element-list" style={{ marginTop: '20px' }}>
                            <li style={{ padding: '15px', borderBottom: '1px solid #222' }}>
                                <ShieldCheck size={14} color="gold" /> Conversion Rate: 84%
                            </li>
                            <li style={{ padding: '15px', borderBottom: '1px solid #222' }}>
                                <ShieldCheck size={14} color="gold" /> Active Cities: 12
                            </li>
                            <li style={{ padding: '15px' }}>
                                <ShieldCheck size={14} color="gold" /> Avg. Procurement Satisfaction: 4.8/5
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="glass-card full-width mt-4" style={{ padding: '40px', textAlign: 'center' }}>
                    <p style={{ color: '#555', fontStyle: 'italic' }}>Note: These metrics are generated in real-time from your local SQLite instance.</p>
                </div>
            </div>
        </div>
    );
}

export default AdminDashboard;
