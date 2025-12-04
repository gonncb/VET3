from sqlalchemy.orm import Session, joinedload
from app.models.cita import Cita

class CitaRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, cita: Cita):
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def buscar_todas(self):
        # Carga mascota y veterinario a la vez para evitar errores en la tabla
        return self.db.query(Cita).options(
            joinedload(Cita.mascota),
            joinedload(Cita.veterinario)
        ).all()