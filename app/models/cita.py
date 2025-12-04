from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(String, nullable=False)
    
    # Relación con Mascota
    id_mascota = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    mascota = relationship("app.models.mascota.Mascota")
    
    # Relación con Veterinario
    id_veterinario = Column(Integer, ForeignKey("veterinarios.id"), nullable=False)
    veterinario = relationship("app.models.veterinario.Veterinario")

    def __repr__(self):
        return f"<Cita {self.fecha} - {self.mascota.nombre}>"