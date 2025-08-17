---
inclusion: fileMatch
fileMatchPattern: '**/app/**'
---

# Backend Architecture & Technology Stack Guidelines

## Core Technology Standards

### Primary Backend Framework
**FastAPI** is the mandatory framework for all backend services.

**Rationale**: 
- Native async/await support for concurrent external API calls
- Automatic OpenAPI documentation generation
- Built-in request/response validation with Pydantic
- Superior performance compared to Flask/Django
- Modern Python type hints integration

**Usage Guidelines**:
- All API endpoints must use FastAPI decorators and dependency injection
- Implement proper async/await patterns for I/O operations
- Use Pydantic models for all request/response schemas
- Leverage FastAPI's automatic documentation features

### Database Technology
**PostgreSQL** is the primary database for all persistent data.

**Rationale**:
- ACID compliance for data integrity
- Advanced indexing capabilities for performance
- JSON/JSONB support for flexible data structures
- Excellent Python ecosystem support
- Proven scalability for content management systems

**Usage Guidelines**:
- Use SQLAlchemy ORM with async support (AsyncSession)
- Implement proper connection pooling (pool_size: 20, max_overflow: 30)
- All schema changes must go through Alembic migrations
- Use composite indexes for frequently queried columns
- Implement read replicas for scaling when needed

### Caching & Session Management
**Redis** is the standard for caching and session management.

**Rationale**:
- In-memory performance for frequent data access
- Native support for complex data structures
- Excellent integration with Celery for task queues
- Built-in persistence options for durability
- Atomic operations for concurrent access

**Usage Guidelines**:
- Use separate Redis databases for different purposes (sessions: db=0, celery: db=1, cache: db=2)
- Implement proper connection pooling and timeout handling
- Use Redis for API response caching (especially OpenAI calls)
- Store task results and status in Redis
- Implement cache invalidation strategies

### Background Task Processing
**Celery** is the required solution for all background processing.

**Rationale**:
- Mature and battle-tested for production workloads
- Excellent Redis integration for message brokering
- Built-in retry mechanisms and error handling
- Task routing and priority queue support
- Comprehensive monitoring and debugging tools

**Usage Guidelines**:
- Use separate queues for different task types (content, images, publishing, analytics)
- Implement proper retry logic with exponential backoff
- Use task routing to distribute load across workers
- Monitor task performance and queue lengths
- Implement proper error handling and logging

## External API Integration Standards

### AI Content Generation
**OpenAI GPT-4** is the primary AI service for content generation.

**Required Implementation Patterns**:
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def generate_content(prompt: str) -> str:
    # Implementation with proper error handling
```

**Usage Guidelines**:
- Always implement retry logic with exponential backoff
- Cache responses to reduce API costs and improve performance
- Use structured prompts with Based Labs brand voice integration
- Implement fallback strategies for API failures
- Monitor token usage and implement cost controls

### Social Media APIs
**Instagram Creator Studio API** and **LinkedIn API v2** are the approved platforms.

**Usage Guidelines**:
- Implement platform-specific adapters with common interface
- Handle rate limiting and API quotas properly
- Use webhook endpoints for real-time updates when available
- Implement proper error handling for publishing failures
- Store API credentials securely using environment variables

### Image Processing
**OpenCV**, **Pillow (PIL)**, and **ImageMagick (Wand)** are the approved libraries.

**Usage Guidelines**:
- Use OpenCV for advanced image processing and effects
- Use Pillow for basic image operations and format conversions
- Use ImageMagick (Wand) for professional-grade effects
- Implement proper memory management for large images
- Use async processing for batch image operations

## Security Standards

### Authentication & Authorization
**JWT tokens** with **HTTPBearer** security scheme.

**Implementation Requirements**:
```python
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

async def get_current_user(credentials = Depends(security)):
    # JWT validation implementation
```

### Input Validation
**Pydantic models** for all input validation with **bleach** for sanitization.

**Usage Guidelines**:
- Use Pydantic validators for complex validation logic
- Sanitize all user input using bleach library
- Implement proper error messages for validation failures
- Use Field constraints for basic validation (min_length, max_length, regex)

### Rate Limiting
**slowapi** for API rate limiting implementation.

**Standard Limits**:
- Content generation: 10 requests/minute per IP
- Image generation: 5 requests/minute per IP
- Publishing: 20 requests/hour per user
- Analytics: 100 requests/minute per user

## Development Standards

### Code Quality
**Mandatory tools and standards**:
- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **mypy** for type checking
- **flake8** for linting
- **pytest** for testing (minimum 80% coverage)

### Project Structure
```
app/
├── api/                 # API route definitions
│   └── v1/             # API version 1
├── core/               # Core application logic
├── db/                 # Database models and utilities
├── services/           # Business logic services
├── schemas/            # Pydantic models
├── utils/              # Utility functions
└── main.py            # FastAPI application entry point
```

### Environment Configuration
**Pydantic Settings** for all configuration management.

**Required Implementation**:
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    openai_api_key: str
    
    class Config:
        env_file = ".env"
```

### Error Handling
**Structured error responses** with proper HTTP status codes.

**Standard Error Format**:
```python
{
    "error_code": "CONTENT_001",
    "message": "Content generation failed",
    "timestamp": "2025-01-17T10:30:00Z",
    "details": {}
}
```

## Monitoring & Observability

### Logging
**structlog** for structured logging with JSON output.

**Required Log Fields**:
- timestamp (ISO format)
- log_level
- service_name
- request_id
- user_id (when available)
- error_details (for errors)

### Health Checks
**Mandatory health check endpoint** at `/health`.

**Required Checks**:
- Database connectivity
- Redis connectivity
- External API availability (OpenAI, social media)
- Disk space and memory usage

### Metrics
**Prometheus metrics** for monitoring and alerting.

**Required Metrics**:
- HTTP request count and duration
- Database query performance
- External API response times
- Task queue lengths and processing times
- Error rates by service and endpoint

## Performance Standards

### Response Time Requirements
- API endpoints: < 200ms for 95th percentile
- Content generation: < 3 seconds
- Image generation: < 500ms
- Database queries: < 100ms for simple queries

### Scalability Guidelines
- Design all services to be stateless
- Use connection pooling for database and Redis
- Implement proper caching strategies
- Use async/await for I/O bound operations
- Design for horizontal scaling from day one

### Resource Management
- Implement proper connection pooling
- Use context managers for resource cleanup
- Monitor memory usage for image processing
- Implement proper timeout handling for external APIs

## Deployment Standards

### Containerization
**Docker** is mandatory for all services.

**Required Dockerfile Standards**:
- Use official Python slim images
- Create non-root user for security
- Implement proper health checks
- Use multi-stage builds for optimization
- Pin all dependency versions

### Environment Management
**Separate configurations** for development, staging, and production.

**Required Environment Variables**:
- Database connection strings
- Redis connection strings
- External API keys and tokens
- Security keys and secrets
- Feature flags and configuration

### CI/CD Pipeline
**GitHub Actions** for continuous integration and deployment.

**Required Pipeline Steps**:
1. Code quality checks (black, isort, flake8, mypy)
2. Unit and integration tests
3. Security scanning
4. Docker image building
5. Deployment to staging
6. Automated testing in staging
7. Production deployment (manual approval)

## Library Version Management

### Core Dependencies
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy[asyncio]>=2.0.0
alembic>=1.12.0
redis>=5.0.0
celery>=5.3.0
pydantic>=2.5.0
asyncpg>=0.29.0
psycopg2-binary>=2.9.0
python-dotenv>=1.0.0
structlog>=23.2.0
```

**Usage Guidelines**:
- **FastAPI**: Primary web framework for all API endpoints
- **Uvicorn**: ASGI server with standard extras for production
- **SQLAlchemy**: ORM with async support for database operations
- **Alembic**: Database migration management
- **Redis**: Caching, session management, and Celery message broker
- **Celery**: Background task processing and job queues
- **Pydantic**: Data validation and serialization
- **asyncpg**: Async PostgreSQL driver for high performance
- **psycopg2-binary**: PostgreSQL adapter for SQLAlchemy
- **python-dotenv**: Environment variable management
- **structlog**: Structured logging with JSON output

### AI & Content Processing
```
openai>=1.3.0
pillow>=10.0.0
opencv-python>=4.8.0
Wand>=0.6.0
numpy>=1.24.0
nltk>=3.8.0
textblob>=0.17.0
tenacity>=8.2.0
```

**Usage Guidelines**:
- **OpenAI**: Primary AI service for content generation with GPT-4
- **Pillow (PIL)**: Basic image operations, format conversions, and text rendering
- **OpenCV**: Advanced image processing, color grading, and professional effects
- **Wand (ImageMagick)**: Professional-grade image effects and transformations
- **NumPy**: Numerical operations for image arrays and data processing
- **NLTK**: Natural language processing for content analysis and sentiment analysis
- **TextBlob**: Simple text processing and sentiment analysis
- **Tenacity**: Retry logic with exponential backoff for external API calls

### Security & Validation
```
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.0
python-multipart>=0.0.6
bleach>=6.0.0
slowapi>=0.1.9
```

### Monitoring & Observability
```
prometheus-client>=0.19.0
structlog>=23.2.0
sentry-sdk[fastapi]>=1.38.0
python-json-logger>=2.0.0
```

**Usage Guidelines**:
- **prometheus-client**: Metrics collection and monitoring
- **structlog**: Structured logging with JSON output
- **sentry-sdk**: Error tracking and performance monitoring
- **python-json-logger**: JSON log formatting for structured logging

### Development & Testing
```
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
black>=23.9.0
isort>=5.12.0
mypy>=1.6.0
flake8>=6.1.0
pre-commit>=3.5.0
httpx>=0.25.0
factory-boy>=3.3.0
```

**Usage Guidelines**:
- **pytest**: Primary testing framework with async support
- **pytest-asyncio**: Async test support for FastAPI endpoints
- **pytest-cov**: Code coverage reporting (minimum 80% required)
- **black**: Code formatting with 88 character line length
- **isort**: Import sorting and organization
- **mypy**: Static type checking for Python code
- **flake8**: Code linting and style checking
- **pre-commit**: Git hooks for code quality enforcement
- **httpx**: HTTP client for testing API endpoints
- **factory-boy**: Test data generation and fixtures

## Migration and Upgrade Policies

### Database Migrations
- All schema changes must be backward compatible
- Use Alembic for all database migrations
- Test migrations on staging before production
- Implement rollback procedures for all changes

### Dependency Updates
- Update dependencies monthly for security patches
- Test all updates in development environment first
- Use dependabot for automated security updates
- Pin major versions to prevent breaking changes

### API Versioning
- Use URL path versioning (/api/v1/, /api/v2/)
- Maintain backward compatibility for at least 6 months
- Provide clear deprecation notices and migration guides
- Use semantic versioning for API releases

## Compliance and Best Practices

### Data Privacy
- Implement proper data encryption at rest and in transit
- Use secure headers for all API responses
- Implement proper session management
- Follow GDPR guidelines for user data handling

### Performance Optimization
- Use database indexes for all frequently queried columns
- Implement proper caching strategies
- Use connection pooling for all external services
- Monitor and optimize slow queries regularly

### Code Review Standards
- All code must be reviewed by at least one other developer
- Use pull request templates for consistent reviews
- Require passing tests before merge
- Implement automated code quality checks

This document serves as the definitive guide for all backend development decisions. Any deviations must be approved by the technical lead and documented with clear rationale.