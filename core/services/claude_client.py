import os
import anthropic
from django.conf import settings

class MedicalAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def analyze_medical_image(self, text_content):
        """Analyze medical text using Claude."""
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                temperature=0.7,
                system="You are a helpful medical assistant. Analyze the medical report and respond with: 1) Summary of findings 2) Diet advice 3) Health warnings if any. Keep responses concise and clear.",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text_content}
                        ]
                    }
                ]
            )
            return response.content[0].text, None
        except Exception as e:
            return None, f"Error analyzing text: {str(e)}"
