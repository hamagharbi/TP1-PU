from dataclasses import dataclass
from datetime import datetime, timedelta

from app.domain.erreurs import CreneauInvalide


@dataclass(frozen=True)
class Creneau:
    debut: datetime
    fin: datetime

    def __post_init__(self) -> None:
        if self.debut >= self.fin:
            raise CreneauInvalide("Le début du créneau doit précéder sa fin.")

    @property
    def duree(self) -> timedelta:
        return self.fin - self.debut

    def chevauche(self, autre: "Creneau") -> bool:
        return self.debut < autre.fin and autre.debut < self.fin
