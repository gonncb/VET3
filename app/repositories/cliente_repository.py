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
        return self.db.query(Cliente).options(joinedload(Cliente.mascotas)).filter(Cliente.dni == dni).first()
    
    def buscar_todos(self):
        return self.db.query(Cliente).options(joinedload(Cliente.mascotas)).all()

    def buscar_por_id(self, id: int):
        return self.db.query(Cliente).filter(Cliente.id == id).first()

    def eliminar(self, cliente: Cliente):
        self.db.delete(cliente)
        self.db.commit()

    def actualizar(self):
        # En SQLAlchemy, si modificas el objeto y haces commit, se actualiza solo.
        self.db.commit()