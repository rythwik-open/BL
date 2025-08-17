---
inclusion: always
---

# Content Generation Rules for Based Labs Automation

## AI Content Generation Guidelines

### Content Analysis Framework
When analyzing trends or news for content opportunities, focus on:

1. **System Friction Points**: Where do outdated rules slow people down?
2. **Permission Barriers**: What do people think they need approval for?
3. **Gatekeeping Mechanisms**: Who controls access to tools/opportunities?
4. **Individual Workarounds**: How are people bypassing traditional systems?

### Content Type Selection Rules

#### Quote Posts (quote_minimal template)
**Use when**:
- Text under 100 characters
- Single powerful insight
- Provocative statement that stops the scroll
- Hook for longer content series

**Structure**: Hook → Attribution/CTA

#### Long Form Posts (long_form template)  
**Use when**:
- Text 100-800 characters
- Explaining a framework or concept
- Breaking down a system problem
- Providing actionable steps

**Structure**: Title → Explanation → Call-to-Action

#### Carousel Series
**Use when**:
- Content exceeds 800 characters
- Complex topic needs breakdown
- Step-by-step process
- Multiple related points

**Structure**: Title slide → 3-5 content slides → CTA slide

### Template Selection Logic

```python
def select_template(content_analysis):
    char_count = len(content_analysis['main_text'])
    content_type = content_analysis['type']
    
    if char_count < 100 or content_type in ['hook', 'quote']:
        return 'quote_minimal'
    elif char_count < 800 and content_type in ['explanation', 'framework']:
        return 'long_form'
    else:
        return 'carousel_series'
```

## Content Quality Filters

### Must Include
- Clear value proposition for the reader
- Specific next action or question
- Connection to Based Labs philosophy
- Provocative but not inflammatory angle

### Must Avoid
- Generic motivational content
- Direct attacks on individuals/companies
- Unsubstantiated claims
- Content that doesn't empower action

### Provocative Level Calibration (7/10)
- ✅ "The education system trains you to wait for permission"
- ✅ "Your boss profits from your hesitation to start"
- ❌ "Universities are scams" (too direct, 9/10)
- ❌ "Maybe consider alternative learning" (too soft, 3/10)

## Platform-Specific Adaptations

### Instagram Content
- **Visual-first**: Text must work with strong visual design
- **Scroll-stopping**: First line must grab attention immediately
- **Hashtag strategy**: #agency #systems #decentralized #futureofwork
- **Story integration**: Use polls and questions for engagement

### LinkedIn Content
- **Professional context**: Frame in business/career terms
- **Thought leadership**: Position as industry insight
- **Network effects**: Encourage sharing and discussion
- **Article format**: Longer explanations with clear structure

## Trend Analysis Prompts

### For News/Trend Input
```
Analyze this news item for Based Labs content opportunities:
[NEWS ITEM]

Focus on:
1. What system or rule is causing friction?
2. Who benefits from the current system?
3. How could individuals work around this?
4. What would a decentralized alternative look like?

Generate 3 content angles that would resonate with people frustrated by slow institutions.
Format as: Hook → Explanation → Call-to-Action
```

### For Community Input Analysis
```
Analyze these community comments/questions for content ideas:
[COMMUNITY INPUT]

Identify:
1. Common frustrations with existing systems
2. Permission-seeking behaviors
3. Successful workarounds or alternatives
4. Questions about tools or processes

Generate content that addresses the underlying system issue, not just the surface problem.
```

## Content Scheduling Strategy

### Weekly Content Mix
- **Monday**: System critique (wake people up for the week)
- **Wednesday**: Framework or tool (practical value)
- **Friday**: Community spotlight or success story (inspiration)

### Posting Times (to be optimized based on performance)
- **Instagram**: 11 AM, 2 PM, 5 PM EST
- **LinkedIn**: 8 AM, 12 PM, 6 PM EST

## Performance Learning Rules

### Track These Metrics
- Engagement rate (likes, comments, shares)
- Save rate (indicates value)
- Comment quality (depth of discussion)
- Click-through to newsletter/website
- Time of posting vs performance

### Content Iteration Rules
- If engagement < 2%: Increase provocative level or improve hook
- If saves < 1%: Add more practical value
- If comments are shallow: Ask better questions
- If no clicks: Strengthen call-to-action

## Integration with Image Generation

### Text-to-Visual Mapping
- **Quote content**: Center-aligned, large font, minimal background
- **Framework content**: Left-aligned, structured layout, bullet points
- **Hook content**: Bold typography, high contrast, attention-grabbing

### Brand Consistency in Visuals
- Always include Based Labs branding
- Maintain neon green (#00ff00) accent color
- Use black/dark backgrounds for contrast
- Ensure text readability across all devices

## Feedback Loop Integration

### Human Review Process
1. AI generates content + selects template
2. Human reviews for brand alignment
3. Feedback captured for AI learning
4. Performance data feeds back to content generation

### Continuous Improvement
- Weekly analysis of top/bottom performing content
- Monthly review of brand voice consistency
- Quarterly update of content themes based on community growth
- Ongoing refinement of provocative level calibration