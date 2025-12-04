import sys
import os

# --- Ajustar la ruta ANTES de importar nada de 'app' ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# -------------------------------------------------------------------

import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.models.cliente import Cliente
from app.models.mascota import Mascota

# Intentamos importar el repositorio
try:
    from app.repositories.cliente_repository import ClienteRepository
except ImportError:
    pass

@pytest.fixture
def session():
    engine = get_engine(test_mode=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_guardar_cliente_con_mascotas(session):
    try:
        repo = ClienteRepository(session)
        
        # Creamos cliente
        cliente = Cliente(dni="5555X", nombre="Maria", telefono="600111222")
        # Creamos mascota asociada
        mascota = Mascota(nombre="Luna", especie="Gato")
        cliente.mascotas.append(mascota)
        
        # Guardamos SOLO al cliente
        repo.guardar(cliente)
        
        # Verificamos si se guardó la mascota también (Cascade)
        cliente_db = repo.buscar_por_dni("5555X")
        
        assert cliente_db is not None
        assert cliente_db.nombre == "Maria"
        assert len(cliente_db.mascotas) == 1
        assert cliente_db.mascotas[0].nombre == "Luna"
        
    except NameError:
        pytest.fail("ClienteRepository no definido")