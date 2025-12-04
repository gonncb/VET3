from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class HistorialMedico(Base):
    __tablename__ = "historiales_medicos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    diagnostico = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False) # Texto largo para detalles
    
    # Relaciones
    id_mascota = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    mascota = relationship("app.models.mascota.Mascota")
    
    id_veterinario = Column(Integer, ForeignKey("veterinarios.id"), nullable=False)
    veterinario = relationship("app.models.veterinario.Veterinario")

    def __repr__(self):
        return f"<Historial {self.fecha} - {self.mascota.nombre}>"