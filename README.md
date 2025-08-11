# AI Empathy Eval

A full-stack platform for evaluating empathetic decision-making in AI models across high-stakes scenarios.

## Features
- Flask backend with JWT authentication (admin/beta users)
- React frontend for scenario input, results, and human rating
- Model orchestration for GPT-J, LLaMA 2, BLOOM, Decision Tree, Random Forest
- Human rating UI for empathy/explanation
- Admin and beta user roles
- Ready for production and research

---

## Project Structure

```
ai-empathy-eval/
│
├── backend/           # Flask API, DB, model orchestration
│   ├── app.py
│   ├── auth.py
│   ├── config.py
│   ├── ml_models.py
│   ├── models.py
│   ├── requirements.txt
│   └── seed_users.py
│
├── frontend/          # React app (login, scenario, results, rating)
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── ScenarioInputForm.jsx
│   │   │   ├── ResultsTable.jsx
│   │   │   └── HumanRatingUI.jsx
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── README.md
│
├── data/              # Scenario CSVs, outputs, etc.
├── models/            # Your model code (llm_runner.py)
├── eval/              # Metrics and evaluation code (pipeline.py)
├── scripts/           # Utility scripts
├── README.md
└── .env               # (optional) for secrets
```

---

## Setup Instructions

### 1. Backend (Flask)
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python seed_users.py   # Seeds admin and 3 beta users
flask run
```

### 2. Frontend (React)
```bash
cd frontend
npm install
npm start
```

---

## Authentication
- **Admin user:**
  - Username: `admin`
  - Password: `adminpass`
- **Beta users:**
  - Username: `beta1`, Password: `betapass1`
  - Username: `beta2`, Password: `betapass2`
  - Username: `beta3`, Password: `betapass3`

---

## Usage
1. **Login** with one of the above users.
2. **Submit a scenario** (text, reference decision, optional additional data).
3. **View model outputs** (decision, rationale, accuracy).
4. **Rate each model** for empathy and explanation (1–5).
5. **Admin** can register new users via API.

---

## Model Integration
- The backend is ready to connect to your real model code.
- Adapt `backend/ml_models.py` to use your logic from `models/llm_runner.py` and `eval/pipeline.py`.
- See the stub in `ml_models.py` for where to plug in your inference and metrics.

---

## GitHub
- Repo initialized in this folder.
- Remote: `git@github.com:joshua1234511/ai-empathy-eval.git`

---

## Contact
For questions or feature requests, open an issue or contact the maintainer.
