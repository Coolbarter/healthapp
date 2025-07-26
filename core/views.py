from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib import messages
from PIL import Image
import pytesseract
from io import BytesIO
import os
import re
from dotenv import load_dotenv
from .forms import ImageUploadForm
from .services.claude_client import MedicalAnalyzer

# Load environment variables
load_dotenv()

class HomeView(FormView):
    template_name = 'core/home.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('home')

    def sanitize_filename(self, filename):
        filename = filename.replace(' ', '_')
        filename = re.sub(r'[^A-Za-z0-9._-]', '', filename)
        return filename

    def form_valid(self, form):
        image = form.cleaned_data['image']
        ocr_text = None
        error = None
        image_preview = None
        analysis = None
        
        try:
            # Read image and perform OCR
            img = Image.open(image)
            ocr_text = pytesseract.image_to_string(img)
            
            if ocr_text.strip():
                # Analyze text with Claude
                analyzer = MedicalAnalyzer()
                analysis, error = analyzer.analyze_medical_image(ocr_text)
            if not ocr_text.strip():
                error = 'No text detected in the image.'
        except Exception as e:
            error = f'Error processing image: {str(e)}'
            ocr_text = None
        # For preview, encode image to base64 (optional, still in-memory)
        try:
            image.seek(0)
            img = Image.open(image)
            buf = BytesIO()
            img.save(buf, format=img.format or 'PNG')
            import base64
            image_preview = base64.b64encode(buf.getvalue()).decode('utf-8')
            image_format = img.format.lower() if img.format else 'png'
        except Exception:
            image_preview = None
            image_format = 'png'
        context = self.get_context_data(
            form=form,
            ocr_text=ocr_text,
            analysis=analysis,
            error=error,
            image_preview=image_preview,
            image_format=image_format
        )
        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error='Please upload a valid image.'))
