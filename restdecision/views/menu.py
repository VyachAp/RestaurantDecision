from django.db.models import Sum

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from datetime import datetime
from restdecision.models.menu import Menu
from restdecision.serializers.menu import (
    MenuSerializer,
    ListMenuVotesSerializer,
    FirstMenuVoteSerializer,
    SecondMenuVoteSerializer,
    CreateMenuSerializer,
)


class MenuView(RetrieveAPIView):
    serializer_class = MenuSerializer

    def get_object(self):
        return Menu.objects.filter(
            restaurant_id=self.kwargs.get("restaurant_id"), dt_load=datetime.today()
        ).first()


class MenuVotesView(ListAPIView):
    serializer_class = ListMenuVotesSerializer

    def get_queryset(self):
        return (
            Menu.objects.filter(dt_load=datetime.today())
            .select_related("restaurant")
            .annotate(count=Sum("votes__points"))
        )


class VoteView(CreateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.META.get("BUILD_VERSION") == "2":
            return SecondMenuVoteSerializer
        return FirstMenuVoteSerializer

    def post(self, request, *args, **kwargs):
        context = {"request": request}
        params = {"context": context}
        if self.request.META.get("BUILD_VERSION") == "2":
            params["many"] = True
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, **params)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": "True",
                    "message": "Voted successfully",
                    "data": serializer.data,
                },
                status=200,
            )
        return Response(serializer.errors, status=400)


class UploadMenuView(CreateAPIView):
    serializer_class = CreateMenuSerializer
