from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "name", "password", "role"]
        read_only_fields = ["id"]

    def validate_role(self, role):
        request = self.context.get("request")
        utilisateur_courant = getattr(request, "user", None)
        if role == User.Role.BIBLIOTHECAIRE and not (
            utilisateur_courant
            and utilisateur_courant.is_authenticated
            and utilisateur_courant.est_bibliothecaire
        ):
            msg = "Seul un bibliothécaire peut créer un compte bibliothécaire."
            raise serializers.ValidationError(msg)
        return role

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }
