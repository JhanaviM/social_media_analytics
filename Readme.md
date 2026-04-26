# 📊 Social Media Analytics (SMA) Platform

A full-stack AI-powered social media analytics dashboard with 12 analytical modules covering NLP, ML, network analysis, and more.

---

## 🗂️ Project Structure

```
social-media-analytics/
├── app/
│   ├── __init__.py          ← Flask app factory
│   ├── models.py            ← Database models (User, Case, RawPost, AnalysisResult)
│   ├── auth/
│   │   ├── __init__.py
│   │   └── routes.py        ← Login / Register / Logout
│   ├── modules/
│   │   ├── sentiment.py     ← Module 1: Sentiment Analysis
│   │   ├── trending.py      ← Module 2: Trending Topics
│   │   ├── network.py       ← Module 3: Network Analysis
│   │   ├── recommendation.py← Module 4: Recommendation System
│   │   ├── fake_news.py     ← Module 5: Fake News Detection
│   │   ├── segmentation.py  ← Module 6: User Segmentation
│   │   ├── visualization.py ← Module 7: Data Visualization
│   │   ├── ads.py           ← Module 8: Ad Campaign Optimization
│   │   ├── influencer.py    ← Module 9: Influencer Detection
│   │   ├── realtime.py      ← Module 10: Real-Time Monitoring
│   │   ├── competitor.py    ← Module 11: Competitor Analysis
│   │   ├── prediction.py    ← Module 12: Popularity Prediction
│   │   ├── data_loader.py   ← Apify + Sample data loader
│   │   └── report.py        ← PDF Report generator
│   └── routes/
│       ├── api.py           ← All /api/* endpoints
│       ├── cases.py         ← Case CRUD routes
│       └── dashboard.py     ← Dashboard page routes
├── frontend/
│   ├── templates/           ← Jinja2 HTML templates
│   └── static/
│       ├── css/main.css     ← All styles
│       └── js/
│           ├── main.js      ← Global utilities
│           ├── charts.js    ← Chart.js renderers
│           └── modules.js   ← Module tab interaction
├── data/                    ← Sample datasets
├── .env                     ← Environment variables (DO NOT commit)
├── .gitignore
├── Procfile                 ← For Render/Railway deployment
├── render.yaml              ← Render one-click deploy config
├── requirements.txt
├── runtime.txt
└── run.py                   ← App entry point
```

---

## ⚡ Local Setup (Step by Step)

### Step 1 — Clone from GitHub
```bash
git clone https://github.com/YOUR_USERNAME/social-media-analytics.git
cd social-media-analytics
```

### Step 2 — Create virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables
```bash
cp .env.example .env   # or just edit .env directly
```
Edit `.env` and set:
- `SECRET_KEY` → any random string
- `APIFY_API_TOKEN` → your token from https://console.apify.com/account/integrations

### Step 5 — Run the app
```bash
python run.py
```

Open http://localhost:5000

**Default login: `admin` / `admin123`**

---

## 🚀 Deploy to Render (Free Hosting)

### Option A — One-Click via render.yaml
1. Push your code to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and configures everything
5. Add `APIFY_API_TOKEN` in Environment Variables
6. Click **Deploy** — live in ~3 minutes!

### Option B — Manual Render Setup
1. Go to https://render.com → New → Web Service
2. Connect GitHub repo
3. Set these fields:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
4. Add Environment Variables:
   - `SECRET_KEY` → click "Generate" 
   - `FLASK_ENV` → `production`
   - `FLASK_DEBUG` → `0`
   - `DATABASE_URL` → `sqlite:///sma.db`
   - `APIFY_API_TOKEN` → your token
5. Click **Create Web Service**

### Option C — Deploy to Railway
1. Go to https://railway.app → New Project → Deploy from GitHub
2. Select your repo
3. Add the same environment variables as above
4. Railway auto-detects `Procfile` and deploys

---

## 🔑 Getting Your Apify Token

1. Sign up at https://apify.com (free)
2. Go to https://console.apify.com/account/integrations
3. Copy your **Personal API Token**
4. Paste it in `.env` as `APIFY_API_TOKEN`

**Actors used:**
- X/Twitter: `apidojo/tweet-scraper`
- Facebook: `apidojo/facebook-posts-scraper`

> **No Apify token?** Use the **"Load Sample Data"** button in the app — it generates 100 realistic posts for demo purposes.

---

## 📋 How to Use the App

1. **Register / Login** at `/auth/register`
2. Click **"New Case"** → enter keyword (e.g. Tesla), platform, description
3. Click **"Load Sample Data"** (or connect Apify for real data)
4. Click **"Run All Modules"** — all 12 analyses run automatically
5. Browse each tab: Sentiment, Trending, Network, etc.
6. Click **"Export PDF"** to download the full report

---

## 🧪 12 Analytics Modules

| # | Module | Algorithm |
|---|--------|-----------|
| 1 | Sentiment Analysis | NLTK VADER |
| 2 | Trending Topics | TF-IDF + Frequency |
| 3 | Network Analysis | NetworkX Centrality |
| 4 | Recommendation | Content-Based + Collaborative |
| 5 | Fake News Detection | Rule-based NLP classifier |
| 6 | User Segmentation | KMeans Clustering |
| 7 | Data Visualization | Chart.js + Engagement metrics |
| 8 | Ad Optimization | CTR/ROI/ROAS formulas |
| 9 | Influencer Detection | Eigenvector Centrality |
| 10 | Real-Time Monitoring | Keyword spike detection |
| 11 | Competitor Analysis | Comparative engagement |
| 12 | Popularity Prediction | Random Forest + Gradient Boosting |

---

## 🎓 Tech Stack

- **Backend**: Python 3.11, Flask 3.0, SQLAlchemy
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **ML/NLP**: scikit-learn, NLTK, NetworkX, XGBoost
- **Frontend**: Bootstrap 5, Chart.js 4, Inter font
- **Data**: Apify API
- **Deploy**: Render / Railway

---

*Built for Social Media Analytics course assignment.*
