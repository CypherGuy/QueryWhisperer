# QueryWhisperer (WIP)

QueryWhisperer is a full-stack web app that converts natural language into SQL queries using user-defined database schemas and a modular LLM-powered backend.

## Features

- Natural language to SQL translation via OpenAI API
- Schema-aware prompt engineering for contextually accurate queries
- JWT-based user authentication
- Modular, model-agnostic backend designed for easy extensibility
- Full-stack deployment (frontend + backend + PostgreSQL)
- JSON-based schema upload
- LLM-generated SQL output only (execution planned)

## Tech Stack

**Frontend**

- React (Next.js)
- Tailwind CSS
- TypeScript
- Vercel

**Backend**

- FastAPI
- SQLAlchemy
- PostgreSQL
- OpenAI API (GPT-4o-mini)
- JWT Auth
- Railway

## Setup

**1. Clone the repository**
'git clone https://github.com/CypherGuy/QueryWhisperer.git && cd QueryWhisperer'

**2. Backend Setup**

- Python 3.11+ recommended
- Create a virtual environment and install dependencies:
  'cd backend'
  'pip install -r requirements.txt'

- Create a `.env` file:
  'SECRET_JWT_KEY=your-secret'
  'OPENAI_API_KEY=your-openai-key'
  'DATABASE_URL=postgresql://user:pass@localhost:5432/db'

- Run backend:
  'uvicorn backend.main:app --reload'

**3. Frontend Setup**

- Node 18+ recommended
- Install dependencies:
  'cd frontend'
  'npm install'

- Create `.env.local`:
  'NEXT_PUBLIC_API_URL=http://localhost:8000'

- Start dev server:
  'npm run dev'

## Deployment

You can deploy the frontend, backend and DB together on [Railway](https://railway.app). Set required environment variables in the Railway dashboard.

## Roadmap

- [x] Secure login and user auth
- [x] Schema input + NL → SQL translation
- [x] SQL execution + result display
- [ ] Automatically detect and load database tables
- [ ] Save query history for each user
- [ ] Add admin and user permission levels
- [ ] Improve prompt quality and speed with smarter caching
- [ ] Redesign the interface for a smoother user experience

## Live Demo

🔗 https://querywhisperer.up.railway.app  
🔗 https://github.com/CypherGuy/QueryWhisperer
