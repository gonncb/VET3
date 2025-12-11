import os
from dotenv import load_dotenv
from app.database import engine, Base, SessionLocal
# Importamos modelos
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from app.models.producto import Producto

# Cargar variables de entorno
load_dotenv()

def inicializar_db():
    print("🏗️  Verificando estructura de base de datos...")
    
    # 1. Crear tablas (Si no existen)
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas sincronizadas.")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return

    # 2. Crear USUARIO ADMIN por defecto (Seguro)
    session = SessionLocal()
    try:
        # Buscamos si ya existe un admin para no duplicarlo
        admin_existente = session.query(Veterinario).filter_by(num_colegiado="admin").first()
        
        if not admin_existente:
            print("👤 Creando usuario Administrador inicial...")
            
            # Leemos la contraseña del .env
            admin_pass = os.getenv("ADMIN_PASSWORD")
            
            if admin_pass:
                admin = Veterinario(
                    nombre="Administrador", 
                    especialidad="Dirección", 
                    num_colegiado="admin", 
                    password=admin_pass 
                )
                session.add(admin)
                session.commit()
                print(f"✅ Admin creado. Usuario: 'admin' | Contraseña: (La de tu .env)")
            else:
                print("⚠️  AVISO: No se ha definido ADMIN_PASSWORD en el archivo .env. No se creó el usuario.")
        else:
            print("ℹ️  El usuario Admin ya existe. No es necesario crearlo.")
            
    except Exception as e:
        print(f"❌ Error creando admin: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    inicializar_db()