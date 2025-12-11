import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.repositories.cliente_repository import ClienteRepository
from app.services.clinic_service import ClinicService
# Importamos TODOS los modelos para que la BD de test se cree bien
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.veterinario import Veterinario
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from app.models.producto import Producto

@pytest.fixture
def session():
    """Crea una base de datos en memoria limpia para cada test"""
    engine = get_engine(test_mode=True)
    Base.metadata.drop_all(engine) # Aseguramos limpieza
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_registrar_cliente_con_mascota_exito(session):
    repo = ClienteRepository(session)
    service = ClinicService(repo)
    
    resultado = service.registrar_cliente_completo(
        dni="1234A", 
        nombre="Carlos", 
        telefono="600123", 
        nombre_mascota="Rex", 
        especie="Perro"
    )
    
    assert resultado is True
    cliente_db = repo.buscar_por_dni("1234A")
    assert cliente_db is not None
    assert len(cliente_db.mascotas) == 1

def test_estadisticas_especies(session):
    # Test del nuevo método para el gráfico circular
    repo = ClienteRepository(session)
    service = ClinicService(repo)
    
    # Registramos 2 perros y 1 gato
    service.registrar_cliente_completo("1A", "Pepe", "000", "Boby", "Perro")
    service.registrar_cliente_completo("2B", "Ana", "000", "Thor", "Perro")
    service.registrar_cliente_completo("3C", "Luis", "000", "Mishi", "Gato")
    
    stats = service.obtener_estadisticas_especies()
    
    assert stats["Perro"] == 2
    assert stats["Gato"] == 1