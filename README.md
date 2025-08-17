# Based Labs - Automated Content Pipeline

> Complete end-to-end system that transforms content curation into published social media posts with minimal human intervention, maintaining Based Labs brand voice and quality standards.

## Overview

The Based Labs Automated Content Pipeline is a comprehensive system that automates the entire workflow from trend monitoring and content generation to image creation, posting, and performance analytics. It combines AI-powered content generation with professional-grade image processing to create posts that look hand-designed while maintaining the Based Labs philosophy of challenging systems and empowering individual agency.

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Trend Monitor │    │  AI Content Gen │    │ Image Generator │
│   (News/Reddit) │───▶│   (OpenAI API)  │───▶│ (OpenCV/PIL)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Database      │    │   Review Queue  │    │  Social APIs    │
│  (Content/Perf) │◄──►│  (Human Check)  │───▶│ (Post/Analytics)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Technology Stack:**
- **Backend**: FastAPI with Python (async/await)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session management and job queues
- **Task Queue**: Celery for background processing
- **Frontend**: React dashboard for review and analytics
- **AI**: OpenAI GPT-4 with custom Based Labs prompts
- **Image Processing**: OpenCV, ImageMagick, Pillow with professional effects

## Features

### 🎯 **Automated Content Curation**
- **Trend monitoring** from news sources and Reddit discussions
- **Community input analysis** for content opportunities
- **Intelligent scoring** based on brand alignment, timeliness, and engagement potential
- **System friction identification** (permission barriers, gatekeeping, individual workarounds)

### 🤖 **AI-Powered Content Generation**
- **Brand voice consistency** with 7/10 provocative level calibration
- **Proven hook formulas**: "You're waiting for permission that will never come", "This rule made sense in 1950. It's destroying you in 2025"
- **Template selection** based on content length (quote_minimal <100 chars, long_form 100-800 chars, carousel_series >800 chars)
- **Quality validation** with automatic regeneration until standards are met
- **Platform-specific adaptation** for Instagram and LinkedIn

### 🎨 **Professional Image Generation**
- **Photoshop-level effects** using OpenCV, ImageMagick, and Skia
- **Dynamic text handling** that adapts font sizes and layouts automatically
- **Template-based consistency** ensuring brand alignment across all posts
- **Based Labs branding** with neon green (#00ff00) accents and black backgrounds
- **Multi-format support** for Instagram posts, carousels, and LinkedIn content

### 📱 **Multi-Platform Publishing**
- **Instagram integration** via Creator Studio API with visual-first optimization
- **LinkedIn integration** via LinkedIn API v2 with professional context framing
- **Optimal scheduling** (Instagram: 11 AM, 2 PM, 5 PM EST; LinkedIn: 8 AM, 12 PM, 6 PM EST)
- **Weekly content mix** (Monday: system critique, Wednesday: framework, Friday: community spotlight)
- **Automatic carousel creation** for content exceeding platform limits

### 👥 **Community Engagement Management**
- **Comment categorization** (questions, feedback, spam, engagement)
- **Response suggestions** based on Based Labs engagement templates
- **Content opportunity identification** from community discussions
- **Constructive criticism handling** guidance
- **Sentiment analysis** for community interactions

### 📊 **Performance Analytics & Learning**
- **Comprehensive metrics tracking** (engagement, saves, clicks, reach)
- **Performance thresholds** (2% engagement rate, 1% save rate monitoring)
- **Pattern identification** for high-performing content (hooks, topics, formats, timing)
- **Continuous improvement** through feedback loops into content generation
- **Actionable insights** and optimization recommendations

### 📅 **Content Calendar & Planning**
- **Strategic content planning** with campaign management
- **Content gap identification** and filling recommendations
- **Content pillar distribution** tracking and balancing
- **Special event integration** for timely content opportunities
- **Manual content requests** with specific topics or themes

## Quick Start

### Option 1: Full Pipeline (Recommended)
```bash
# Navigate to the main application
cd automated-content-pipeline

# Setup environment
cp .env.example .env
# Edit .env with your API keys (OpenAI, Instagram, LinkedIn, etc.)

# Start with Docker (easiest)
make docker-up

# Or run locally
make setup-dev
make dev  # API server
make frontend-dev  # Frontend dashboard (in another terminal)
```

### Option 2: Test Image Generation Only
```bash
# Test the image generation system
python setup_test.py
python test_integration.py

# View results in output/ directory:
# - post_quote_instagram.png (Quote format)
# - post_article_linkedin.png (Long-form content)  
# - post_hook_instagram.png (Hook/teaser format)
```

### Access Points
- **API Documentation**: http://localhost:8000/docs
- **Frontend Dashboard**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Trend Monitor │    │  AI Content Gen │    │ Image Generator │
│   (News/Reddit) │───▶│   (OpenAI API)  │───▶│ (OpenCV/PIL)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Database      │    │   Review Queue  │    │  Social APIs    │
│  (Content/Perf) │◄──►│  (Human Check)  │───▶│ (Post/Analytics)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Core Services

### 1. Trend Monitor Service (`app/services/trend_monitor.py`)
- **News API integration** for identifying content opportunities
- **Reddit monitoring** for community discussions and trends
- **Scoring algorithm** based on brand alignment (40%), timeliness (30%), engagement potential (20%), uniqueness (10%)
- **Community input processing** for converting discussions into content ideas

### 2. Content Generator Service (`app/services/content_generator.py`)
- **OpenAI GPT-4 integration** with Based Labs brand voice prompts
- **Hook formula implementation** with proven engagement patterns
- **Quality validation** with automatic regeneration cycles
- **Platform-specific adaptation** for Instagram and LinkedIn

### 3. Image Generator Service (`app/services/image_generator.py`)
- **Professional image generation** with Photoshop-level effects
- **Template system** (quote_minimal, long_form, carousel_series)
- **Dynamic text rendering** with optimal font sizing and wrapping
- **Brand consistency** with neon green accents and professional typography

### 4. Community Engagement Service
- **Comment categorization** and sentiment analysis
- **Response suggestion generation** using AI and templates
- **Content opportunity identification** from community interactions
- **Constructive feedback handling** guidance

### 5. Analytics Service
- **Performance metrics tracking** across all platforms
- **Pattern recognition** for high-performing content
- **Threshold monitoring** (2% engagement, 1% save rates)
- **Continuous learning** integration into content generation

### 6. Content Calendar Service
- **Strategic planning** with campaign management
- **Content pillar balancing** and gap identification
- **Optimal scheduling** with platform-specific timing
- **Special event integration** for timely opportunities

## Configuration

### Environment Setup
```bash
# Copy and configure environment variables
cp automated-content-pipeline/.env.example automated-content-pipeline/.env
```

**Required API Keys:**
- `OPENAI_API_KEY` - For AI content generation
- `INSTAGRAM_ACCESS_TOKEN` - For Instagram posting
- `LINKEDIN_ACCESS_TOKEN` - For LinkedIn posting  
- `NEWS_API_KEY` - For trend monitoring
- `REDDIT_CLIENT_ID` & `REDDIT_CLIENT_SECRET` - For Reddit monitoring

### Brand Voice Configuration
Steering files in `.kiro/steering/` control the entire system behavior:
- **`based-labs-voice.md`** - Core brand voice (7/10 provocative level, tone, themes)
- **`content-generation-rules.md`** - AI generation rules and quality filters
- **`directory-structure.md`** - Project organization and naming conventions

### Template System
Templates in `automated-content-pipeline/templates/`:
- **`quote_minimal`** - Short, punchy statements (<100 characters)
- **`long_form`** - Detailed explanations and frameworks (100-800 characters)
- **`carousel_series`** - Multi-slide content (>800 characters)
- **Custom templates** can be added by extending the BasedLabsImageGenerator

### Content Themes & Scheduling
- **Monday**: System critique content
- **Wednesday**: Framework and tool content  
- **Friday**: Community spotlight content
- **Instagram**: 11 AM, 2 PM, 5 PM EST
- **LinkedIn**: 8 AM, 12 PM, 6 PM EST

## Advanced Features

### Professional Image Processing
```python
# Color grading like Photoshop
lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
l, a, b = cv2.split(lab)
l = cv2.equalizeHist(l)  # Enhance contrast

# Professional effects with ImageMagick
with WandImage.from_array(img_array) as wand_img:
    wand_img.unsharp_mask(radius=0.5, sigma=0.5, amount=1.2)
    wand_img.enhance()
```

### Dynamic Text Handling
```python
# Automatically fit text to area
font = self._get_optimal_font(text, area)
lines = self._wrap_text(text, area.max_width, font)

# Smart positioning and alignment
x_pos = self._get_x_position(line, area, font)
draw.text((x_pos, y_pos), line, fill=area.color, font=font)
```

## API Endpoints

### Content Generation
```bash
# Generate content from trend
POST /api/v1/content/generate
{
  "trend_opportunity_id": "uuid",
  "content_type": "quote_minimal",
  "platform": "instagram"
}

# Generate image for content
POST /api/v1/content/generate-image/{content_id}

# Approve/reject content
PUT /api/v1/content/{content_id}/approve
PUT /api/v1/content/{content_id}/reject
```

### Trend Monitoring
```bash
# Get current trends
GET /api/v1/trends?limit=10

# Trigger manual trend monitoring
POST /api/v1/trends/monitor
```

### Analytics
```bash
# Get dashboard data
GET /api/v1/analytics/dashboard?timeframe=7d

# Get content performance
GET /api/v1/analytics/performance/{content_id}
```

### Database Schema
The system uses PostgreSQL with the following key tables:
- **`trend_opportunities`** - Identified content opportunities
- **`generated_content`** - AI-generated content pieces
- **`content_packages`** - Grouped content for campaigns
- **`post_metrics`** - Performance tracking data
- **`comments`** - Community engagement data
- **`content_calendar`** - Scheduling and planning data

## Development

### Common Commands
```bash
cd automated-content-pipeline

# Development
make setup-dev          # Setup development environment
make dev                # Start API server
make frontend-dev       # Start React dashboard
make worker             # Start Celery worker
make scheduler          # Start Celery beat scheduler

# Docker
make docker-up          # Start all services
make docker-down        # Stop all services
make docker-logs        # View logs

# Database
make migrate            # Run migrations
make create-migration MESSAGE="description"

# Testing
make test               # Run tests
make lint               # Code linting
make type-check         # Type checking
```

### Adding New Features
1. **Check requirements** in `.kiro/specs/automated-content-pipeline/requirements.md`
2. **Follow cursor rules** defined in `cursorrules` file
3. **Implement service layer** with proper business logic
4. **Add database models** with migrations
5. **Create API endpoints** with proper schemas
6. **Add comprehensive tests**
7. **Update documentation**

### Brand Voice Compliance
All content must maintain:
- **7/10 provocative level** (never below 6/10 or above 8/10)
- **Based Labs themes**: agency over permission, system inefficiencies, gatekeeping, individual empowerment
- **Proven hook formulas** for engagement
- **Clear value proposition** and specific next actions
- **Connection to Based Labs philosophy**

## Performance & Quality

### System Performance
- **Image generation**: 0.1-0.5 seconds per image
- **Content generation**: 1-3 seconds per piece
- **Batch processing**: 10+ posts per minute
- **API response time**: <200ms for most endpoints

### Quality Assurance
- **Automated testing**: 80%+ code coverage required
- **Brand consistency**: Enforced through steering files and validation
- **Performance monitoring**: 2% engagement rate, 1% save rate thresholds
- **Continuous learning**: Performance data feeds back into generation algorithms

### Scaling Considerations
- **Horizontal scaling**: Stateless services with load balancing
- **Database optimization**: Connection pooling and query optimization
- **Caching strategy**: Redis for frequently accessed data
- **Background processing**: Celery for long-running tasks
- **CDN integration**: For image delivery and static assets

## Dependencies

### Core Stack
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Primary database with SQLAlchemy ORM
- **Redis**: Caching and task queue backend
- **Celery**: Background task processing
- **React**: Frontend dashboard framework

### AI & Content
- **OpenAI GPT-4**: Content generation
- **NLTK/TextBlob**: Natural language processing
- **Custom steering**: Based Labs brand voice enforcement

### Image Processing
- **Pillow (PIL)**: Core image manipulation
- **OpenCV**: Advanced image processing and effects
- **Wand**: ImageMagick bindings for professional effects
- **NumPy**: Numerical operations for image arrays

### Social Media APIs
- **Instagram Creator Studio API**: Automated posting
- **LinkedIn API v2**: Professional content publishing
- **News API**: Trend monitoring
- **Reddit API**: Community discussion analysis

## Documentation

- **Requirements**: `.kiro/specs/automated-content-pipeline/requirements.md`
- **System Design**: `.kiro/specs/automated-content-pipeline/design.md`
- **Implementation Tasks**: `.kiro/specs/automated-content-pipeline/tasks.md`
- **Brand Voice Guidelines**: `.kiro/steering/based-labs-voice.md`
- **Content Generation Rules**: `.kiro/steering/content-generation-rules.md`
- **Development Rules**: `cursorrules`
- **API Documentation**: http://localhost:8000/docs (when running)

## Support

For development questions or issues:
1. Check the `cursorrules` file for development standards
2. Review the spec documents in `.kiro/specs/`
3. Follow the brand voice guidelines in `.kiro/steering/`
4. Ensure all tests pass before submitting changes
5. Maintain the 7/10 provocative level in all content

The system embodies the Based Labs philosophy: challenge systems, empower individuals, and build the future without waiting for permission.