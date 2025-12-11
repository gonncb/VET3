from app.database import engine, Base
# Importamos todos los modelos para que SQLAlchemy sepa qué tablas crear
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from app.models.producto import Producto

def crear_tablas():
    print("🏗️ Creando estructura de base de datos (Tablas vacías)...")
    try:
        # Esto crea las tablas si no existen, pero NO inserta datos
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas correctamente.")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")

if __name__ == "__main__":
    crear_tablas()