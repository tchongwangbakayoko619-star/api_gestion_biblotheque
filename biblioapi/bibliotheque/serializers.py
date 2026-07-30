from django.utils import timezone
from rest_framework import serializers

from biblioapi.bibliotheque.models import Emprunt
from biblioapi.bibliotheque.models import Livre


class LivreSerializer(serializers.ModelSerializer):
    disponible = serializers.SerializerMethodField()

    class Meta:
        model = Livre
        fields = [
            "id",
            "titre",
            "auteur",
            "isbn",
            "nombre_exemplaires",
            "nombre_exemplaires_disponibles",
            "disponible",
        ]
        read_only_fields = ["nombre_exemplaires_disponibles"]

    def get_disponible(self, obj) -> bool:
        return obj.nombre_exemplaires_disponibles > 0

    def create(self, validated_data):
        # À la création, le stock disponible démarre égal au stock total
        validated_data["nombre_exemplaires_disponibles"] = validated_data[
            "nombre_exemplaires"
        ]
        return super().create(validated_data)


class EmpruntSerializer(serializers.ModelSerializer):
    livre = LivreSerializer(read_only=True)
    livre_id = serializers.PrimaryKeyRelatedField(
        queryset=Livre.objects.all(),
        source="livre",
        write_only=True,
    )
    utilisateur = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Emprunt
        fields = [
            "id",
            "livre",
            "livre_id",
            "utilisateur",
            "date_emprunt",
            "date_retour_prevue",
            "date_retour_reelle",
            "statut",
        ]
        read_only_fields = [
            "utilisateur",
            "date_emprunt",
            "date_retour_reelle",
            "statut",
        ]

    def validate_livre_id(self, livre):
        if livre.nombre_exemplaires_disponibles < 1:
            msg = "Ce livre n'a plus d'exemplaires disponibles."
            raise serializers.ValidationError(msg)
        return livre

    def validate_date_retour_prevue(self, value):
        if value <= timezone.now().date():
            msg = "La date de retour prévue doit être dans le futur."
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data):
        livre = validated_data["livre"]
        livre.nombre_exemplaires_disponibles -= 1
        livre.save(update_fields=["nombre_exemplaires_disponibles"])
        validated_data["utilisateur"] = self.context["request"].user
        return super().create(validated_data)
