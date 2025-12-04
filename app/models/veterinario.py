from sqlalchemy import Column, Integer, String
from app.database import Base

class Veterinario(Base):
    __tablename__ = "veterinarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)
    num_colegiado = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) # Para el login futuro

    def __repr__(self):
        return f"<Veterinario {self.nombre}>"