from sqlalchemy.orm import Session, joinedload
from app.models.historial import HistorialMedico

class HistorialRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, historial: HistorialMedico):
        self.db.add(historial)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def buscar_por_mascota(self, id_mascota: int):
        """Devuelve todo el historial de una mascota ordenado por fecha descendente"""
        return self.db.query(HistorialMedico)\
            .options(joinedload(HistorialMedico.veterinario))\
            .filter(HistorialMedico.id_mascota == id_mascota)\
            .order_by(HistorialMedico.fecha.desc())\
            .all()