from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.domain.erreurs import CreneauInvalide

DUREE_MAX = timedelta(hours=24)


def en_utc_naif(moment: datetime) -> datetime:
    """Convertit en UTC sans fuseau ; une date sans fuseau est considérée UTC."""
    if moment.tzinfo is None:
        return moment
    try:
        return moment.astimezone(timezone.utc).replace(tzinfo=None)
    except OverflowError:
        raise CreneauInvalide("Date hors limites.") from None


def maintenant_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


@dataclass(frozen=True)
class Creneau:
    debut: datetime
    fin: datetime

    def __post_init__(self) -> None:
        object.__setattr__(self, "debut", en_utc_naif(self.debut))
        object.__setattr__(self, "fin", en_utc_naif(self.fin))
        if self.debut >= self.fin:
            raise CreneauInvalide("Le début du créneau doit précéder sa fin.")
        if self.duree > DUREE_MAX:
            raise CreneauInvalide("Un créneau ne peut pas dépasser 24 heures.")

    @property
    def duree(self) -> timedelta:
        return self.fin - self.debut

    def chevauche(self, autre: "Creneau") -> bool:
        return self.debut < autre.fin and autre.debut < self.fin
