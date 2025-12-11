from sqlalchemy.orm import Session
from app.models.producto import Producto

class ProductoRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def guardar(self, producto: Producto):
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def buscar_todos(self):
        return self.db.query(Producto).all()

    def buscar_por_id(self, id: int):
        return self.db.query(Producto).filter(Producto.id == id).first()

    def eliminar(self, producto: Producto):
        self.db.delete(producto)
        self.db.commit()

    def actualizar_stock(self):
        # SQLAlchemy detecta los cambios en los objetos cargados y hace update al commit
        self.db.commit()