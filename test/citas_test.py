import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import date, time
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota

# Intentamos importar lo que NO EXISTE
try:
    from app.models.cita import Cita
    from app.repositories.cita_repository import CitaRepository
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

def test_crear_cita_con_relaciones(session):
    try:
        # 1. Crear datos previos necesarios (Vet, Cliente, Mascota)
        vet = Veterinario(nombre="Dr. House", especialidad="Diag", num_colegiado="1", password="1")
        cliente = Cliente(dni="1A", nombre="Pepe", telefono="600")
        mascota = Mascota(nombre="Toby", especie="Perro", id_cliente=1) # Asumiendo ID 1
        
        # Guardamos previos
        session.add(vet)
        session.add(cliente)
        session.commit() # Esto asigna IDs
        
        # Asignamos mascota al cliente (forma ORM)
        cliente.mascotas.append(mascota)
        session.commit()

        # 2. Usar Repositorio de Citas
        repo_citas = CitaRepository(session)
        
        # 3. Crear la Cita
        nueva_cita = Cita(
            fecha=date(2025, 10, 20),
            hora=time(10, 30),
            motivo="Vacuna",
            id_mascota=mascota.id,
            id_veterinario=vet.id
        )
        
        repo_citas.guardar(nueva_cita)
        
        # 4. Verificar
        cita_db = repo_citas.buscar_todas()[0]
        
        assert cita_db.motivo == "Vacuna"
        assert cita_db.mascota.nombre == "Toby"      # Relación funciona
        assert cita_db.veterinario.nombre == "Dr. House" # Relación funciona
        
    except NameError:
        pytest.fail("Cita o CitaRepository no definidos")