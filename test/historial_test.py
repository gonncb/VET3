import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import date
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota

# Importamos lo que NO EXISTE
try:
    from app.models.historial import HistorialMedico
    from app.repositories.historial_repository import HistorialRepository
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

def test_crear_historial_medico(session):
    try:
        # 1. Preparar entorno (Vet, Cliente, Mascota)
        vet = Veterinario(nombre="Dra. Polo", especialidad="Ley", num_colegiado="55", password="00")
        cliente = Cliente(dni="88B", nombre="Luis", telefono="900")
        mascota = Mascota(nombre="Garfield", especie="Gato", id_cliente=1)
        
        session.add(vet)
        session.add(cliente)
        session.commit()
        cliente.mascotas.append(mascota)
        session.commit()
        
        # 2. Usar Repo de Historial
        repo = HistorialRepository(session)
        
        # 3. Crear Entrada Médica
        entrada = HistorialMedico(
            fecha=date.today(),
            descripcion="Vacuna triple felina aplicada.",
            diagnostico="Sano",
            id_mascota=mascota.id,
            id_veterinario=vet.id
        )
        
        repo.guardar(entrada)
        
        # 4. Verificar
        historial_db = repo.buscar_por_mascota(mascota.id)
        assert len(historial_db) == 1
        assert historial_db[0].descripcion == "Vacuna triple felina aplicada."
        assert historial_db[0].veterinario.nombre == "Dra. Polo"
        
    except NameError:
        pytest.fail("HistorialMedico o Repository no definidos")