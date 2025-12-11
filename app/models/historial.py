from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla intermedia para la relación Muchos-a-Muchos entre Historial y Productos
historial_productos = Table(
    'historial_productos', Base.metadata,
    Column('historial_id', Integer, ForeignKey('historiales_medicos.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('productos.id'), primary_key=True)
)

class HistorialMedico(Base):
    __tablename__ = "historiales_medicos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    diagnostico = Column(String, nullable=False)
    descripcion = Column(Text, nullable=False)
    
    # Relaciones
    id_mascota = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    mascota = relationship("app.models.mascota.Mascota")
    
    id_veterinario = Column(Integer, ForeignKey("veterinarios.id"), nullable=False)
    veterinario = relationship("app.models.veterinario.Veterinario")

    # Relación con Productos (NUEVO)
    productos_utilizados = relationship("app.models.producto.Producto", secondary=historial_productos)

    def __repr__(self):
        return f"<Historial {self.fecha} - {self.mascota.nombre}>"