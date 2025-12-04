from app.database import engine, Base
# IMPORTANTE: Importar todos los modelos para que SQLAlchemy sepa que debe crear las tablas
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita           # <--- Asegúrate que este está
from app.models.historial import HistorialMedico # <--- Y este también
from sqlalchemy.orm import sessionmaker

def init_db():
    print("🔄 Eliminando y recreando tablas...")
    # Esto borrará y creará todo desde cero (útil para desarrollo)
    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Crear Admin
    if not session.query(Veterinario).filter_by(num_colegiado="admin").first():
        print("👤 Creando usuario administrador...")
        admin = Veterinario(
            nombre="Administrador", 
            especialidad="Dirección", 
            num_colegiado="admin", 
            password="123"
        )
        session.add(admin)

    session.commit()
    session.close()
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_db()