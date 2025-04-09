from rest_framework import serializers
from .models import Hotel, Reservation, ReservationGuest

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'price', 'availability']

class ReservationGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationGuest
        fields = ['guest_name', 'gender']

class ReservationSerializer(serializers.ModelSerializer):
    guests = ReservationGuestSerializer(many=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)

    class Meta:
        model = Reservation
        fields = ['hotel', 'hotel_name', 'checkin', 'checkout', 'confirmation_number', 'guests']
        read_only_fields = ['confirmation_number']

    def create(self, validated_data):
        guests_data = validated_data.pop('guests')
        reservation = Reservation.objects.create(**validated_data)

        import uuid
        reservation.confirmation_number = uuid.uuid4().hex[:8].upper()
        reservation.save()

        
        for guest_data in guests_data:
            ReservationGuest.objects.create(reservation=reservation, **guest_data)

        return reservation