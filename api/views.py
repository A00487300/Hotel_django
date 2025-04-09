from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Hotel, Reservation, ReservationGuest
from .serializers import HotelSerializer, ReservationSerializer

class HotelListView(APIView):
    """
    GET /api/hotels?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD&guests=2
    返回可用酒店列表
    """
    def get(self, request, *args, **kwargs):
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')
        guests = request.query_params.get('guests')

        # 简单示例，只要 availability=True 都返回
        queryset = Hotel.objects.filter(availability=True)

        # 你也可以根据 checkin/checkout 做更复杂的排期过滤
        # 比如 queryset = queryset.exclude(...) # 过滤掉已经被订满的日期

        serializer = HotelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        price = request.data.get('price')

        if not name or not price:
            return Response({"error": "Missing 'name' or 'price'"}, status=status.HTTP_400_BAD_REQUEST)

        hotel = Hotel(name=name, price=price, availability=True)
        hotel.save()

        serializer = HotelSerializer(hotel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
class ReservationConfirmationView(APIView):
    """
    POST /api/reservationConfirmation
    接收:
    {
      "hotel_name": <string>,
      "checkin": <YYYY-MM-DD>,
      "checkout": <YYYY-MM-DD>,
      "guests_list": [
          {"guest_name":"Alice", "gender":"Female"},
          {"guest_name":"Bob", "gender":"Male"}
      ]
    }
    返回:
    {
      "confirmation_number": <string>
    }
    """
    
    def get(self, request, *args, **kwargs):
        # 如果仅想列出所有 Reservation，可直接这样写：
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        data = request.data
        hotel_name = data.get("hotel_name")
        checkin = data.get("checkin")
        checkout = data.get("checkout")
        guests_list = data.get("guests_list", [])

        if not hotel_name or not checkin or not checkout:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # 根据hotel_name查找Hotel
        try:
            hotel = Hotel.objects.get(name=hotel_name)
        except Hotel.DoesNotExist:
            return Response({"error": "Invalid hotel_name"}, status=status.HTTP_400_BAD_REQUEST)

        # 构造 ReservationSerializer 所需的数据结构
        payload = {
            "hotel": hotel.id,
            "checkin": checkin,
            "checkout": checkout,
            "guests": [  # 注意: ReservationSerializer里 guests=ReservationGuestSerializer(many=True)
                {
                    "guest_name": g.get("guest_name"),
                    "gender": g.get("gender")
                }
                for g in guests_list
            ]
        }

        serializer = ReservationSerializer(data=payload)
        if serializer.is_valid():
            reservation = serializer.save()  # create方法中会生成confirmation_number
            return Response({
                "confirmation_number": reservation.confirmation_number
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
