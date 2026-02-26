import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { User, Lock, Mail, MapPin, Loader2, Sparkles, ArrowRight } from "lucide-react";
import bg from "../assets/bg.jpg";
import "./design.css"; // Reuse styling for consistency

const API_BASE_URL = "http://127.0.0.1:8000";

function Auth() {
    const [isLogin, setIsLogin] = useState(true);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Form states
    const [formData, setFormData] = useState({
        name: "",
        username: "",
        email: "",
        password: "",
        location: ""
    });

    const [locations, setLocations] = useState([]);

    useEffect(() => {
        const fetchLocations = async () => {
            try {
                const res = await axios.get(`${API_BASE_URL}/api/locations`);
                setLocations(res.data);
                if (res.data.length > 0) {
                    setFormData(prev => ({ ...prev, location: res.data[0] }));
                }
            } catch (err) {
                console.error("Failed to fetch locations");
            }
        };
        fetchLocations();
    }, []);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            if (isLogin) {
                const res = await axios.post(`${API_BASE_URL}/login`, {
                    username: formData.username,
                    password: formData.password
                });
                localStorage.setItem("token", res.data.token);
                localStorage.setItem("user_name", res.data.name);
                localStorage.setItem("is_admin", res.data.is_admin);

                if (res.data.is_admin) navigate("/admin");
                else navigate("/dashboard");
            } else {
                await axios.post(`${API_BASE_URL}/register`, formData);
                setIsLogin(true);
                alert("Registration successful! Please login.");
            }
        } catch (err) {
            setError(err.response?.data?.message || "Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="design-container" style={{ backgroundImage: `url(${bg})`, backgroundAttachment: 'fixed' }}>
            <div className="overlay"></div>
            <div className="content-wrapper" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
                <div className="design-card auth-card" style={{ maxWidth: '480px', width: '95%', margin: '40px auto', padding: '60px 40px' }}>
                    <div style={{ textAlign: 'center', marginBottom: '40px' }}>
                        <div style={{ display: 'inline-flex', padding: '20px', borderRadius: '50%', background: 'rgba(212, 175, 55, 0.1)', marginBottom: '20px' }}>
                            <Sparkles size={40} color="#d4af37" />
                        </div>
                        <h2 className="design-title" style={{ fontSize: '2.5rem', marginBottom: '10px' }}>
                            {isLogin ? "Welcome Back" : "Create Account"}
                        </h2>
                        <p style={{ color: '#888', fontSize: '1rem', fontWeight: '500' }}>
                            {isLogin ? "Your AI-powered interior awaits." : "Join the revolution of agentic design."}
                        </p>
                    </div>

                    <form onSubmit={handleSubmit}>
                        {!isLogin && (
                            <>
                                <div className="form-group">
                                    <label><User size={16} className="inline-icon" /> Full Name</label>
                                    <input name="name" type="text" placeholder="John Doe" required onChange={handleChange} />
                                </div>
                                <div className="form-group">
                                    <label><Mail size={16} className="inline-icon" /> Email Address</label>
                                    <input name="email" type="email" placeholder="john@example.com" required onChange={handleChange} />
                                </div>
                            </>
                        )}
                        <div className="form-group">
                            <label><User size={16} className="inline-icon" /> Username</label>
                            <input name="username" type="text" placeholder="johndoe123" required onChange={handleChange} />
                        </div>
                        <div className="form-group">
                            <label><Lock size={16} className="inline-icon" /> Password</label>
                            <input name="password" type="password" placeholder="••••••••" required onChange={handleChange} />
                        </div>
                        {!isLogin && (
                            <div className="form-group">
                                <label><MapPin size={16} className="inline-icon" /> Catchment Location</label>
                                <select
                                    name="location"
                                    className="design-input"
                                    style={{ background: 'rgba(255,255,255,0.05)', color: '#fff', border: '1px solid #444', height: '50px', borderRadius: '10px', padding: '0 15px', width: '100%' }}
                                    onChange={handleChange}
                                    value={formData.location}
                                >
                                    {locations.map(loc => (
                                        <option key={loc} value={loc} style={{ background: '#111', color: '#fff' }}>{loc}</option>
                                    ))}
                                </select>
                            </div>
                        )}

                        {error && <p className="error-message" style={{ textAlign: 'center' }}>{error}</p>}

                        <button className="generate-btn" type="submit" disabled={loading} style={{ marginTop: '20px' }}>
                            {loading ? <Loader2 className="animate-spin" /> : (
                                <span style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                                    {isLogin ? "Login Now" : "Register"} <ArrowRight size={18} />
                                </span>
                            )}
                        </button>
                    </form>

                    <div style={{ textAlign: 'center', marginTop: '20px', color: '#888', fontSize: '0.9rem' }}>
                        {isLogin ? "Don't have an account?" : "Already have an account?"}
                        <button
                            className="shop-link"
                            style={{ background: 'none', border: 'none', padding: '0 5px', cursor: 'pointer', display: 'inline' }}
                            onClick={() => setIsLogin(!isLogin)}
                        >
                            {isLogin ? "Register here" : "Login here"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Auth;
