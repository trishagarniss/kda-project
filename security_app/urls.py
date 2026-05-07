from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_and_secure, name='upload_and_secure'),
    path('audit/<int:doc_id>/', views.audit_document, name='audit_document'),
    path('documents/', views.get_all_documents, name='get_all_documents'),
    path('audit-network/', views.audit_network_integrity, name='audit_network'),
    path('download/<int:doc_id>/', views.download_decrypted_file, name='download_decrypted_file'),
]