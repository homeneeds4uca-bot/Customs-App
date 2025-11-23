# CustomsCompass - Canadian Customs Compliance SaaS Platform

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Next.js](https://img.shields.io/badge/next.js-15.0.3-black.svg)
![React](https://img.shields.io/badge/react-19.0.0-blue.svg)

> **AI-powered HS code classification, duty calculator, and document generation for Canadian SMB importers. CARM-compliant customs automation platform.**

## 🎯 Mission

Make customs compliance invisible for SMB importers - from product description to border clearance in 3 clicks.

## ⚠️ Critical Legal Notice

**Per CBSA D-Memorandum D17-2-5 and Section 32 of the Customs Act:**

> "The importer is ultimately responsible for the accounting documentation, payment of duties and taxes, and subsequent corrections such as re-determination of classification, origin and valuation - **even if using the services of a customs broker or software platform.**"

This platform provides classification guidance and calculation tools - **NOT official customs rulings**. Users accept full liability for all customs declarations.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                 │
│  Next.js 15 + React 19 + TypeScript + Tailwind CSS             │
│  Deployed on: Vercel (prod) / localhost:3000 (dev)             │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS/REST
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                         BACKEND                                  │
│  Python FastAPI + SQLAlchemy + PostgreSQL                       │
│  Deployed on: Railway (prod) / localhost:8000 (dev)            │
└────────────────────────────┬────────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
┌──────────────────┐ ┌──────────────┐ ┌────────────────┐
│   PostgreSQL     │ │    Redis     │ │  ML Service    │
│   (Data)         │ │  (Cache)     │ │  (AI Models)   │
└──────────────────┘ └──────────────┘ └────────────────┘
```

## 🚀 Quick Start

> **📖 For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)**

### Prerequisites

- **Python 3.11+** (backend)
- **Node.js 18+** (frontend)
- **Docker Desktop** (for services)
- **Git**

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourcompany/Customs-App.git
cd Customs-App

# Run automated setup
./setup.sh

# Follow the on-screen instructions to start the servers
```

### Option 2: Manual Setup

See detailed manual setup instructions in [QUICKSTART.md](QUICKSTART.md)

### Verify Installation

After starting all services, run the verification script:

```bash
./verify.sh
```

This will check:
- ✓ Docker services (PostgreSQL, Redis, MinIO, Mailhog)
- ✓ Backend API health
- ✓ Frontend accessibility
- ✓ Database connectivity
- ✓ All endpoints responding correctly

### 2. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Generate secure SECRET_KEY
openssl rand -hex 32

# Update .env with your values
nano .env
```

### 3. Start Infrastructure Services

```bash
# Start PostgreSQL, Redis, MinIO, Mailhog
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 4. Start Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --port 8000
```

Backend will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 5. Start Frontend

```bash
# In a new terminal
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

### 6. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | N/A |
| Backend API | http://localhost:8000 | N/A |
| API Docs | http://localhost:8000/api/docs | N/A |
| PostgreSQL | localhost:5432 | customs/customs |
| Redis | localhost:6379 | N/A |
| MinIO Console | http://localhost:9001 | minioadmin/minioadmin |
| Mailhog UI | http://localhost:8025 | N/A |

## 📁 Project Structure

```
Customs-App/
├── frontend/                 # Next.js application
│   ├── app/                  # App router pages
│   │   ├── (auth)/           # Auth pages
│   │   ├── (dashboard)/      # Protected pages
│   │   ├── globals.css       # Global styles
│   │   ├── layout.tsx        # Root layout
│   │   └── page.tsx          # Landing page
│   ├── components/           # React components
│   │   ├── ui/               # Base UI components
│   │   ├── forms/            # Form components
│   │   └── layout/           # Layout components
│   ├── lib/                  # Utilities
│   └── package.json
│
├── backend/                  # FastAPI application
│   ├── api/                  # API routes
│   │   ├── routes/
│   │   │   └── auth.py       # Authentication routes
│   │   └── deps.py           # Dependencies
│   ├── core/                 # Core modules
│   │   ├── config.py         # Settings
│   │   ├── database.py       # DB connection
│   │   └── security.py       # Auth/security
│   ├── models/               # SQLAlchemy models
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── classification.py
│   │   ├── tariff.py
│   │   ├── document.py
│   │   ├── audit.py
│   │   └── verification.py
│   ├── schemas/              # Pydantic schemas
│   │   └── user.py
│   ├── services/             # Business logic
│   ├── main.py               # FastAPI app
│   └── requirements.txt
│
├── ml/                       # ML service
│   ├── models/               # Trained models
│   ├── training/             # Training scripts
│   └── inference/            # Inference API
│
├── docker/                   # Docker configs
├── scripts/                  # Utility scripts
├── docs/                     # Documentation
├── docker-compose.yml        # Local services
└── .env.example              # Environment template
```

## 🔐 Security Features

- **Password**: bcrypt with cost factor 12
- **JWT**: HS256 algorithm, 1-hour access tokens, 7-30 day refresh tokens
- **Account Lockout**: 5 failed attempts = 15-minute lockout
- **Rate Limiting**: Tier-based limits
- **Data Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Data Residency**: Canadian servers (PIPEDA compliant)
- **Audit Trail**: 7-year retention (customs requirement)

## 📊 Database Models

### Core Models

1. **User** - Authentication, profile, subscription tier
2. **Product** - Product library with HS codes
3. **Classification** - AI classification audit trail
4. **TariffRate** - CBSA tariff schedule
5. **UploadedDocument** - Supporting documents
6. **GeneratedDocument** - System-generated documents
7. **AuditLog** - Compliance audit trail
8. **UsageMonthly** - Usage tracking for rate limiting

## 🛣️ Development Roadmap

### Phase 1: MVP (Months 1-6) - Current Phase

- [x] Project infrastructure setup
- [x] Authentication system
- [x] Database schema
- [x] Landing page with liability notice
- [ ] Signup flow with market segmentation
- [ ] Tariff database scraper
- [ ] AI classification engine
- [ ] Duty calculator
- [ ] Document generation
- [ ] Product library UI
- [ ] Beta testing

### Phase 2: Growth (Months 7-12)

- [ ] Document upload & OCR validation
- [ ] Audit trail & compliance dashboard
- [ ] Tariff change alerts
- [ ] CBSA Third-Party Provider application
- [ ] Enhanced reporting
- [ ] Mobile responsive improvements

### Phase 3: US Expansion (Months 13-18)

- [ ] US HTS classification
- [ ] US duty calculator
- [ ] Section 301 tariff tracking
- [ ] Cross-border features
- [ ] Enterprise features (SSO, teams, API)

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov  # With coverage
```

### Frontend Tests

```bash
cd frontend
npm test
npm run test:watch  # Watch mode
```

## 📈 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/verify/{token}` - Verify email
- `POST /api/auth/forgot-password` - Request reset
- `POST /api/auth/reset-password` - Reset password

### Products (Coming Soon)

- `GET /api/products` - List products
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product

### Classification (Coming Soon)

- `POST /api/classify` - Classify product
- `POST /api/classify/batch` - Bulk classify

### Calculator (Coming Soon)

- `POST /api/calculate/duty` - Calculate landed cost

### Documents (Coming Soon)

- `POST /api/documents/invoice` - Generate invoice
- `POST /api/documents/packing-list` - Generate packing list
- `POST /api/documents/coo` - Generate COO

## 🎨 Design System

### Colors

- **Navy** (#102a43 - #627d98) - Primary brand color
- **Gold** (#f59e0b - #fbbf24) - Accent color
- **Semantic** - Success, warning, error states

### Typography

- **Display**: DM Serif Display (headings)
- **Body**: Source Sans 3 (text)
- **Mono**: JetBrains Mono (code)

## 🤝 Contributing

This is a proprietary project. For internal development:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push to branch: `git push origin feature/your-feature`
4. Open a pull request

## 📝 License

Proprietary - CustomsCompass. All rights reserved.

## 📞 Support

- **Email**: support@customscompass.ca
- **Documentation**: [docs.customscompass.ca](https://docs.customscompass.ca)
- **Status**: [status.customscompass.ca](https://status.customscompass.ca)

## 🙏 Acknowledgments

- CBSA for tariff data and rulings
- Canadian importers for feedback and validation
- Open source community for amazing tools

---

**Built with ❤️ in Canada 🇨🇦**
