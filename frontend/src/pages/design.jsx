import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import { Loader2, Sparkles, ShoppingBag, Palette, Layout, ChevronRight, CheckCircle2, RefreshCw, ArrowLeft } from "lucide-react";
import bg from "../assets/bg.jpg";
import "./design.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function Design() {
    const [budgetLevel, setBudgetLevel] = useState("");
    const [theme, setTheme] = useState("");
    const [description, setDescription] = useState("");
    const [image, setImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [upPreview, setUpPreview] = useState(null);

    const location = useLocation();
    const navigate = useNavigate();

    // Iteration States
    const [tempTheme, setTempTheme] = useState("");
    const [tempBudget, setTempBudget] = useState("");

    // Load from history if coming from dashboard
    useEffect(() => {
        if (location.state?.previousResult) {
            const hist = location.state.previousResult;
            // Map history item back to result format
            setResult({
                status: "success",
                scene_analysis: {
                    theme: hist.theme,
                    space_type: hist.space_type,
                    budget: hist.budget,
                    detected_elements: [] // History only stores basics, but enough to show
                },
                design_strategy: {
                    summary: "Retrieved from your history",
                    space_type: hist.space_type,
                    theme: hist.theme
                },
                visuals: {
                    image_links: [hist.image_url],
                    transformation_guide: "History view: Please check your previous generation for full guide details."
                },
                procurement: {
                    comparison_plans: hist.procurement_plans || []
                }
            });
            // Sync temp states
            setTempTheme(hist.theme);
            const b = hist.budget;
            if (b <= 30000) setTempBudget("25000");
            else if (b <= 70000) setTempBudget("60000");
            else setTempBudget("100000");
        }
    }, [location.state]);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setUpPreview(URL.createObjectURL(file));
        }
    };

    const getBudgetLabel = (level) => {
        if (level === "1" || level === "25000") return 25000;
        if (level === "2" || level === "60000") return 60000;
        if (level === "3" || level === "100000") return 100000;
        return parseInt(level) || 30000;
    };

    const handleGenerate = async (isIteration = false) => {
        const currentTheme = isIteration ? tempTheme : theme;
        const currentBudget = isIteration ? getBudgetLabel(tempBudget) : getBudgetLabel(budgetLevel);
        const currentDesc = isIteration ? result.scene_analysis.description_text : description;

        if (!isIteration && (!description || !theme || !budgetLevel)) {
            alert("Please fill in the description, theme, and budget.");
            return;
        }

        setLoading(true);
        setError(null);

        try {
            let response;
            const token = localStorage.getItem("token");
            const headers = token ? { Authorization: `Bearer ${token}` } : {};

            if (!isIteration && image) {
                // Initial run with image: use FormData
                const formData = new FormData();
                formData.append("description_text", currentDesc);
                formData.append("theme", currentTheme);
                formData.append("budget", currentBudget);
                formData.append("image", image);

                response = await axios.post(`${API_BASE_URL}/generate-design`, formData, {
                    headers: { ...headers, 'Content-Type': 'multipart/form-data' }
                });
            } else {
                // Iteration or run without image: use JSON
                const payload = {
                    description_text: currentDesc,
                    theme: currentTheme,
                    budget: currentBudget,
                };
                if (isIteration && result) {
                    payload["previous_scene_data"] = result.scene_analysis;
                }
                response = await axios.post(`${API_BASE_URL}/generate-design`, payload, { headers });
            }
            console.log("Design Generation Result:", response.data);
            setResult(response.data);

            // Sync temp states
            if (response.data?.scene_analysis) {
                setTempTheme(response.data.scene_analysis.theme || "");
                const b = response.data.scene_analysis.budget;
                if (b <= 30000) setTempBudget("25000");
                else if (b <= 70000) setTempBudget("60000");
                else setTempBudget("100000");
            }

            // Scroll to results
            setTimeout(() => {
                document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);

        } catch (err) {
            console.error("Design Generation Error:", err);
            setError(err.response?.data?.message || "Failed to generate design. Our AI service might be busy. Please check your API keys.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            className="design-container"
            style={{
                backgroundImage: `url(${bg})`,
                backgroundAttachment: 'fixed'
            }}
        >
            <div className="overlay"></div>

            <div className="content-wrapper">
                {!result ? (
                    <div className="design-card">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                            <h1 className="design-title" style={{ margin: 0 }}>Design Your Space</h1>
                            <button onClick={() => navigate("/dashboard")} className="back-btn" style={{ background: 'rgba(255,255,255,0.1)', border: '1px solid #444' }}>
                                Dashboard
                            </button>
                        </div>

                        <div className="form-group">
                            <label><Layout className="inline-icon" size={18} /> 1. Describe Your Interior</label>
                            <textarea
                                placeholder="Describe your room layout, lighting, furniture, vibe..."
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                            />
                        </div>

                        <div className="form-group">
                            <label><Palette className="inline-icon" size={18} /> 2. Select Budget Level</label>
                            <div className="budget-grid">
                                <div
                                    className={`budget-box ${budgetLevel === "1" ? "active" : ""}`}
                                    onClick={() => setBudgetLevel("1")}
                                >
                                    Level 1 <br /> ~₹25,000
                                </div>
                                <div
                                    className={`budget-box ${budgetLevel === "2" ? "active" : ""}`}
                                    onClick={() => setBudgetLevel("2")}
                                >
                                    Level 2 <br /> ~₹60,000
                                </div>
                                <div
                                    className={`budget-box ${budgetLevel === "3" ? "active" : ""}`}
                                    onClick={() => setBudgetLevel("3")}
                                >
                                    Level 3 <br /> ₹1,00,000+
                                </div>
                            </div>
                        </div>

                        <div className="form-group">
                            <label><Palette className="inline-icon" size={18} /> 3. Preferred Theme</label>
                            <select
                                value={theme}
                                onChange={(e) => setTheme(e.target.value)}
                            >
                                <option value="">Select Theme</option>
                                <option value="traditional_indian">Traditional Indian</option>
                                <option value="contemporary_indian">Contemporary Indian</option>
                                <option value="rustic_indian">Rustic Indian</option>
                                <option value="rajasthani_mughal">Rajasthani Mughal</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label><Sparkles className="inline-icon" size={18} /> 4. Upload Current Room Image</label>
                            <div className="upload-container">
                                <input type="file" accept="image/*" onChange={handleImageUpload} id="file-upload" />
                                {upPreview && <img src={upPreview} alt="upload preview" className="mini-upload-preview" />}
                                {image && <p className="file-ready">Image selected: {image.name}</p>}
                            </div>
                        </div>

                        <button
                            className="generate-btn"
                            onClick={() => handleGenerate(false)}
                            disabled={loading}
                        >
                            {loading ? <><Loader2 className="animate-spin" /> Analyzing...</> : "Generate Design"}
                        </button>

                        {error && <p className="error-message">{error}</p>}
                    </div>
                ) : (
                    <div id="results-section" className="results-container">
                        <div className="result-header">
                            <button className="back-btn" onClick={() => {
                                navigate("/dashboard");
                            }}><ArrowLeft size={18} /> Back</button>
                            <h2><Sparkles className="gold-icon" /> Your AI Transformation</h2>
                        </div>

                        {/* Top: Visualization & Analysis Side-by-Side */}
                        <div className="results-grid-layout">

                            {/* Visual Preview (Most important part) */}
                            <div className="glass-card strategy-card hero-visual">
                                <h3><Sparkles size={20} /> Generated Design Preview</h3>
                                <div className="visual-preview">
                                    {result.visuals?.image_links?.length > 0 ? (
                                        result.visuals.image_links.map((link, i) => (
                                            <div key={i} className="visual-frame">
                                                <img src={link} alt="AI Visualization" />
                                                <div className="frame-overlay">Thematic Interior Concept</div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="visual-placeholder">
                                            <p>Rendering Visualization...</p>
                                        </div>
                                    )}
                                </div>
                                <div className="strategy-text">
                                    <p className="strategy-summary">"{result.design_strategy.summary}"</p>
                                </div>
                            </div>

                            {/* Refinement Panel (Change Theme/Budget) */}
                            <div className="glass-card analysis-card refinement-panel">
                                <h3><RefreshCw size={20} /> Refine Your Design</h3>
                                <div className="refinement-controls">
                                    <div className="control-group">
                                        <label>Modify Theme</label>
                                        <select value={tempTheme} onChange={(e) => setTempTheme(e.target.value)}>
                                            <option value="traditional_indian">Traditional Indian</option>
                                            <option value="contemporary_indian">Contemporary Indian</option>
                                            <option value="rustic_indian">Rustic Indian</option>
                                            <option value="rajasthani_mughal">Rajasthani Mughal</option>
                                        </select>
                                    </div>
                                    <div className="control-group">
                                        <label>Adjust Budget Level</label>
                                        <div className="budget-mini-grid">
                                            {["25000", "60000", "100000"].map(lvl => (
                                                <button
                                                    key={lvl}
                                                    className={tempBudget === lvl ? "active" : ""}
                                                    onClick={() => setTempBudget(lvl)}
                                                >
                                                    ~₹{lvl}
                                                </button>
                                            ))}
                                        </div>
                                    </div>
                                    <button
                                        className="update-btn"
                                        disabled={loading}
                                        onClick={() => handleGenerate(true)}
                                    >
                                        {loading ? <Loader2 className="animate-spin" size={16} /> : <RefreshCw size={16} />}
                                        Update Output
                                    </button>
                                </div>

                                <div className="scene-details mt-4">
                                    <h4><Layout size={16} /> Scene Details</h4>
                                    <div className="analysis-tags">
                                        <span className="tag"><b>Space:</b> {result.scene_analysis.space_type}</span>
                                        <span className="tag"><b>Budget:</b> ₹{result.scene_analysis.budget}</span>
                                    </div>
                                    <h5 className="mt-3">Detected Elements:</h5>
                                    <ul className="element-list">
                                        {result.scene_analysis.detected_elements?.map((el, i) => (
                                            <li key={i}><CheckCircle2 size={12} /> {el}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>

                        {/* Guide Card */}
                        <div className="glass-card full-width guide-card">
                            <h3><Layout size={20} /> Transformation Execution Guide</h3>
                            <div className="guide-content">
                                {result.visuals?.transformation_guide?.split('\n').map((line, i) => (
                                    <p key={i} className={line.startsWith('-') ? 'guide-step' : ''}>{line}</p>
                                ))}
                            </div>
                        </div>

                        {/* Procurement Section */}
                        <div className="procurement-section">
                            <h3><ShoppingBag size={20} /> Curated Procurement Comparison</h3>
                            <p className="section-subtitle">We found the best matches from our Indian Interior Dataset</p>
                            <div className="plans-grid">
                                {result.procurement?.comparison_plans?.map((plan, i) => (
                                    <div key={i} className={`plan-card-result ${i === 0 ? 'featured-plan' : ''}`}>
                                        <div className="plan-meta">
                                            <span className="plan-name">{plan.plan_name}</span>
                                            <span className="plan-total">₹{plan.total_cost.toLocaleString()}</span>
                                        </div>
                                        <p className="savings">Potential Savings: ₹{plan.savings.toLocaleString()}</p>
                                        <ul className="shopping-list">
                                            {plan.items.map((item, j) => (
                                                <li key={j}>
                                                    <div className="item-info">
                                                        <span className="item-type">{item.item_type}</span>
                                                        <span className="selection">{item.selection}</span>
                                                    </div>
                                                    {item.link ? (
                                                        <a href={item.link} target="_blank" rel="noreferrer" className="shop-link">
                                                            {item.price === 0 ? "View Tutorial" : `₹${item.price.toLocaleString()}`} <ChevronRight size={14} />
                                                        </a>
                                                    ) : (
                                                        <span className="no-link">N/A</span>
                                                    )}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Design;