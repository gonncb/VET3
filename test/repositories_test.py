import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.models.veterinario import Veterinario
import sys
import os

# Ajuste de path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos el repositorio (QUE AÚN NO EXISTE)
try:
    from app.repositories.veterinario_repository import VeterinarioRepository
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

def test_repo_guardar_y_buscar(session):
    try:
        # 1. Instanciar repositorio
        repo = VeterinarioRepository(session)
        
        # 2. Crear objeto
        nuevo_vet = Veterinario(
            nombre="Dr. Strange", 
            especialidad="Cirugía Mística", 
            num_colegiado="999", 
            password="time"
        )
        
        # 3. Usar el repositorio para guardar
        repo.guardar(nuevo_vet)
        
        # 4. Usar el repositorio para buscar
        vet_encontrado = repo.buscar_por_colegiado("999")
        
        assert vet_encontrado is not None
        assert vet_encontrado.nombre == "Dr. Strange"
        
    except NameError:
        pytest.fail("La clase 'VeterinarioRepository' no está definida")