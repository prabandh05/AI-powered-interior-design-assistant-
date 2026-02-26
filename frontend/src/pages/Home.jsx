import { useNavigate } from "react-router-dom";

import img1 from "../assets/img1.jpg";
import img2 from "../assets/img2.jpg";
import img3 from "../assets/img3.jpg";
import img4 from "../assets/img4.jpg";
import img5 from "../assets/img5.jpg";
import img6 from "../assets/img6.jpg";
import img7 from "../assets/img7.jpg";
import img8 from "../assets/img8.jpg";

function Home() {
    const navigate = useNavigate();

    return (
        <div
            style={{
                display: "flex",
                height: "100vh",
                width: "100%",
                overflow: "hidden",
            }}
        >
            {/* LEFT SIDE */}
            <div
                style={{
                    flex: 1,
                    backgroundImage: `url(${img8})`,
                    backgroundSize: "cover",
                    backgroundPosition: "center",
                    display: "flex",
                    flexDirection: "column",
                    justifyContent: "center",
                    padding: "80px",
                    position: "relative",
                    color: "white",
                }}
            >
                <div
                    style={{
                        position: "absolute",
                        inset: 0,
                        background: "rgba(0,0,0,0.6)",
                    }}
                />

                <div style={{ position: "relative", zIndex: 2 }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "30px" }}>
                        <img src="/favicon.png" alt="Gruha Logo" style={{ width: "50px", height: "50px" }} />
                        <span style={{ fontSize: "24px", fontWeight: "800", letterSpacing: "2px", color: "gold" }}>GRUHA</span>
                    </div>
                    <h1 style={{ fontSize: "48px", marginBottom: "20px" }}>
                        Agentic AI Interior Design
                    </h1>

                    <p style={{ marginBottom: "40px", fontSize: "18px", color: "#ddd" }}>
                        Intelligence. Precision.
                    </p>

                    <button
                        onClick={() => {
                            navigate("/auth");
                        }}
                        style={{
                            padding: "16px 45px",
                            fontSize: "18px",
                            borderRadius: "30px",
                            border: "none",
                            background: "gold",
                            cursor: "pointer",
                            fontWeight: "bold",
                            transition: "0.3s"
                        }}
                    >
                        Get Started
                    </button>
                </div>
            </div>

            {/* RIGHT SIDE */}
            <div
                style={{
                    flex: 1,
                    background: "#000",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                }}
            >
                <div
                    className="rotating-circle"
                    style={{
                        position: "relative",
                        width: "500px",
                        height: "500px",
                    }}
                >
                    {[img1, img2, img3, img4, img5, img6, img7].map(
                        (img, index) => {
                            const angle = (index / 7) * 2 * Math.PI;
                            const radius = 180;

                            const x = 250 + radius * Math.cos(angle) - 80;
                            const y = 250 + radius * Math.sin(angle) - 80;

                            return (
                                <img
                                    key={index}
                                    src={img}
                                    alt="design"
                                    style={{
                                        position: "absolute",
                                        width: "160px",
                                        height: "160px",
                                        objectFit: "cover",
                                        borderRadius: "20px",
                                        left: `${x}px`,
                                        top: `${y}px`,
                                        transform: `rotate(${index % 2 === 0 ? -10 : 10}deg)`,
                                        boxShadow: "0 0 25px rgba(255,255,255,0.4)",
                                    }}
                                />
                            );
                        }
                    )}
                </div>
            </div>
        </div>
    );
}

export default Home;