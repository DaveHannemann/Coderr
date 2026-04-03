from django.urls import path
from .views import OfferDetailView, OfferListCreateView, OfferRetrieveUpdateDestroyView

urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer-list'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offerdetail-detail'),
]
