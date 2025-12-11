from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    categoria = Column(String, nullable=False) # Ej: Vacuna, Medicamento, Accesorio
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<Producto {self.nombre} (Stock: {self.stock})>"