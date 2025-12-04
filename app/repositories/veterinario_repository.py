from sqlalchemy.orm import Session
from app.models.veterinario import Veterinario

class VeterinarioRepository:
    def __init__(self, db_session: Session):
        # Inyección de dependencia: El repositorio recibe la sesión de DB
        self.db = db_session

    def guardar(self, veterinario: Veterinario):
        self.db.add(veterinario)
        self.db.commit()
        self.db.refresh(veterinario) # Actualiza el ID generado por la DB
        return veterinario

    def buscar_por_id(self, vet_id: int):
        return self.db.query(Veterinario).filter(Veterinario.id == vet_id).first()

    def buscar_por_colegiado(self, num_colegiado: str):
        return self.db.query(Veterinario).filter(Veterinario.num_colegiado == num_colegiado).first()
    
    def buscar_todos(self):
        return self.db.query(Veterinario).all()