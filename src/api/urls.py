from django.urls import path
from .views import Cars, CarsSingle, Rate, Popular

urlpatterns = [
    path('cars/', Cars.as_view(), name='cars'),
    path('cars/<int:car_id>/', CarsSingle.as_view(), name='cars_single'),
    path('rate/', Rate.as_view(), name='rate'),
    path('popular/', Popular.as_view(), name='popular')
]
