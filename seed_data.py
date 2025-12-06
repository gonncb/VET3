import os
from dotenv import load_dotenv # <--- Importamos esto
from app.database import SessionLocal, engine, Base
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from datetime import date, time

# 1. Cargar variables de entorno del archivo .env
load_dotenv()

def cargar_datos_prueba():
    print("🌱 Iniciando carga de datos de prueba...")
    
    # Obtenemos las contraseñas del entorno (Environment Variables)
    # os.getenv("NOMBRE_VAR", "valor_por_defecto_si_falla")
    admin_pass = os.getenv("ADMIN_PASSWORD")
    vet_pass = os.getenv("VET_PASSWORD")

    if not admin_pass or not vet_pass:
        print("❌ ERROR CRÍTICO: No se han encontrado las contraseñas en el archivo .env")
        print("Crea un archivo .env con ADMIN_PASSWORD y VET_PASSWORD antes de continuar.")
        return

    try:
        # Reinicio de tablas...
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        session = SessionLocal()

        # 2. Crear Usuarios usando las variables seguras
        print("👤 Creando usuarios seguros...")
        
        admin = Veterinario(
            nombre="Admin", 
            especialidad="Dirección", 
            num_colegiado="admin", 
            password=admin_pass  # <--- Usamos la variable, no el texto
        )
        
        vet1 = Veterinario(
            nombre="Dr. House", 
            especialidad="Diagnóstico", 
            num_colegiado="100", 
            password=vet_pass    # <--- Usamos la variable
        )
        
        session.add(admin)
        session.add(vet1)
        session.commit()

        # ... (El resto del código de Clientes, Mascotas y Citas sigue igual) ...
        
        # (Aquí añade el resto del código que ya tenías para crear clientes/citas)
        # ...
        
        # Parte final del script:
        print("👥 Creando clientes y citas de ejemplo...")
        # ... [Pega aquí el resto de tu lógica de clientes/citas] ...
        
        # Como ejemplo resumido para que funcione el script completo, aquí tienes el bloque final:
        cliente = Cliente(dni="1111A", nombre="Ana Garcia", telefono="600111222")
        mascota = Mascota(nombre="Thor", especie="Perro")
        cliente.mascotas.append(mascota)
        session.add(cliente)
        session.commit()
        
        vet_db = session.query(Veterinario).filter_by(num_colegiado="100").first()
        mascota_db = session.query(Mascota).filter_by(nombre="Thor").first()
        
        cita = Cita(fecha=date.today(), hora=time(10,30), motivo="Rev", id_mascota=mascota_db.id, id_veterinario=vet_db.id)
        session.add(cita)
        
        hist = HistorialMedico(fecha=date.today(), diagnostico="OK", descripcion="Todo bien", id_mascota=mascota_db.id, id_veterinario=vet_db.id)
        session.add(hist)
        
        session.commit()

        print("✅ ¡DATOS SEGUROS CARGADOS!")
        print(f"🔑 Admin Pass: {admin_pass[0]}*** (Oculta)")
        print(f"🔑 Vet Pass:   {vet_pass[0]}*** (Oculta)")

    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    cargar_datos_prueba()