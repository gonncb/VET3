from sqlalchemy.orm import Session, joinedload
from app.models.cliente import Cliente

class ClienteRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, cliente: Cliente):
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def buscar_por_dni(self, dni: str):
        # El joinedload evita el error al cerrar sesión
        return self.db.query(Cliente).options(joinedload(Cliente.mascotas)).filter(Cliente.dni == dni).first()
    
    def buscar_todos(self):
        return self.db.query(Cliente).options(joinedload(Cliente.mascotas)).all()