from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    telefono = Column(String)

    # Relación: Un cliente tiene muchas mascotas
    # 'mascotas' será una lista de objetos Mascota
    mascotas = relationship("Mascota", back_populates="dueno", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente {self.nombre}>"