---
inclusion: manual
---

# Based Labs Directory Structure Guidelines

This document defines the directory structure and organization principles for the Based Labs automated content pipeline project.

## Project Organization

### Root Directory Structure
```
based-labs/
├── automated-content-pipeline/     # Main application (FastAPI + React)
├── brand docs/                    # Brand guidelines and assets
└── .kiro/                        # Kiro IDE configuration and specs
```

### Main Application Structure
```
automated-content-pipeline/
├── app/                          # Python FastAPI application
│   ├── __init__.py
│   ├── main.py                   # FastAPI app entry point
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── v1/                   # API version 1
│   │       ├── __init__.py
│   │       ├── api.py            # Main router
│   │       └── endpoints/        # Individual endpoint modules
│   │           ├── trends.py     # Trend monitoring endpoints
│   │           ├── content.py    # Content generation endpoints
│   │           ├── review.py     # Review workflow endpoints
│   │           └── analytics.py  # Analytics endpoints
│   ├── core/                     # Core application components
│   │   ├── __init__.py
│   │   ├── config.py             # Application configuration
│   │   └── database.py           # Database setup and session management
│   ├── models/                   # SQLAlchemy database models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model with common fields
│   │   ├── trend_opportunity.py  # Trend monitoring models
│   │   ├── generated_content.py  # Content generation models
│   │   ├── content_package.py    # Content packaging models
│   │   ├── post_metrics.py       # Analytics models
│   │   ├── comment.py            # Community engagement models
│   │   ├── response_suggestion.py # Response management models
│   │   └── content_calendar.py   # Calendar and scheduling models
│   ├── schemas/                  # Pydantic schemas for API
│   │   ├── __init__.py
│   │   ├── trend_opportunity.py  # Trend API schemas
│   │   └── content.py            # Content API schemas
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── trend_monitor.py      # Trend monitoring service
│   │   ├── content_generator.py  # AI content generation service
│   │   └── image_generator.py    # Professional image generation service
│   ├── tasks/                    # Celery background tasks
│   │   ├── __init__.py
│   │   ├── trend_monitoring.py   # Background trend monitoring
│   │   └── content_generation.py # Background content generation
│   └── worker.py                 # Celery worker configuration
├── frontend/                     # React dashboard application
│   ├── package.json
│   ├── src/
│   │   ├── App.js                # Main React component
│   │   ├── App.css               # Based Labs styling
│   │   └── components/           # React components
│   │       ├── Dashboard.js      # Main dashboard
│   │       ├── ReviewQueue.js    # Content review interface
│   │       ├── Analytics.js      # Performance analytics
│   │       └── ContentCalendar.js # Content planning
├── templates/                    # Image generation templates
├── fonts/                        # Typography assets
├── tests/                        # Test suite
│   ├── __init__.py
│   └── conftest.py               # Pytest configuration
├── alembic/                      # Database migrations
│   ├── env.py                    # Alembic environment
│   └── script.py.mako            # Migration template
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Development environment
├── Dockerfile                    # Container configuration
├── alembic.ini                   # Database migration config
├── Makefile                      # Development commands
└── README.md                     # Project documentation
```

## File Organization Principles

### 1. Separation of Concerns
- **API Layer** (`app/api/`): HTTP endpoints and request/response handling
- **Business Logic** (`app/services/`): Core application logic and external integrations
- **Data Layer** (`app/models/`): Database models and data structures
- **Background Tasks** (`app/tasks/`): Asynchronous processing

### 2. Modular Design
- Each service handles a specific domain (trends, content, images, analytics)
- Models are organized by functional area
- API endpoints are grouped by feature

### 3. Configuration Management
- Environment-based configuration in `app/core/config.py`
- Database setup centralized in `app/core/database.py`
- Secrets and API keys managed through environment variables

### 4. Testing Structure
- Tests mirror the application structure
- Shared fixtures in `conftest.py`
- Integration tests for complete workflows

## Naming Conventions

### Files and Directories
- **Snake_case** for Python files: `trend_monitor.py`
- **Kebab-case** for directories when needed: `automated-content-pipeline`
- **PascalCase** for React components: `Dashboard.js`

### Python Code
- **PascalCase** for classes: `TrendMonitorService`
- **Snake_case** for functions and variables: `generate_content`
- **UPPER_CASE** for constants: `DEFAULT_POSTING_TIMES`

### Database
- **Snake_case** for table names: `trend_opportunities`
- **Snake_case** for column names: `created_at`
- **Descriptive names** that indicate purpose: `engagement_rate`

## Import Organization

### Python Import Order
1. Standard library imports
2. Third-party imports
3. Local application imports

Example:
```python
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.trend_opportunity import TrendOpportunity
from app.services.trend_monitor import TrendMonitorService
```

## Development Workflow

### Adding New Features
1. **Create models** in `app/models/` if new data structures are needed
2. **Implement services** in `app/services/` for business logic
3. **Add API endpoints** in `app/api/v1/endpoints/`
4. **Create schemas** in `app/schemas/` for API contracts
5. **Add tests** in `tests/` following the same structure
6. **Update documentation** in README files

### Database Changes
1. **Modify models** in `app/models/`
2. **Generate migration**: `make create-migration MESSAGE="description"`
3. **Review migration** in `alembic/versions/`
4. **Apply migration**: `make migrate`

### Frontend Changes
1. **Add components** in `frontend/src/components/`
2. **Update routing** in `frontend/src/App.js`
3. **Maintain styling** consistency with Based Labs brand

## Asset Management

### Templates
- Store in `templates/` directory
- Use descriptive names: `quote_minimal_bg.png`
- Maintain consistent dimensions (1080x1080 for Instagram)

### Fonts
- Store in `fonts/` directory
- Include license information
- Use web-safe fallbacks in code

### Brand Assets
- Maintain in `brand docs/` directory
- Include usage guidelines
- Version control all brand assets

## Configuration Files

### Environment Variables
- Use `.env.example` as template
- Never commit actual `.env` files
- Document all required variables

### Docker Configuration
- `docker-compose.yml` for development
- `Dockerfile` for production builds
- Include health checks and proper networking

### Development Tools
- `Makefile` for common commands
- `alembic.ini` for database migrations
- `requirements.txt` for Python dependencies
- `package.json` for frontend dependencies

## Documentation Standards

### Code Documentation
- Docstrings for all public functions and classes
- Type hints for function parameters and returns
- Inline comments for complex logic

### API Documentation
- FastAPI automatic documentation at `/docs`
- Detailed endpoint descriptions
- Example requests and responses

### Project Documentation
- README files at appropriate levels
- Setup and deployment instructions
- Architecture and design decisions

This structure supports the Based Labs automated content pipeline while maintaining clean separation of concerns, scalability, and developer productivity.