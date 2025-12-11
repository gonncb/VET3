from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Mascota(Base):
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especie = Column(String, nullable=False)
    
    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    
    # RELACIÓN: Una mascota pertenece a un Cliente
    # back_populates debe coincidir con el nombre de la variable en Cliente (que es 'mascotas')
    cliente = relationship("app.models.cliente.Cliente", back_populates="mascotas")

    def __repr__(self):
        return f"<Mascota {self.nombre}>"