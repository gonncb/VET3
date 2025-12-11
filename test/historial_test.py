import sys
import os
from datetime import date
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
# Modelos
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.historial import HistorialMedico
from app.models.producto import Producto
# Repositorios
from app.repositories.historial_repository import HistorialRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.producto_repository import ProductoRepository
# Servicio
from app.services.medical_service import MedicalService

@pytest.fixture
def session():
    engine = get_engine(test_mode=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_crear_historial_con_producto_y_descontar_stock(session):
    # 1. PREPARACIÓN (Setup)
    # Creamos repositorios
    hist_repo = HistorialRepository(session)
    client_repo = ClienteRepository(session)
    prod_repo = ProductoRepository(session)
    
    # Instanciamos el servicio con las 3 DEPENDENCIAS (Esto es lo que fallaba antes)
    service = MedicalService(hist_repo, client_repo, prod_repo)
    
    # Creamos datos base (Vet, Cliente, Mascota, Producto)
    vet = Veterinario(nombre="Dra. Polo", especialidad="Ley", num_colegiado="55", password="00")
    cliente = Cliente(dni="88B", nombre="Luis", telefono="900")
    mascota = Mascota(nombre="Garfield", especie="Gato")
    cliente.mascotas.append(mascota)
    producto = Producto(nombre="Vacuna", categoria="X", precio=10.0, stock=50) # Stock inicial 50
    
    session.add_all([vet, cliente, producto])
    session.commit()
    
    # Recuperamos IDs frescos
    id_mascota = session.query(Mascota).first().id
    id_vet = session.query(Veterinario).first().id
    id_prod = session.query(Producto).first().id
    
    # 2. EJECUCIÓN: Registramos consulta usando el producto
    service.registrar_consulta(
        id_mascota=id_mascota,
        id_veterinario=id_vet,
        diagnostico="Sano",
        descripcion="Vacunación",
        lista_ids_productos=[id_prod] # Usamos la vacuna
    )
    
    # 3. VERIFICACIÓN
    # A. Chequear que el historial existe
    historial = service.obtener_historial_mascota(id_mascota)
    assert len(historial) == 1
    assert historial[0].diagnostico == "Sano"
    
    # B. Chequear que el producto se ha guardado en la relación
    assert len(historial[0].productos_utilizados) == 1
    assert historial[0].productos_utilizados[0].nombre == "Vacuna"
    
    # C. ¡IMPORTANTE! Chequear que el STOCK ha bajado de 50 a 49
    prod_actualizado = prod_repo.buscar_por_id(id_prod)
    assert prod_actualizado.stock == 49