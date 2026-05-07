from django.urls import path
from . import views

urlpatterns = [
    # endpoint for fase 1-4
    path('upload/', views.upload_and_secure, name='upload_and_secure'),

    # endpoint for fase 5 
    path('audit/<int:doc_id>/', views.audit_document, name='audit_document'),
]