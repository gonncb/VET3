import pytest
from sqlalchemy import text
import sys
import os

# Aseguramos que Python encuentre la carpeta 'app' añadiendo la raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# AHORA IMPORTAMOS DIRECTAMENTE (Sin try/except)
from app.database import get_engine

def test_connection_sqlite():
    """
    Prueba que verifica que SQLAlchemy puede crear un motor y conectar.
    """
    # Usamos :memory: para que sea una DB volátil en RAM para el test
    engine = get_engine(test_mode=True)
    
    # Probamos la conexión real
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.scalar() == 1