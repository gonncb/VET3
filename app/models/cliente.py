from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    dni = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    telefono = Column(String)

    # RELACIÓN: Un cliente tiene muchas mascotas
    # Importante: back_populates debe coincidir con el nombre de la variable en Mascota (que es 'cliente')
    mascotas = relationship(
        "app.models.mascota.Mascota", 
        back_populates="cliente",  # <--- ANTES PONÍA "dueno", AHORA DEBE SER "cliente"
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cliente {self.nombre} ({self.dni})>"