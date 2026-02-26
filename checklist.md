Agentic AI Interior Design System
Hackathon Execution Checklist
🚀 PHASE 0 — Project Initialization
🔧 Environment Setup

[*] Create GitHub repository

[ ] Define folder structure

[ ] Setup virtual environment

[ ] Install Flask

[ ] Install required AI SDK (OpenAI / Gemini / etc.)

[ ] Install image processing libraries (Pillow, requests, etc.)

[ ] Add .env file for API keys

[ ] Test basic Flask server runs

🗂 PHASE 1 — Project Structure
📁 Folder Organization

[ ] Create app.py

[ ] Create agents/ folder

[ ] Create dataset/ folder

[ ] Create static/

[ ] Create templates/

[ ] Create utils/

[ ] Add dataset.json

[ ] Add requirements.txt

📝 PHASE 2 — Frontend Form
🖥 Form UI

[ ] Create home page

[ ] Create input form

[ ] Add description text area

[ ] Add image upload field

[ ] Add budget input field

[ ] Add theme dropdown

[ ] Add submit button

[ ] Validate required fields

[ ] Test form submission

🧩 PHASE 3 — Agent 1: Input Structuring Agent
🎯 Responsibilities

[ ] Accept raw form input

[ ] Accept uploaded image

[ ] Send prompt to LLM for structured output

[ ] Force JSON-only response

[ ] Parse JSON safely

[ ] Handle parsing failure fallback

[ ] Return structured scene JSON

🛡 Error Handling

[ ] Handle missing image

[ ] Handle missing theme

[ ] Handle LLM failure

[ ] Add default fallback theme

🎨 PHASE 4 — Agent 2: Design Planner Agent
🧠 Responsibilities

[ ] Receive structured scene JSON

[ ] Generate design summary

[ ] Generate required item_types list

[ ] Assign priority values

[ ] Generate placement suggestions

[ ] Generate visualization prompt

[ ] Force structured JSON output

[ ] Validate JSON format

⚠️ Important

[ ] Do NOT include product links here

[ ] Do NOT include price math here

🖼 PHASE 5 — Agent 3: Visualization Agent
🖌 Responsibilities

[ ] Receive visual prompt

[ ] Call image generation API

[ ] Save generated image URL

[ ] Return JSON with image URL

🛡 Fallback Plan

[ ] If image API fails, show placeholder

[ ] If prompt invalid, retry once

🛒 PHASE 6 — Dataset Creation
📊 Dataset Structure

[ ] Flat list format

 Each item contains:

[ ] item_type

[ ] name

[ ] category

[ ] themes

[ ] price

[ ] product_link

[ ] diy_link

[ ] is_diy flag

🎯 Content Planning

[ ] Finalize 3 themes

[ ] Finalize 6–8 core item_types

[ ] Add 4–5 real items per item_type

[ ] Add 1 DIY option per item_type

[ ] Verify all product links work

[ ] Verify YouTube DIY links work

🧮 PHASE 7 — Agent 4: Procurement & Budget Optimization
🔄 Filtering Logic

[ ] Filter by item_type

[ ] Filter by theme

[ ] Separate real items and DIY items

[ ] Sort real items by price ascending

💰 Budget Logic (Progressive Upgrade Model)

[ ] Start with cheapest variant of each item_type

[ ] Calculate total cost

[ ] Check budget status

[ ] Upgrade highest priority item if possible

[ ] Loop upgrade until budget exhausted

[ ] If item cannot fit → fallback to DIY

[ ] Calculate final total

[ ] Generate cost savings summary

📤 Output JSON Must Include

[ ] selected_products

[ ] diy_recommendations

[ ] total_cost

[ ] budget_status

[ ] optimization_summary

🔁 PHASE 8 — Iteration Logic
🔄 User Modification Support

[ ] Allow theme change

[ ] Allow budget change

[ ] Re-run Agent 2

[ ] Re-run Agent 3

[ ] Re-run Agent 4

[ ] Do NOT re-run Agent 1 unnecessarily

🔗 PHASE 9 — Backend Orchestration
🔄 Pipeline Integration

[ ] Connect Agent 1 → Agent 2

[ ] Connect Agent 2 → Agent 3

[ ] Connect Agent 2 → Agent 4

[ ] Merge final output

[ ] Return single structured response to frontend

🧪 PHASE 10 — Testing
🧪 Test Cases

[ ] High budget case

[ ] Medium budget case

[ ] Very low budget case

[ ] Missing theme case

[ ] No image case

[ ] Image API failure case

[ ] LLM malformed JSON case

🎤 PHASE 11 — Demo Preparation
🎯 Demo Flow

[ ] Prepare 1 strong demo example

[ ] Prepare 1 low-budget example

[ ] Prepare explanation of agent architecture

[ ] Prepare explanation of optimization strategy

[ ] Prepare future AR integration statement

[ ] Practice 2-minute pitch

[ ] Practice live run

📊 PHASE 12 — Architecture Explanation Slide
📐 Include

[ ] Agent diagram

[ ] Modular architecture explanation

[ ] Budget optimization explanation

[ ] Dataset strategy explanation

[ ] Scalability & AR-ready statement

🛡 PHASE 13 — Backup Plan

[ ] Save dataset locally

[ ] Cache one generated image

[ ] Have screenshot backup

[ ] Prepare static demo JSON in case API fails

🏁 FINAL PRE-SUBMISSION CHECK

[ ] No hardcoded API keys

[ ] No broken links

[ ] Clean UI

[ ] No console errors

[ ] All JSON outputs valid

[ ] Budget math verified

[ ] Demo rehearsed

🎯 Team Task Division Example
Member 1 — Backend Orchestration

[ ] Flask setup

[ ] Agent pipeline

[ ] API calls

Member 2 — Dataset & Procurement Logic

[ ] dataset.json

[ ] Budget algorithm

[ ] Upgrade logic

Member 3 — Prompt Engineering

[ ] Agent 1 prompt

[ ] Agent 2 prompt

[ ] Structured JSON enforcement

Member 4 — Frontend & Demo

[ ] UI

[ ] Result rendering

[ ] Demo narration