from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from biblioapi.bibliotheque.models import Emprunt
from biblioapi.bibliotheque.models import Livre
from biblioapi.bibliotheque.permissions import EstBibliothecaireOuLectureSeule
from biblioapi.bibliotheque.permissions import EstProprietaireEmpruntOuBibliothecaire
from biblioapi.bibliotheque.serializers import EmpruntSerializer
from biblioapi.bibliotheque.serializers import LivreSerializer


class LivreViewSet(viewsets.ModelViewSet):
    queryset = Livre.objects.all()
    serializer_class = LivreSerializer
    permission_classes = [IsAuthenticated, EstBibliothecaireOuLectureSeule]
    filterset_fields = ["auteur"]
    search_fields = ["titre", "auteur", "isbn"]


class EmpruntViewSet(viewsets.ModelViewSet):
    queryset = Emprunt.objects.all()
    serializer_class = EmpruntSerializer
    permission_classes = [IsAuthenticated, EstProprietaireEmpruntOuBibliothecaire]

    def get_queryset(self):
        user = self.request.user
        if user.est_bibliothecaire:
            return Emprunt.objects.all()
        return Emprunt.objects.filter(utilisateur=user)

    @action(detail=True, methods=["post"])
    def retourner(self, request, pk=None):
        emprunt = self.get_object()
        if emprunt.statut == Emprunt.Statut.RETOURNE:
            return Response(
                {"detail": "Cet emprunt a déjà été retourné."},
                status=400,
            )
        emprunt.statut = Emprunt.Statut.RETOURNE
        emprunt.date_retour_reelle = timezone.now()
        emprunt.save(update_fields=["statut", "date_retour_reelle"])

        livre = emprunt.livre
        livre.nombre_exemplaires_disponibles += 1
        livre.save(update_fields=["nombre_exemplaires_disponibles"])

        serializer = self.get_serializer(emprunt)
        return Response(serializer.data)
