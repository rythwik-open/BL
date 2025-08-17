"""
Integration test showing how image generator fits into the larger system
This demonstrates the API structure that will be used in the full backend
"""

import json
from typing import Dict, List
from image_generator import BasedLabsImageGenerator
from dataclasses import dataclass, asdict

@dataclass
class ContentRequest:
    """Structure for content generation requests"""
    text: str
    content_type: str  # quote, article, list, hook
    platform: str  # instagram, linkedin
    template_preference: str = None
    brand_voice_level: int = 7  # 1-10 provocative level

@dataclass
class GeneratedContent:
    """Structure for AI-generated content"""
    main_text: str = ""
    attribution: str = None
    title: str = None
    body: str = None
    cta: str = None
    content_type: str = "quote"
    template_suggestion: str = None

class ContentProcessor:
    """
    This class simulates how the image generator integrates 
    with AI content generation and the broader system
    """
    
    def __init__(self):
        self.image_generator = BasedLabsImageGenerator()
    
    def process_content_request(self, request: ContentRequest) -> Dict:
        """
        Full pipeline: Request -> AI Content -> Image Generation
        This is how it will work in the real system
        """
        
        # Step 1: Generate content with AI (simulated for now)
        ai_content = self.simulate_ai_content_generation(request)
        
        # Step 2: Generate image
        image = self.image_generator.generate_post(
            content=asdict(ai_content),
            template_name=ai_content.template_suggestion
        )
        
        # Step 3: Return complete package
        return {
            "content": asdict(ai_content),
            "image": image,
            "metadata": {
                "request_id": "test_123",
                "platform": request.platform,
                "template_used": ai_content.template_suggestion or "auto_selected",
                "processing_time": "0.5s"  # Would be real timing
            }
        }
    
    def simulate_ai_content_generation(self, request: ContentRequest) -> GeneratedContent:
        """
        Simulate AI content generation
        In the real system, this would call OpenAI API with brand voice prompts
        """
        
        # Sample content based on Based Labs brand voice with proper structure
        sample_content = {
            "quote": GeneratedContent(
                title="You don't need permission to start building the future",
                description="Most people wait for approval that will never come. The system profits from your hesitation.",
                attribution="- Based Labs",
                content_type="quote",
                template_suggestion="quote_post"
            ),
            "article": GeneratedContent(
                title="$100,000 FOR A NEWLY MINED BITCOIN",
                description="Bitcoin has reached an unprecedented value of $100,000 per coin, marking a historic moment in the digital currency's volatile journey, showcasing its resilience and growing acceptance in financial markets worldwide.",
                cta="READ MORE →",
                content_type="news",
                template_suggestion="news_post"
            ),
            "hook": GeneratedContent(
                title="The real cost of playing by the old rules",
                description="While you wait for permission, others are building the future without asking.",
                attribution="What are you waiting for?",
                content_type="insight",
                template_suggestion="quote_post"
            )
        }
        
        return sample_content.get(request.content_type, sample_content["quote"])

# API-style functions that will integrate into FastAPI backend
class ImageGenerationAPI:
    """API endpoints for the image generation system"""
    
    def __init__(self):
        self.processor = ContentProcessor()
    
    async def generate_post(self, request_data: Dict) -> Dict:
        """
        POST /api/generate-post
        Main endpoint for generating social media posts
        """
        try:
            request = ContentRequest(**request_data)
            result = self.processor.process_content_request(request)
            
            # Save image to output directory
            output_path = f"output/post_{request.content_type}_{request.platform}.png"
            result["image"].save(output_path)
            
            return {
                "success": True,
                "image_path": output_path,
                "content": result["content"],
                "metadata": result["metadata"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def get_templates(self) -> Dict:
        """
        GET /api/templates
        Return available templates
        """
        return {
            "templates": list(self.processor.image_generator.templates.keys()),
            "template_details": {
                name: {
                    "suitable_for": template.suitable_for,
                    "text_areas": list(template.text_areas.keys())
                }
                for name, template in self.processor.image_generator.templates.items()
            }
        }

def run_integration_tests():
    """Run comprehensive tests showing system integration"""
    
    api = ImageGenerationAPI()
    
    # Test different content types
    test_requests = [
        {
            "text": "Agency over permission",
            "content_type": "quote",
            "platform": "instagram"
        },
        {
            "text": "Why traditional education fails entrepreneurs",
            "content_type": "article", 
            "platform": "linkedin"
        },
        {
            "text": "The permission trap",
            "content_type": "hook",
            "platform": "instagram"
        }
    ]
    
    results = []
    
    print("Running integration tests...\n")
    
    for i, request_data in enumerate(test_requests, 1):
        print(f"Test {i}: {request_data['content_type']} for {request_data['platform']}")
        
        # This would be async in the real system
        import asyncio
        result = asyncio.run(api.generate_post(request_data))
        
        if result["success"]:
            print(f"✅ Generated: {result['image_path']}")
            print(f"   Content: {result['content']['main_text'][:50]}...")
            print(f"   Template: {result['metadata']['template_used']}")
        else:
            print(f"❌ Failed: {result['error']}")
        
        results.append(result)
        print()
    
    # Test template endpoint
    print("Testing template endpoint...")
    templates = asyncio.run(api.get_templates())
    print(f"✅ Available templates: {templates['templates']}")
    
    return results

if __name__ == "__main__":
    # First setup the test environment
    print("Setting up test environment...")
    from setup_test import create_test_environment
    create_test_environment()
    
    print("\n" + "="*50)
    print("INTEGRATION TESTS")
    print("="*50)
    
    # Run integration tests
    results = run_integration_tests()
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    
    successful = sum(1 for r in results if r["success"])
    print(f"Tests passed: {successful}/{len(results)}")
    
    if successful == len(results):
        print("🎉 All tests passed! System ready for backend integration.")
    else:
        print("⚠️  Some tests failed. Check error messages above.")
    
    print("\nNext steps:")
    print("1. Install fonts (see fonts/README.txt)")
    print("2. Install optional dependencies: pip install Wand skia-python")
    print("3. Integrate into FastAPI backend")
    print("4. Add AI content generation")
    print("5. Connect to social media APIs")