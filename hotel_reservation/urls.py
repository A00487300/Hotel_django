from django.contrib import admin
from django.urls import path
from api.views import HotelListView, ReservationConfirmationView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 你的API路径
    path('api/hotels/', HotelListView.as_view(), name='hotels'),
    path('api/reservationConfirmation/', ReservationConfirmationView.as_view(), name='reservation_confirmation'),
]