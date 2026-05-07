from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_secure, name='upload_and_secure'),
    path('audit/<int:doc_id>/', views.audit_document, name='audit_document'),
]