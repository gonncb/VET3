from app.database import SessionLocal, engine, Base
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from datetime import date, time

def cargar_datos_prueba():
    print("🌱 Iniciando carga de datos de prueba...")
    
    # 1. Recrear tablas limpias
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()

    # 2. Crear Veterinarios
    admin = Veterinario(nombre="Admin", especialidad="Dirección", num_colegiado="admin", password="123")
    vet1 = Veterinario(nombre="Dr. House", especialidad="Diagnóstico", num_colegiado="100", password="100")
    session.add(admin)
    session.add(vet1)
    session.commit()

    # 3. Crear Cliente
    cliente = Cliente(dni="1111A", nombre="Ana Garcia", telefono="600111222")
    
    # 4. Crear Mascota y asociarla
    mascota = Mascota(nombre="Thor", especie="Perro", id_cliente=cliente.id)
    # Nota: Al añadir la mascota a la lista, SQLAlchemy gestiona las IDs tras el commit
    cliente.mascotas.append(mascota)
    
    session.add(cliente)
    session.commit() # Aquí se generan los IDs de cliente y mascota

    # Recuperamos los objetos con sus IDs frescos
    vet_db = session.query(Veterinario).filter_by(num_colegiado="100").first()
    mascota_db = session.query(Mascota).filter_by(nombre="Thor").first()

    # 5. Crear Cita
    cita = Cita(
        fecha=date.today(),
        hora=time(10, 30),
        motivo="Revisión General",
        id_mascota=mascota_db.id,
        id_veterinario=vet_db.id
    )
    session.add(cita)

    # 6. Crear Historial
    historial = HistorialMedico(
        fecha=date.today(),
        diagnostico="Sano",
        descripcion="El paciente presenta buen estado general.",
        id_mascota=mascota_db.id,
        id_veterinario=vet_db.id
    )
    session.add(historial)
    
    session.commit()
    session.close()
    print("✅ ¡Datos cargados! Usuario: admin / Contraseña: 123")

if __name__ == "__main__":
    cargar_datos_prueba()