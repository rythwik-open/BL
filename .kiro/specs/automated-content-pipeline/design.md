# Design Document

## Overview

The Based Labs Automated Content Pipeline is designed as a modular, event-driven system that transforms content curation into published social media posts. The architecture prioritizes maintainability, scalability, and brand consistency while enabling a solo operator to manage high-quality content at scale.

The system follows a microservices-inspired approach with clear separation of concerns: content curation, AI generation, image processing, publishing, and analytics. Each component can be developed, tested, and scaled independently while maintaining tight integration through well-defined APIs.

## Architecture

### High-Level System Architecture

```mermaid
graph TB
    subgraph "Content Sources"
        A[News APIs]
        B[Reddit API]
        C[Community Input]
        D[Manual Requests]
    end
    
    subgraph "Core Pipeline"
        E[Trend Monitor]
        F[Content Generator]
        G[Image Generator]
        H[Review Queue]
        I[Scheduler]
        J[Publisher]
        R[Community Manager]
        S[Content Calendar]
    end
    
    subgraph "External Services"
        K[OpenAI API]
        L[Instagram API]
        M[LinkedIn API]
        N[Analytics APIs]
    end
    
    subgraph "Data Layer"
        O[PostgreSQL]
        P[Redis Cache]
        Q[File Storage]
    end
    
    A --> E
    B --> E
    C --> E
    D --> F
    E --> F
    F --> K
    F --> G
    G --> H
    H --> I
    I --> J
    J --> L
    J --> M
    J --> N
    J --> R
    R --> F
    S --> I
    S --> F
    
    E --> O
    F --> O
    G --> Q
    H --> O
    I --> P
    J --> O
    N --> O
    R --> O
    S --> O
```

### Component Architecture

The system is built using FastAPI as the core framework with the following key components:

1. **Trend Monitor Service**: Continuously monitors external sources for content opportunities
2. **Content Generation Service**: Uses AI to create brand-consistent content
3. **Image Generation Service**: Creates professional visuals using the existing BasedLabsImageGenerator
4. **Review and Approval Service**: Manages human oversight workflow
5. **Publishing Service**: Handles multi-platform posting and scheduling
6. **Analytics Service**: Tracks performance and provides insights
7. **Community Engagement Service**: Manages community interactions and response suggestions
8. **Content Calendar Service**: Provides planning and campaign management capabilities
9. **Orchestration Service**: Coordinates the entire pipeline

## Components and Interfaces

### 1. Trend Monitor Service

**Purpose**: Continuously scan external sources for content opportunities aligned with Based Labs themes.

**Key Interfaces**:
```python
class TrendMonitorService:
    async def scan_news_sources() -> List[TrendOpportunity]
    async def analyze_reddit_discussions() -> List[TrendOpportunity]
    async def process_community_input() -> List[TrendOpportunity]
    async def score_opportunity(opportunity: TrendOpportunity) -> float
```

**Data Sources**:
- News APIs (NewsAPI, Reddit API)
- RSS feeds from relevant publications
- Community Discord/Telegram channels
- Manual trend submissions

**Scoring Algorithm**:
- Brand alignment (40%): System friction, permission barriers, gatekeeping mechanisms, individual workarounds
- Timeliness (30%): Trending topics, breaking news, community discussions
- Engagement potential (20%): Historical performance of similar content, provocative level alignment (7/10)
- Uniqueness (10%): Differentiation from existing content

**Community Input Processing**:
- Comment and question analysis for content ideas
- Identification of common frustrations and system barriers
- Conversion of community discussions into content opportunities

### 2. Content Generation Service

**Purpose**: Transform trend opportunities into brand-consistent content using AI.

**Key Interfaces**:
```python
class ContentGenerationService:
    async def generate_content(opportunity: TrendOpportunity) -> GeneratedContent
    async def select_template(content: GeneratedContent) -> str
    async def validate_brand_voice(content: GeneratedContent) -> bool
    async def optimize_for_platform(content: GeneratedContent, platform: str) -> GeneratedContent
```

**AI Integration**:
- OpenAI GPT-4 with custom system prompts enforcing 7/10 provocative level
- Based Labs steering files integration for brand voice consistency
- Proven hook formulas: "You're waiting for permission that will never come", "This rule made sense in 1950. It's destroying you in 2025"
- Template selection logic based on character count and content analysis
- Quality validation with automatic regeneration until standards are met

**Content Types and Selection Logic**:
- Quote posts: Provocative statements under 100 characters (quote_minimal template)
- Long-form posts: Educational content 100-800 characters (long_form template)
- Carousel series: Multi-slide content over 800 characters (carousel format)
- Automatic content type detection based on character count and content structure

**Content Quality Requirements**:
- Clear value proposition for the reader
- Specific next action or call-to-action
- Connection to Based Labs philosophy (agency, systems, decentralization)
- Adherence to 7/10 provocative level calibration

### 3. Image Generation Service

**Purpose**: Create professional visuals using the existing BasedLabsImageGenerator.

**Key Interfaces**:
```python
class ImageGenerationService:
    async def generate_image(content: GeneratedContent, template: str) -> Image
    async def apply_brand_effects(image: Image) -> Image
    async def optimize_for_platform(image: Image, platform: str) -> Image
    async def generate_variations(content: GeneratedContent) -> List[Image]
```

**Integration with Existing System**:
- Extends current BasedLabsImageGenerator
- Maintains existing template system
- Preserves professional effects pipeline
- Adds batch processing capabilities

### 4. Review and Approval Service

**Purpose**: Manage human oversight workflow for content quality control.

**Key Interfaces**:
```python
class ReviewService:
    async def queue_for_review(content_package: ContentPackage) -> str
    async def get_pending_reviews() -> List[ContentPackage]
    async def approve_content(review_id: str, feedback: str) -> bool
    async def reject_content(review_id: str, feedback: str) -> bool
```

**Review Dashboard Features**:
- Side-by-side content and image preview
- Brand guideline checklist
- One-click approval/rejection
- Feedback collection for AI improvement
- Batch review capabilities

### 5. Publishing Service

**Purpose**: Handle multi-platform posting and scheduling.

**Key Interfaces**:
```python
class PublishingService:
    async def schedule_post(content_package: ContentPackage, platform: str, schedule_time: datetime) -> str
    async def publish_immediately(content_package: ContentPackage, platform: str) -> PublishResult
    async def get_optimal_posting_time(platform: str, content_type: str) -> datetime
    async def handle_publishing_failure(post_id: str, error: str) -> None
```

**Platform Integrations**:
- Instagram: Creator Studio API with visual-first optimization and scroll-stopping hooks
- LinkedIn: LinkedIn API v2 with professional/business context framing for thought leadership
- Platform-specific hashtag generation (#agency #systems #decentralized #futureofwork for Instagram)
- Future platforms: Extensible adapter pattern

**Scheduling Logic**:
- Optimal timing: Instagram (11 AM, 2 PM, 5 PM EST), LinkedIn (8 AM, 12 PM, 6 PM EST)
- Weekly content mix: Monday (system critique), Wednesday (framework/tool), Friday (community spotlight)
- Content mix balancing with automatic adjustment recommendations
- Rate limiting and API quota management
- Automatic carousel creation for content exceeding platform limits

### 6. Analytics Service

**Purpose**: Track performance and provide insights for continuous improvement.

**Key Interfaces**:
```python
class AnalyticsService:
    async def track_post_performance(post_id: str, metrics: PostMetrics) -> None
    async def analyze_content_patterns() -> ContentInsights
    async def generate_performance_report(timeframe: str) -> PerformanceReport
    async def identify_optimization_opportunities() -> List[Optimization]
```

### 7. Community Engagement Service

**Purpose**: Manage community interactions and convert engagement into content opportunities.

**Key Interfaces**:
```python
class CommunityEngagementService:
    async def categorize_comments(comments: List[Comment]) -> Dict[str, List[Comment]]
    async def identify_content_opportunities(comments: List[Comment]) -> List[ContentOpportunity]
    async def generate_response_suggestions(message: str, context: str) -> List[ResponseSuggestion]
    async def analyze_community_sentiment(interactions: List[Interaction]) -> SentimentAnalysis
    async def provide_criticism_guidance(feedback: str) -> ResponseGuidance
```

**Comment Categorization**:
- Questions: Opportunities for educational content
- Feedback: Insights for content improvement
- Spam: Automatic filtering and removal
- Engagement: High-value interactions for community building

**Response Generation**:
- Based Labs engagement templates integration
- Context-aware suggestions using AI
- Constructive criticism handling guidelines
- Community question conversion to content topics

### 8. Content Calendar Service

**Purpose**: Provide strategic content planning and campaign management capabilities.

**Key Interfaces**:
```python
class ContentCalendarService:
    async def get_content_calendar(timeframe: str) -> ContentCalendar
    async def identify_content_gaps() -> List[ContentGap]
    async def suggest_campaign_content(theme: str, duration: int) -> List[ContentSuggestion]
    async def balance_content_pillars() -> ContentBalanceReport
    async def schedule_special_events(events: List[Event]) -> List[ContentOpportunity]
```

**Calendar Features**:
- Scheduled posts visualization with content themes
- Content pillar distribution tracking (system critique, frameworks, community)
- Campaign planning with manual content request capabilities
- Special event and date-based content suggestions
- Content gap identification and filling recommendations
- Posting frequency optimization

**Metrics Tracked**:
- Engagement rates (likes, comments, shares, saves) with 2% threshold monitoring
- Save rates with 1% threshold for practical value assessment
- Click-through rates to newsletter/website
- Audience growth and retention
- Content type performance comparison (hooks, topics, formats, timing)
- Optimal posting time analysis
- Performance pattern identification for high-performing content

**Performance-Based Learning**:
- Automatic flagging when engagement falls below 2%
- Suggestions for increasing provocative level or improving hooks
- Practical value enhancement recommendations for low save rates
- Continuous feedback loop into content generation algorithms

## Data Models

### Core Data Structures

```python
@dataclass
class TrendOpportunity:
    id: str
    source: str  # news, reddit, community, manual
    title: str
    description: str
    url: Optional[str]
    relevance_score: float
    created_at: datetime
    processed: bool

@dataclass
class GeneratedContent:
    id: str
    opportunity_id: str
    content_type: str  # quote, long_form, carousel
    main_text: str
    title: Optional[str]
    description: Optional[str]
    cta: Optional[str]
    attribution: Optional[str]
    template_suggestion: str
    brand_voice_score: float
    created_at: datetime

@dataclass
class ContentPackage:
    id: str
    content: GeneratedContent
    image_path: str
    platform: str
    status: str  # pending, approved, rejected, scheduled, published
    review_feedback: Optional[str]
    scheduled_time: Optional[datetime]
    published_time: Optional[datetime]

@dataclass
class PostMetrics:
    post_id: str
    platform: str
    likes: int
    comments: int
    shares: int
    saves: int
    impressions: int
    reach: int
    click_through_rate: float
    engagement_rate: float
    collected_at: datetime

@dataclass
class Comment:
    id: str
    post_id: str
    platform: str
    author: str
    text: str
    category: str  # question, feedback, spam, engagement
    sentiment: float
    created_at: datetime

@dataclass
class ResponseSuggestion:
    comment_id: str
    suggested_response: str
    response_type: str  # educational, engagement, redirect
    confidence_score: float
    template_used: str

@dataclass
class ContentCalendarEntry:
    id: str
    scheduled_date: datetime
    content_theme: str  # system_critique, framework, community_spotlight
    platform: str
    status: str  # planned, generated, approved, published
    content_pillar: str
```

### Database Schema

```sql
-- Trend opportunities
CREATE TABLE trend_opportunities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    url TEXT,
    relevance_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);

-- Generated content
CREATE TABLE generated_content (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    opportunity_id UUID REFERENCES trend_opportunities(id),
    content_type VARCHAR(20) NOT NULL,
    main_text TEXT NOT NULL,
    title TEXT,
    description TEXT,
    cta TEXT,
    attribution TEXT,
    template_suggestion VARCHAR(50),
    brand_voice_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content packages (content + image + metadata)
CREATE TABLE content_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES generated_content(id),
    image_path TEXT,
    platform VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    review_feedback TEXT,
    scheduled_time TIMESTAMP,
    published_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Post performance metrics
CREATE TABLE post_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    package_id UUID REFERENCES content_packages(id),
    platform VARCHAR(20),
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    click_through_rate FLOAT DEFAULT 0,
    engagement_rate FLOAT DEFAULT 0,
    collected_at TIMESTAMP DEFAULT NOW()
);

-- Community comments and interactions
CREATE TABLE comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id VARCHAR(100),
    platform VARCHAR(20),
    author VARCHAR(100),
    text TEXT,
    category VARCHAR(20), -- question, feedback, spam, engagement
    sentiment FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Response suggestions for community management
CREATE TABLE response_suggestions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    comment_id UUID REFERENCES comments(id),
    suggested_response TEXT,
    response_type VARCHAR(20), -- educational, engagement, redirect
    confidence_score FLOAT,
    template_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Content calendar entries
CREATE TABLE content_calendar (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scheduled_date TIMESTAMP,
    content_theme VARCHAR(50), -- system_critique, framework, community_spotlight
    platform VARCHAR(20),
    status VARCHAR(20) DEFAULT 'planned', -- planned, generated, approved, published
    content_pillar VARCHAR(50),
    package_id UUID REFERENCES content_packages(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- System configuration
CREATE TABLE system_config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB,
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Error Handling

### Error Categories and Strategies

1. **External API Failures**
   - Retry with exponential backoff
   - Circuit breaker pattern for persistent failures
   - Fallback to cached data when available
   - Graceful degradation of features

2. **Content Generation Failures**
   - Multiple AI model fallbacks (GPT-4 → GPT-3.5 → Claude)
   - Template-based content generation as last resort
   - Human notification for persistent failures
   - Content queue management to prevent blocking

3. **Image Generation Failures**
   - Fallback to simpler templates
   - Text-only content options
   - Error logging with context for debugging
   - Automatic retry with different parameters

4. **Publishing Failures**
   - Automatic retry with different timing
   - Manual publishing workflow as fallback
   - Platform-specific error handling (Instagram Creator Studio API, LinkedIn API v2)
   - User notification with manual posting instructions
   - Automatic carousel creation for content exceeding platform limits

5. **Review Process Failures**
   - 24-hour reminder notifications for pending reviews
   - Escalation workflows for overdue approvals
   - Feedback collection and learning integration
   - Quality filter bypass for urgent content

### Error Recovery Workflows

```python
class ErrorHandler:
    async def handle_api_failure(service: str, error: Exception) -> RecoveryAction
    async def handle_content_generation_failure(opportunity: TrendOpportunity) -> RecoveryAction
    async def handle_publishing_failure(package: ContentPackage) -> RecoveryAction
    async def escalate_to_human(error_context: ErrorContext) -> None
```

## Testing Strategy

### Unit Testing
- Individual service components
- Data model validation
- Business logic functions
- Error handling scenarios

### Integration Testing
- API endpoint testing
- Database operations
- External service integrations
- End-to-end pipeline flows

### Performance Testing
- Content generation throughput
- Image processing speed
- Database query optimization
- API response times

### Brand Consistency Testing
- Automated brand voice validation with 7/10 provocative level verification
- Template rendering verification (quote_minimal, long_form, carousel)
- Content quality scoring against Based Labs guidelines
- Visual brand compliance (neon green #00ff00, black backgrounds, high contrast)
- Hook formula validation and effectiveness testing

### Community Engagement Testing
- Comment categorization accuracy testing
- Response suggestion quality validation
- Sentiment analysis accuracy verification
- Content opportunity identification from community input

### Content Calendar Testing
- Content pillar distribution validation
- Scheduling optimization verification
- Campaign planning functionality testing
- Content gap identification accuracy

### Test Data Management
```python
# Test fixtures for consistent testing
@pytest.fixture
def sample_trend_opportunity():
    return TrendOpportunity(
        source="news",
        title="New AI regulation proposed",
        description="Government proposes new AI oversight rules",
        relevance_score=0.85
    )

@pytest.fixture
def sample_generated_content():
    return GeneratedContent(
        content_type="quote",
        main_text="You don't need permission to innovate",
        template_suggestion="quote_post",
        brand_voice_score=0.9
    )
```

### Continuous Integration Pipeline
1. **Code Quality**: Black formatting, type checking, linting
2. **Unit Tests**: 90%+ coverage requirement
3. **Integration Tests**: API and database testing
4. **Brand Compliance**: Automated brand voice validation
5. **Performance Tests**: Response time and throughput benchmarks
6. **Security Scanning**: Dependency and code security analysis

## Backend Architecture & Technology Stack

### Core Backend Framework

**FastAPI** serves as the primary backend framework, chosen for:
- **Async/await support**: Essential for handling multiple external API calls concurrently
- **Automatic API documentation**: Built-in OpenAPI/Swagger documentation generation
- **Type safety**: Full Python type hints integration with Pydantic models
- **Performance**: One of the fastest Python web frameworks available
- **Modern Python features**: Full support for Python 3.8+ features

### Database Architecture

**PostgreSQL** as the primary database with the following design principles:

#### Connection Management
```python
# Database connection pool configuration
DATABASE_CONFIG = {
    "pool_size": 20,
    "max_overflow": 30,
    "pool_timeout": 30,
    "pool_recycle": 3600,
    "echo": False  # Set to True for SQL debugging
}

# Async SQLAlchemy setup
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL, **DATABASE_CONFIG)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

#### Migration Strategy
- **Alembic** for database migrations with automatic model detection
- **Version control**: All schema changes tracked in git
- **Rollback capability**: Every migration includes downgrade path
- **Environment separation**: Separate migration paths for dev/staging/prod

#### Performance Optimization
- **Indexing strategy**: Composite indexes on frequently queried columns
- **Query optimization**: SQLAlchemy query profiling and optimization
- **Connection pooling**: Optimized pool sizes based on concurrent load
- **Read replicas**: Future scaling with read-only database replicas

### Caching Layer

**Redis** implementation for multiple use cases:

#### Session Management
```python
# Redis session configuration
REDIS_SESSION_CONFIG = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
    "decode_responses": True,
    "socket_timeout": 5,
    "socket_connect_timeout": 5,
    "retry_on_timeout": True
}
```

#### Task Queue Backend
- **Celery integration**: Redis as message broker for background tasks
- **Result backend**: Store task results and status in Redis
- **Task routing**: Different queues for different task types (content generation, image processing, publishing)

#### Application Caching
- **API response caching**: Cache expensive API calls (OpenAI, social media APIs)
- **Content caching**: Cache generated content and images
- **Analytics caching**: Cache performance metrics and reports

### Background Task Processing

**Celery** configuration for asynchronous task processing:

```python
# Celery configuration
CELERY_CONFIG = {
    "broker_url": "redis://localhost:6379/1",
    "result_backend": "redis://localhost:6379/2",
    "task_serializer": "json",
    "accept_content": ["json"],
    "result_serializer": "json",
    "timezone": "UTC",
    "enable_utc": True,
    "task_routes": {
        "content_generation.*": {"queue": "content"},
        "image_processing.*": {"queue": "images"},
        "publishing.*": {"queue": "publishing"},
        "analytics.*": {"queue": "analytics"}
    }
}
```

#### Task Categories
1. **Content Generation Tasks**: AI content creation, brand voice validation
2. **Image Processing Tasks**: Image generation, optimization, format conversion
3. **Publishing Tasks**: Social media posting, scheduling, retry logic
4. **Analytics Tasks**: Performance data collection, report generation
5. **Monitoring Tasks**: Health checks, system metrics collection

### API Design Patterns

#### RESTful API Structure
```python
# API versioning and structure
/api/v1/trends/                    # Trend monitoring endpoints
/api/v1/content/                   # Content generation endpoints
/api/v1/images/                    # Image generation endpoints
/api/v1/publishing/                # Publishing and scheduling endpoints
/api/v1/analytics/                 # Performance and analytics endpoints
/api/v1/community/                 # Community engagement endpoints
/api/v1/calendar/                  # Content calendar endpoints
```

#### Request/Response Models
```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ContentGenerationRequest(BaseModel):
    trend_opportunity_id: str = Field(..., description="UUID of the trend opportunity")
    content_type: str = Field(..., regex="^(quote|long_form|carousel)$")
    platform: str = Field(..., regex="^(instagram|linkedin)$")
    custom_prompt: Optional[str] = Field(None, max_length=500)

class ContentGenerationResponse(BaseModel):
    content_id: str
    generated_content: GeneratedContent
    image_url: Optional[str]
    estimated_engagement: float
    brand_voice_score: float
    created_at: datetime
```

#### Error Handling Standards
```python
from fastapi import HTTPException
from enum import Enum

class ErrorCode(Enum):
    CONTENT_GENERATION_FAILED = "CONTENT_001"
    IMAGE_GENERATION_FAILED = "IMAGE_001"
    PUBLISHING_FAILED = "PUBLISH_001"
    EXTERNAL_API_ERROR = "API_001"

class APIError(HTTPException):
    def __init__(self, error_code: ErrorCode, detail: str, status_code: int = 500):
        super().__init__(status_code=status_code, detail={
            "error_code": error_code.value,
            "message": detail,
            "timestamp": datetime.utcnow().isoformat()
        })
```

### External API Integration

#### OpenAI Integration
```python
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

class OpenAIService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_content(self, prompt: str, max_tokens: int = 500) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": BASED_LABS_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
```

#### Social Media API Integration
```python
class SocialMediaPublisher:
    def __init__(self):
        self.instagram_client = InstagramAPI(access_token=settings.INSTAGRAM_TOKEN)
        self.linkedin_client = LinkedInAPI(access_token=settings.LINKEDIN_TOKEN)
    
    async def publish_to_platform(self, content: ContentPackage, platform: str) -> PublishResult:
        if platform == "instagram":
            return await self._publish_instagram(content)
        elif platform == "linkedin":
            return await self._publish_linkedin(content)
        else:
            raise ValueError(f"Unsupported platform: {platform}")
```

### Security Implementation

#### Authentication & Authorization
```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
```

#### API Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/content/generate")
@limiter.limit("10/minute")
async def generate_content(request: Request, content_request: ContentGenerationRequest):
    # Content generation logic
    pass
```

#### Input Validation & Sanitization
```python
from pydantic import validator, Field
import bleach

class ContentInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    
    @validator('text')
    def sanitize_text(cls, v):
        # Remove potentially harmful HTML/JavaScript
        return bleach.clean(v, tags=[], attributes={}, strip=True)
```

### Monitoring & Observability

#### Logging Configuration
```python
import structlog
from pythonjsonlogger import jsonlogger

# Structured logging setup
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

#### Health Checks
```python
@app.get("/health")
async def health_check():
    checks = {
        "database": await check_database_connection(),
        "redis": await check_redis_connection(),
        "openai": await check_openai_api(),
        "instagram": await check_instagram_api(),
        "linkedin": await check_linkedin_api()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

#### Performance Metrics
```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics collection
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
CONTENT_GENERATION_DURATION = Histogram('content_generation_duration_seconds', 'Content generation time')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(duration)
    
    return response
```

### Development & Deployment

#### Environment Configuration
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str
    database_pool_size: int = 20
    
    # Redis
    redis_url: str
    redis_session_db: int = 0
    redis_celery_db: int = 1
    
    # External APIs
    openai_api_key: str
    instagram_access_token: str
    linkedin_access_token: str
    news_api_key: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### Docker Configuration
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### CI/CD Pipeline
```yaml
# .github/workflows/backend.yml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

This comprehensive backend architecture provides a solid foundation for the Based Labs Automated Content Pipeline, ensuring scalability, maintainability, and robust error handling while maintaining the high-quality standards required for the brand.

This design provides a robust, scalable foundation for your automated content pipeline while maintaining the quality and brand consistency that Based Labs requires. The modular architecture allows for incremental development and easy maintenance as the system grows.