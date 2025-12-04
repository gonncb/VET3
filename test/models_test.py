import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
import sys
import os

# Ajuste de path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importamos los modelos (QUE AÚN NO EXISTEN)
# Usamos try/except para que el test no explote antes de empezar, 
# pero fallará en las aserciones si no existen.
try:
    from app.models.veterinario import Veterinario
    from app.models.cliente import Cliente
    from app.models.mascota import Mascota
except ImportError:
    pass

@pytest.fixture
def session():
    """Fixture que crea una DB en memoria fresca para cada test"""
    engine = get_engine(test_mode=True)
    Base.metadata.create_all(engine)  # Crea tablas
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # Entrega la sesión al test
    session.close() # Limpieza post-test

def test_crear_veterinario(session):
    try:
        vet = Veterinario(nombre="Dr. House", especialidad="Diagnóstico", num_colegiado="1111", password="123")
        session.add(vet)
        session.commit()
    except NameError:
        pytest.fail("El modelo 'Veterinario' no está definido")

    vet_guardado = session.query(Veterinario).filter_by(num_colegiado="1111").first()
    assert vet_guardado is not None
    assert vet_guardado.nombre == "Dr. House"

def test_crear_cliente_y_mascota(session):
    try:
        # 1. Crear Cliente
        cliente = Cliente(dni="1234A", nombre="Juan Perez", telefono="600123123")
        session.add(cliente)
        session.commit()
        
        # 2. Crear Mascota asociada al cliente
        mascota = Mascota(nombre="Firulais", especie="Perro", id_cliente=cliente.id)
        session.add(mascota)
        session.commit()
    except NameError:
        pytest.fail("Los modelos 'Cliente' o 'Mascota' no están definidos")

    # 3. Verificar relación
    mascota_db = session.query(Mascota).filter_by(nombre="Firulais").first()
    assert mascota_db is not None
    assert mascota_db.dueno.nombre == "Juan Perez"  # Probamos la relación SQL (ORM)