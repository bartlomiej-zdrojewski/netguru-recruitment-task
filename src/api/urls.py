from django.urls import path
from .views import Cars, CarsUpdate, Rate, Popular

urlpatterns = [
    path('cars/', Cars.as_view(), name='cars'),
    path('cars/<int:car_id>/', CarsUpdate.as_view(), name='cars_update'),
    path('rate/', Rate.as_view(), name='rate'),
    path('popular/', Popular.as_view(), name='popular')
]
