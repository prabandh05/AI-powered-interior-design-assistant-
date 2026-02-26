import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import {
    Users, BarChart3, TrendingUp, IndianRupee, PieChart,
    ShieldCheck, LogOut, ArrowLeft, MapPin, Layers
} from "lucide-react";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    AreaChart, Area, PieChart as RePieChart, Pie, Cell, Legend
} from 'recharts';
import bg from "../assets/bg.jpg";
import "./design.css";

const API_BASE_URL = "http://127.0.0.1:8000";
const COLORS = ['#d4af37', '#e5c568', '#f1d994', '#c09d2e', '#9b7e23'];
const SPACE_COLORS = {
    "Living Room": "#d4af37",
    "Bedroom": "#c0a0c0",
    "Kitchen": "#4cd137",
    "Study Room": "#00a8ff",
    "Dining Room": "#e84118"
};

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

    if (loading || !stats) return (
        <div className="design-container" style={{ backgroundImage: `url(${bg})` }}>
            <div className="overlay"></div>
            <div className="content-wrapper">
                <div style={{ color: 'gold', fontSize: '1.5rem', fontWeight: 'bold' }}>Synchronizing Intelligence Matrix...</div>
            </div>
        </div>
    );

    return (
        <div className="design-container" style={{ backgroundImage: `url(${bg})`, backgroundAttachment: 'fixed', minHeight: '100vh', color: '#eee' }}>
            <div className="overlay"></div>

            <div className="content-wrapper" style={{ maxWidth: '1400px', width: '95%' }}>
                <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '40px', paddingTop: '20px', width: '100%' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                        <div style={{ padding: '15px', borderRadius: '15px', background: 'rgba(212, 175, 55, 0.1)', border: '1px solid rgba(212, 175, 55, 0.2)' }}>
                            <ShieldCheck size={32} color="#d4af37" />
                        </div>
                        <div>
                            <h1 className="design-title" style={{ textAlign: 'left', marginBottom: '5px', fontSize: '2.5rem', textShadow: '0 4px 10px rgba(0,0,0,0.5)' }}>Strategy Intelligence</h1>
                            <p style={{ color: '#aaa', fontSize: '1.1rem' }}>Enterprise Analytics & Behavioral Patterns</p>
                        </div>
                    </div>
                    <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                        <button onClick={() => navigate("/dashboard")} className="back-btn" style={{ borderRadius: '12px', background: 'rgba(255,255,255,0.05)', color: '#fff', border: '1px solid #444' }}>
                            <ArrowLeft size={18} /> Exit to Dashboard
                        </button>
                        <button onClick={handleLogout} className="back-btn" style={{ borderRadius: '12px', background: 'rgba(255,50,50,0.15)', color: '#ff6b6b', border: '1px solid rgba(255,50,50,0.3)' }}>
                            <LogOut size={18} /> Terminate Session
                        </button>
                    </div>
                </header>

                {/* Key Metrics Row */}
                <div className="plans-grid" style={{ marginBottom: '40px', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', width: '100%', gap: '20px' }}>
                    <div className="plan-card-result featured-plan" style={{ background: 'linear-gradient(135deg, rgba(212, 175, 55, 0.2), rgba(0,0,0,0.6))', height: '180px' }}>
                        <Users size={24} color="gold" />
                        <div style={{ fontSize: '2.8rem', fontWeight: '900', margin: '10px 0', color: '#fff' }}>{stats.total_users}</div>
                        <p style={{ color: 'gold', textTransform: 'uppercase', fontSize: '0.8rem', fontWeight: 'bold' }}>Active Ecosystem Users</p>
                    </div>
                    <div className="plan-card-result" style={{ background: 'rgba(20,20,20,0.7)', height: '180px', border: '1px solid #333' }}>
                        <BarChart3 size={24} color="gold" />
                        <div style={{ fontSize: '2.8rem', fontWeight: '900', margin: '10px 0', color: '#fff' }}>{stats.total_designs}</div>
                        <p style={{ color: '#aaa', textTransform: 'uppercase', fontSize: '0.8rem' }}>Intelligence Cycles</p>
                    </div>
                    <div className="plan-card-result" style={{ background: 'rgba(20,20,20,0.7)', height: '180px', border: '1px solid #333' }}>
                        <IndianRupee size={24} color="gold" />
                        <div style={{ fontSize: '2.8rem', fontWeight: '900', margin: '10px 0', color: '#fff' }}>₹{Math.round(stats.avg_budget)?.toLocaleString()}</div>
                        <p style={{ color: '#aaa', textTransform: 'uppercase', fontSize: '0.8rem' }}>Mean Captive Budget</p>
                    </div>
                    <div className="plan-card-result" style={{ background: 'rgba(20,20,20,0.7)', height: '180px', border: '1px solid #333' }}>
                        <TrendingUp size={24} color="gold" />
                        <div style={{ fontSize: '1.4rem', fontWeight: '900', margin: '20px 0', color: 'gold', textTransform: 'uppercase' }}>
                            {stats.theme_distribution?.[0]?.name || "N/A"}
                        </div>
                        <p style={{ color: '#aaa', textTransform: 'uppercase', fontSize: '0.8rem' }}>Dominant Aesthetic Market</p>
                    </div>
                </div>

                {/* Main Analytics Matrix */}
                <div className="results-grid-layout" style={{ width: '100%', gap: '30px' }}>

                    {/* Theme vs Space Matrix (HEATMAP SUBSTITUTE) */}
                    <div className="glass-card full-width" style={{ height: '450px', display: 'flex', flexDirection: 'column', background: 'rgba(15,15,15,0.8)', border: '1px solid #222' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', padding: '0 10px' }}>
                            <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'gold' }}>
                                <Layers size={22} /> Thematic Space Utilization Matrix
                            </h3>
                            <div style={{ display: 'flex', gap: '15px', fontSize: '0.7rem' }}>
                                {Object.entries(SPACE_COLORS).map(([name, color]) => (
                                    <div key={name} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                                        <div style={{ width: 10, height: 10, background: color, borderRadius: '2px' }}></div>
                                        <span style={{ color: '#aaa' }}>{name}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div style={{ flex: 1, width: '100%' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={stats.heatmap_data} margin={{ top: 20, right: 30, left: 20, bottom: 40 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={false} />
                                    <XAxis dataKey="name" stroke="#fff" interval={0} angle={0} textAnchor="middle" height={50} fontSize={10} fontWeight="bold" />
                                    <YAxis stroke="#aaa" label={{ value: 'Frequency', angle: -90, position: 'insideLeft', fill: 'gold' }} fontSize={11} />
                                    <Tooltip
                                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                        contentStyle={{ backgroundColor: '#000', border: '1px solid gold', borderRadius: '8px' }}
                                        itemStyle={{ color: '#fff' }}
                                        labelStyle={{ color: '#fff' }}
                                    />
                                    <Bar dataKey="Living Room" stackId="a" fill={SPACE_COLORS["Living Room"]} />
                                    <Bar dataKey="Bedroom" stackId="a" fill={SPACE_COLORS["Bedroom"]} />
                                    <Bar dataKey="Kitchen" stackId="a" fill={SPACE_COLORS["Kitchen"]} />
                                    <Bar dataKey="Study Room" stackId="a" fill={SPACE_COLORS["Study Room"]} />
                                    <Bar dataKey="Dining Room" stackId="a" fill={SPACE_COLORS["Dining Room"]} radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Regional Engagement */}
                    <div className="glass-card" style={{ height: '400px', display: 'flex', flexDirection: 'column', background: 'rgba(15,15,15,0.8)', border: '1px solid #222' }}>
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'gold' }}><MapPin size={20} /> Geographic Market Penetration</h3>
                        <div style={{ flex: 1, width: '100%', marginTop: '20px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={stats.location_distribution} margin={{ top: 20, right: 30, left: 10, bottom: 20 }}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#222" vertical={false} />
                                    <XAxis dataKey="name" stroke="#fff" fontSize={10} fontWeight="bold" />
                                    <YAxis stroke="#666" label={{ value: 'User Count', angle: -90, position: 'insideLeft', fill: '#666' }} fontSize={11} />
                                    <Tooltip
                                        cursor={{ fill: 'rgba(212, 175, 55, 0.1)' }}
                                        contentStyle={{ backgroundColor: '#111', border: '1px solid gold', borderRadius: '8px' }}
                                        itemStyle={{ color: '#fff' }}
                                        labelStyle={{ color: 'gold' }}
                                    />
                                    <Bar dataKey="value" fill="gold" radius={[5, 5, 0, 0]} barSize={40} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Budget Stratification */}
                    <div className="glass-card" style={{ height: '400px', display: 'flex', flexDirection: 'column', background: 'rgba(15,15,15,0.8)', border: '1px solid #222' }}>
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'gold' }}><IndianRupee size={20} /> Budget Stratification</h3>
                        <div style={{ flex: 1, width: '100%', marginTop: '20px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <RePieChart>
                                    <Pie
                                        data={stats.budget_distribution}
                                        innerRadius={70}
                                        outerRadius={110}
                                        paddingAngle={8}
                                        dataKey="value"
                                        stroke="none"
                                    >
                                        {stats.budget_distribution?.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#000', border: '1px solid gold', borderRadius: '10px' }}
                                        itemStyle={{ color: '#fff' }}
                                        labelStyle={{ color: '#fff' }}
                                    />
                                    <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ paddingTop: '20px', color: '#aaa' }} />
                                </RePieChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* Adoption Curve */}
                    <div className="glass-card full-width" style={{ height: '350px', display: 'flex', flexDirection: 'column', background: 'rgba(15,15,15,0.8)', border: '1px solid #222' }}>
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'gold' }}><TrendingUp size={22} /> Adoption Velocity (Last 30 Days)</h3>
                        <div style={{ flex: 1, width: '100%', marginTop: '20px' }}>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={stats.trend} margin={{ right: 30, left: 10 }}>
                                    <defs>
                                        <linearGradient id="colorTrend" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="gold" stopOpacity={0.4} />
                                            <stop offset="95%" stopColor="gold" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <XAxis dataKey="date" stroke="#666" fontSize={10} axisLine={false} tickLine={false} />
                                    <YAxis stroke="#666" fontSize={10} axisLine={false} tickLine={false} />
                                    <Tooltip
                                        contentStyle={{ backgroundColor: '#111', border: '1px solid gold' }}
                                        itemStyle={{ color: '#fff' }}
                                        labelStyle={{ color: 'gold' }}
                                    />
                                    <Area type="stepAfter" dataKey="count" stroke="gold" strokeWidth={3} fillOpacity={1} fill="url(#colorTrend)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                <div className="glass-card full-width mt-4" style={{ padding: '25px', textAlign: 'center', background: 'rgba(0,0,0,0.5)', marginTop: '50px', border: '1px solid #222' }}>
                    <p style={{ color: '#666', fontStyle: 'italic', fontSize: '0.9rem', letterSpacing: '0.5px' }}>
                        Proprietary Analytics Core V2.0 • Real-time Data Stream from SQLite Instance • System Status: <span style={{ color: '#4cd137' }}>Optimal</span>
                    </p>
                </div>
            </div>
        </div>
    );
}

// Minimal placeholder icons to avoid import errors if some icons are different
const Palette = ({ size, color }) => <PieChart size={size} color={color} />;

export default AdminDashboard;
