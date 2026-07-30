from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Livre(models.Model):
    titre = models.CharField(_("Titre"), max_length=255)
    auteur = models.CharField(_("Auteur"), max_length=255)
    isbn = models.CharField(_("ISBN"), max_length=13, unique=True)
    nombre_exemplaires = models.PositiveIntegerField(
        _("Nombre d'exemplaires"),
        default=1,
    )
    nombre_exemplaires_disponibles = models.PositiveIntegerField(
        _("Exemplaires disponibles"),
        default=1,
    )

    class Meta:
        verbose_name = _("Livre")
        verbose_name_plural = _("Livres")
        ordering = ["titre"]

    def __str__(self):
        return f"{self.titre} ({self.auteur})"


class Emprunt(models.Model):
    class Statut(models.TextChoices):
        EN_COURS = "en_cours", _("En cours")
        RETOURNE = "retourne", _("Retourné")
        EN_RETARD = "en_retard", _("En retard")

    livre = models.ForeignKey(
        Livre,
        verbose_name=_("Livre"),
        on_delete=models.CASCADE,
        related_name="emprunts",
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Utilisateur"),
        on_delete=models.CASCADE,
        related_name="emprunts",
    )
    date_emprunt = models.DateTimeField(_("Date d'emprunt"), auto_now_add=True)
    date_retour_prevue = models.DateField(_("Date de retour prévue"))
    date_retour_reelle = models.DateTimeField(
        _("Date de retour réelle"),
        null=True,
        blank=True,
    )
    statut = models.CharField(
        _("Statut"),
        max_length=20,
        choices=Statut.choices,
        default=Statut.EN_COURS,
    )

    class Meta:
        verbose_name = _("Emprunt")
        verbose_name_plural = _("Emprunts")
        ordering = ["-date_emprunt"]

    def __str__(self):
        return f"{self.utilisateur} — {self.livre} ({self.statut})"
