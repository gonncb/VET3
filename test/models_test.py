import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.cliente import Cliente
from app.models.mascota import Mascota

# Configuración de base de datos en memoria para tests
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_crear_cliente_y_mascota(session):
    # 1. Crear Cliente
    cliente = Cliente(dni="12345678A", nombre="Juan Pérez", telefono="600123456")
    
    # 2. Crear Mascota
    mascota = Mascota(nombre="Fido", especie="Perro")
    
    # 3. Asociar
    cliente.mascotas.append(mascota)
    
    # 4. Guardar
    session.add(cliente)
    session.commit()
    
    # 5. Comprobaciones
    assert cliente.id is not None
    assert mascota.id is not None
    assert len(cliente.mascotas) == 1
    assert cliente.mascotas[0].nombre == "Fido"
    
    # --- AQUÍ ESTABA EL ERROR ---
    # Antes ponía: assert mascota.dueno == cliente
    # Ahora debe poner:
    assert mascota.cliente == cliente  # <--- CORREGIDO: Usamos 'cliente'