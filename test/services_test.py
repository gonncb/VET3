import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.models.veterinario import Veterinario
from app.repositories.veterinario_repository import VeterinarioRepository
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos el servicio (QUE AÚN NO EXISTE)
try:
    from app.services.auth_service import AuthService
except ImportError:
    pass

@pytest.fixture
def db_session():
    engine = get_engine(test_mode=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Pre-cargamos un veterinario para probar el login
    repo = VeterinarioRepository(session)
    repo.guardar(Veterinario(nombre="Test", especialidad="X", num_colegiado="admin", password="123"))
    
    yield session
    session.close()

def test_login_correcto(db_session):
    try:
        # Inyectamos dependencias (Session -> Repo -> Service)
        repo = VeterinarioRepository(db_session)
        service = AuthService(repo)
        
        # Intentamos login correcto
        usuario = service.login("admin", "123")
        assert usuario is not None
        assert usuario.nombre == "Test"
        
    except NameError:
        pytest.fail("AuthService no definido")

def test_login_incorrecto(db_session):
    try:
        repo = VeterinarioRepository(db_session)
        service = AuthService(repo)
        
        # Intentamos login con password mal
        usuario = service.login("admin", "password_falsa")
        assert usuario is None
        
    except NameError:
        pytest.fail("AuthService no definido")