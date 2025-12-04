from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Nombre de la base de datos real (se creará en la carpeta raíz)
DATABASE_URL = "sqlite:///./veterinaria.db"

# Clase Base para los modelos (Entidades)
Base = declarative_base()

def get_engine(test_mode=False):
    """
    Devuelve el motor de base de datos.
    Si test_mode es True, usa memoria RAM (rápido y limpio para tests).
    Si es False, usa el archivo real.
    """
    if test_mode:
        # DB en memoria (se borra al cerrar el programa)
        return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    else:
        # DB en archivo físico
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configuración global de sesión (para usarla luego en la app)
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)