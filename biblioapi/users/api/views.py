from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import inline_serializer
from rest_framework import generics
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# biblioapi/users/api/views.py
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from biblioapi.users.api.serializers import InscriptionSerializer
from biblioapi.users.models import User

from .serializers import UserSerializer


class InscriptionAPIView(generics.CreateAPIView):
    serializer_class = InscriptionSerializer
    permission_classes = [AllowAny]  # tout le monde peut créer un compte lecteur


class MoiAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Profil de l'utilisateur connecté",
        responses=inline_serializer(
            name="MoiResponse",
            fields={
                "id": serializers.IntegerField(),
                "username": serializers.CharField(),
                "email": serializers.EmailField(),
                "role": serializers.CharField(),
            },
        ),
    )
    def get(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        )


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
