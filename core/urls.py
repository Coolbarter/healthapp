from django.urls import path
from .views import HomeView, AnalysisSliderView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('analysis-slider/', AnalysisSliderView.as_view(), name='analysis_slider'),
] 