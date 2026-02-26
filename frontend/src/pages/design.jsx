import { useState } from "react";
import bg from "../assets/bg.jpg";   // your collage image
import "./design.css";

function Design() {
    const [budget, setBudget] = useState("");
    const [theme, setTheme] = useState("");
    const [description, setDescription] = useState("");
    const [idea, setIdea] = useState("");
    const [image, setImage] = useState(null);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(URL.createObjectURL(file));
        }
    };

    return (
        <div
            className="design-container"
            style={{
                backgroundImage: `url(${bg})`,
            }}
        >
            <div className="overlay"></div>

            <div className="design-card">
                <h1 className="design-title">Design Your Space</h1>

                <div className="form-group">
                    <label>1. Describe Your Interior</label>
                    <textarea
                        placeholder="Describe your room layout, lighting, furniture, vibe..."
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label>2. Select Budget Level</label>
                    <div className="budget-grid">
                        <div
                            className={`budget-box ${budget === "1" ? "active" : ""}`}
                            onClick={() => setBudget("1")}
                        >
                            Level 1 <br /> ₹1000 – ₹2000
                        </div>
                        <div
                            className={`budget-box ${budget === "2" ? "active" : ""}`}
                            onClick={() => setBudget("2")}
                        >
                            Level 2 <br /> ₹2000 – ₹5000
                        </div>
                        <div
                            className={`budget-box ${budget === "3" ? "active" : ""}`}
                            onClick={() => setBudget("3")}
                        >
                            Level 3 <br /> ₹5000+
                        </div>
                    </div>
                </div>

                <div className="form-group">
                    <label>3. Preferred Theme</label>
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
                    <label>4. Describe Your Idea (Optional)</label>
                    <textarea
                        placeholder="Tell us your dream look, inspirations..."
                        value={idea}
                        onChange={(e) => setIdea(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label>5. Upload Current Room Image</label>
                    <input type="file" accept="image/*" onChange={handleImageUpload} />
                    {image && <img src={image} alt="preview" className="preview-img" />}
                </div>
                <div className="form-group">
                    <label>6. Upload Reference Room Image</label>
                    <input type="file" accept="image/*" onChange={handleImageUpload} />
                    {image && <img src={image} alt="preview" className="preview-img" />}
                </div>

                <button className="generate-btn">
                    Generate Design
                </button>
            </div>
        </div>
    );
}

export default Design;