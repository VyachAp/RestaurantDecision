from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView

from restdecision.models.restaurant import Restaurant
from restdecision.serializers.restaurant import RestaurantSerializer


class RestaurantView(CreateAPIView, ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
