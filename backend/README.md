# CustomsCompass Backend

FastAPI backend for the CustomsCompass Canadian customs compliance platform.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Cache**: Redis
- **Authentication**: JWT (jose)
- **Password Hashing**: bcrypt
- **Validation**: Pydantic v2

## Setup

### 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and update values:

```bash
cp ../.env.example .env
```

Generate a secure SECRET_KEY:

```bash
openssl rand -hex 32
```

### 3. Start Services

Start PostgreSQL, Redis, MinIO, and Mailhog:

```bash
cd ..
docker-compose up -d
```

### 4. Initialize Database

The database will be initialized automatically on first startup. Tables will be created based on SQLAlchemy models.

### 5. Run Development Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive Docs (Swagger): http://localhost:8000/api/docs
- Alternative Docs (ReDoc): http://localhost:8000/api/redoc

## Project Structure

```
backend/
├── api/                    # API routes and dependencies
│   ├── routes/             # Route modules
│   │   └── auth.py         # Authentication routes
│   └── deps.py             # FastAPI dependencies
├── core/                   # Core configuration
│   ├── config.py           # Settings
│   ├── database.py         # Database connection
│   └── security.py         # Auth utilities
├── models/                 # SQLAlchemy models
│   ├── user.py
│   ├── product.py
│   ├── classification.py
│   ├── tariff.py
│   ├── document.py
│   ├── audit.py
│   └── verification.py
├── schemas/                # Pydantic schemas
│   └── user.py
├── services/               # Business logic
└── main.py                 # FastAPI application
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/verify/{token}` - Verify email
- `POST /api/auth/forgot-password` - Request password reset
- `POST /api/auth/reset-password` - Reset password with token

## Database Models

### User
- Authentication and profile information
- Subscription tier tracking
- Market segmentation data
- Account security (lockout, failed attempts)

### Product
- User's product library
- HS code classification results
- Confidence scores
- Supporting documentation flags

### Classification
- Audit trail of all classifications
- AI model results and alternatives
- User corrections
- Processing metadata

### TariffRate
- CBSA tariff schedule data
- Duty rates by trade agreement
- GST/excise flags

### Documents
- Uploaded supporting documents
- Generated customs documents
- OCR extraction results

### AuditLog
- 7-year audit trail (customs requirement)
- All user actions tracked
- IP addresses and user agents

### UsageMonthly
- Monthly usage tracking
- Rate limiting
- Billing metrics

## Security

- **Password**: bcrypt with cost factor 12
- **JWT**: HS256 algorithm, 1-hour access tokens
- **Refresh Tokens**: 7-30 day expiry
- **Account Lockout**: 5 failed attempts, 15-minute lockout
- **Rate Limiting**: Tier-based limits
- **CORS**: Configured for frontend origin

## Testing

```bash
pytest
```

## Development Tips

1. **Auto-reload**: The `--reload` flag watches for code changes
2. **Database changes**: Update models and restart server to recreate tables (use Alembic for production migrations)
3. **API docs**: Use Swagger UI at `/api/docs` for interactive testing
4. **Email testing**: Check Mailhog UI at http://localhost:8025 for sent emails

## License

Proprietary - CustomsCompass
