from django.urls import path
from .views import ProberProfileListView, ProberProfileDetailView

urlpatterns = [
    path('prober-profiles/', ProberProfileListView.as_view(), name='prober-profile-list'),
    path('prober-profiles/<int:pk>/', ProberProfileDetailView.as_view(), name='prober-profile-detail'),
]