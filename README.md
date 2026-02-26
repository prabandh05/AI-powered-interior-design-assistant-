
# Gruha Assistant: Agentic AI Interior Design 

Gruha Assistant is a state-of-the-art **Agentic AI Interior Design System** designed to transform Indian homes through intelligence, precision, and aesthetic excellence. Leveraging the power of Google's **Gemini 2.5 Flash** and advanced image generation models, it provides a seamless end-to-end design experience—from initial concept to a fully cost-optimized procurement plan.

---

##  Why 4 Agents? The Architecture of Choice

Unlike simple prompt-to-image tools, Gruha Assistant utilizes a **Multi-Agent Orchestration Architecture**. Modern interior design is complex; it requires understanding spatial constraints, thematic consistency, visual inspiration, and financial feasibility. One LLM call cannot handle all these dimensions reliably. 

Our system splits the workload into specialized expert agents:

### 1.  Agent 1: Scene Structuring Expert
**The Goal:** Transform raw, noisy user input into a machine-readable spatial map.  
**Responsibilities:** 
- Analyzes natural language (e.g., "Make my bedroom look like a Rajasthani palace") and uploaded images.
- Normalizes data: identifies space type, detected furniture, and intended budget.
- Outputs a consistent JSON structure that the rest of the pipeline depends on.

### 2.  Agent 2: Design Strategist
**The Goal:** Plan the aesthetic and functional blueprint.  
**Responsibilities:** 
- Interprets the structured scene to determine a precise interior design strategy.
- Selects required furniture items, colors, and materials.
- Generates a "Visual Prompt" specifically optimized for image generation models.
- Acts as the "Creative Director" of the pipeline.

### 3.  Agent 3: Visual Artist & Execution Guide
**The Goal:** Create the "Wow" factor and a roadmap for the user.  
**Responsibilities:** 
- Generates high-fidelity, photorealistic 3D renders using the **Imagen 1.0 Ultra** model.
- Produces a detailed **Transformation Execution Guide**—a step-by-step conceptual roadmap explaining how to achieve the look.

### 4.  Agent 4: Procurement Specialist
**The Goal:** Bridge the gap between inspiration and reality.  
**Responsibilities:** 
- Scans our curated **Indian Interior Dataset** (500+ real products from Indian markets).
- Generates **3 Distinct Procurement Plans**:
    - **Luxury (100% Budget):** Premium selections with no compromises.
    - **Moderate (70% Budget):** High-impact balance of quality and cost.
    - **Minimal (50% Budget):** Budget-friendly essentials and DIY alternatives.
- Provides real shopping links/tutorials for every item.

---

##  Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Google Cloud API Key** (for Gemini)
- **Bytez API Key** (for Image Generation)

### Installation (Backend)
1. Navigate to the root directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your `GOOGLE_API_KEY` and `BYTEZ_API_KEY`.
5. Initialize the database:
   ```bash
   python seed_data.py
   ```
6. Run the server:
   ```bash
   python app.py
   ```

### Installation (Frontend)
1. Navigate to the `frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

---

##  Dashboard & Business Intelligence
The project includes a robust **Admin Intelligence Suite** designed for SaaS-level analytics:
- **Adoption Velocity:** Tracks daily design generation trends.
- **Thematic Matrix:** Visualizes which themes (e.g., Rajasthani vs Contemporary) dominate specific space types.
- **Budget Stratification:** Understand market preferences through budget tier distributions.
- **Geographic Penetration:** Track user engagement across major Indian hubs.

---


**Designed with love for Indian Homes.**
 "Architecture is a visual art, and the buildings speak for themselves." — Gruha Assistant makes that voice yours.
