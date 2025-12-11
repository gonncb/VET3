from sqlalchemy.orm import Session, joinedload
from app.models.cita import Cita
from app.models.mascota import Mascota # <--- Importante importar Mascota para el join

class CitaRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, cita: Cita):
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def buscar_todas(self):
        # AQUI ESTA LA MAGIA:
        # 1. Cargamos el Veterinario
        # 2. Cargamos la Mascota Y ADEMÁS (joinedload anidado) cargamos el Cliente de esa mascota
        return self.db.query(Cita).options(
            joinedload(Cita.veterinario),
            joinedload(Cita.mascota).joinedload(Mascota.cliente) 
        ).all()
        
    def eliminar_por_id(self, id_cita: int):
        cita = self.db.query(Cita).filter(Cita.id == id_cita).first()
        if cita:
            self.db.delete(cita)
            self.db.commit()
            return True
        return False