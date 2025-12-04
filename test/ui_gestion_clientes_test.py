import sys
import os
# Ajuste de ruta para que encuentre la carpeta 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.repositories.cliente_repository import ClienteRepository
from app.services.clinic_service import ClinicService

@pytest.fixture
def session():
    """Crea una base de datos en memoria limpia para cada test"""
    engine = get_engine(test_mode=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_registrar_cliente_con_mascota_exito(session):
    # 1. Preparación
    repo = ClienteRepository(session)
    service = ClinicService(repo)
    
    # 2. Ejecución: Registramos un cliente nuevo
    resultado = service.registrar_cliente_completo(
        dni="1234A", 
        nombre="Carlos", 
        telefono="600123", 
        nombre_mascota="Rex", 
        especie="Perro"
    )
    
    # 3. Verificación
    assert resultado is True
    
    # Comprobamos en la base de datos real
    cliente_db = repo.buscar_por_dni("1234A")
    assert cliente_db is not None
    assert cliente_db.nombre == "Carlos"
    assert len(cliente_db.mascotas) == 1
    assert cliente_db.mascotas[0].nombre == "Rex"
    assert cliente_db.mascotas[0].especie == "Perro"

def test_bloquear_dni_duplicado(session):
    # 1. Preparación
    repo = ClienteRepository(session)
    service = ClinicService(repo)
    
    # Registramos el primero
    service.registrar_cliente_completo("1111A", "Juan", "600", "Boby", "Perro")
    
    # 2. Ejecución: Intentamos registrar el mismo DNI
    resultado = service.registrar_cliente_completo(
        dni="1111A",  # DUPLICADO
        nombre="Otro Juan", 
        telefono="700", 
        nombre_mascota="Luna", 
        especie="Gato"
    )
    
    # 3. Verificación
    assert resultado is False  # Debe fallar
    
    # Aseguramos que no se ha modificado el original
    cliente_db = repo.buscar_por_dni("1111A")
    assert cliente_db.nombre == "Juan" # Sigue siendo el primero