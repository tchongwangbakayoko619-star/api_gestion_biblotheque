from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from biblioapi.bibliotheque.views import EmpruntViewSet
from biblioapi.bibliotheque.views import LivreViewSet
from biblioapi.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("livres", LivreViewSet)
router.register("emprunts", EmpruntViewSet, basename="emprunt")
router.register("users", UserViewSet)

app_name = "api"
urlpatterns = router.urls
