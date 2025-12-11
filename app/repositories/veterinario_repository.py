from sqlalchemy.orm import Session
from app.models.veterinario import Veterinario

class VeterinarioRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, veterinario: Veterinario):
        self.db.add(veterinario)
        self.db.commit()
        self.db.refresh(veterinario)
        return veterinario

    def buscar_por_colegiado(self, num_colegiado: str):
        # Buscamos el usuario exacto por su ID de empleado (num_colegiado)
        return self.db.query(Veterinario).filter(Veterinario.num_colegiado == num_colegiado).first()
    
    def buscar_todos(self):
        return self.db.query(Veterinario).all()
        
    def buscar_por_id(self, id: int):
        return self.db.query(Veterinario).filter(Veterinario.id == id).first()