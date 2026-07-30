from rest_framework import permissions


class EstBibliothecaireOuLectureSeule(permissions.BasePermission):
    """Seuls les bibliothécaires peuvent créer/modifier/supprimer des livres."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.est_bibliothecaire)


class EstProprietaireEmpruntOuBibliothecaire(permissions.BasePermission):
    """Un lecteur ne peut voir/modifier que ses propres emprunts.
    Un bibliothécaire a accès à tous les emprunts."""

    def has_permission(self, request, view):
        # Un lecteur peut créer un emprunt (pour lui-même, géré dans le serializer)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.est_bibliothecaire:
            return True
        return obj.utilisateur == request.user
