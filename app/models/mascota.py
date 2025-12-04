from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    
    # Clave Foránea: Apunta a clientes.id
    id_cliente = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    # Relación inversa: Acceder al objeto Cliente desde la Mascota
    dueno = relationship("app.models.cliente.Cliente", back_populates="mascotas")

    def __repr__(self):
        return f"<Mascota {self.nombre}>"