from django.db import models


class Hotel(models.Model):
    """
    用于存储酒店信息
    """
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    """
    预订主表，存储主要信息，比如酒店、入住/退房日期
    """
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    checkin = models.DateField()
    checkout = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Reservation: {self.confirmation_number}"

class ReservationGuest(models.Model):
    """
    存储客人信息，与 Reservation 多对一关系
    """
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests')
    guest_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
