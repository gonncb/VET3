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
        return self.db.query(Cita).options(
            joinedload(Cita.mascota),
            joinedload(Cita.veterinario)
        ).all()
        
    # --- NUEVO MÉTODO ---
    def eliminar_por_id(self, id_cita: int):
        cita = self.db.query(Cita).filter(Cita.id == id_cita).first()
        if cita:
            self.db.delete(cita)
            self.db.commit()
            return True
        return False