import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.database import get_engine, Base
from sqlalchemy.orm import sessionmaker
from app.repositories.producto_repository import ProductoRepository
from app.services.inventory_service import InventoryService
from app.models.producto import Producto
# Importamos resto de modelos para evitar errores de Foreign Keys
from app.models.cliente import Cliente 
from app.models.mascota import Mascota
from app.models.veterinario import Veterinario
from app.models.cita import Cita
from app.models.historial import HistorialMedico

@pytest.fixture
def session():
    engine = get_engine(test_mode=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_gestion_inventario(session):
    repo = ProductoRepository(session)
    service = InventoryService(repo)
    
    # 1. Crear producto
    service.crear_producto("Collar", "Accesorio", 15.5, 10)
    
    prod = repo.buscar_todos()[0]
    assert prod.nombre == "Collar"
    assert prod.stock == 10
    
    # 2. Sumar stock (Reposición)
    service.actualizar_stock(prod.id, 5, "sumar")
    session.refresh(prod) # Refrescamos objeto desde DB
    assert prod.stock == 15
    
    # 3. Restar stock (Venta/Uso)
    service.actualizar_stock(prod.id, 3, "restar")
    session.refresh(prod)
    assert prod.stock == 12
    
    # 4. Probar que no baja de 0
    service.actualizar_stock(prod.id, 100, "restar") # Intentamos restar 100 a 12
    session.refresh(prod)
    assert prod.stock == 0 # Debería quedarse en 0, no -88