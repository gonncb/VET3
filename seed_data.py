import os
import random
from datetime import date, time, timedelta
from dotenv import load_dotenv

# Importamos la base de datos y modelos
from app.database import SessionLocal, engine, Base
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico

# Cargar variables de entorno
load_dotenv()

def cargar_datos_prueba():
    print("🌱 INICIANDO CARGA MASIVA DE DATOS...")

    # 1. Obtener contraseñas del .env
    pass_admin = os.getenv("ADMIN_PASSWORD")
    pass_house = os.getenv("VET_PASSWORD")
    pass_grey = os.getenv("GREY_PASSWORD")
    pass_dolittle = os.getenv("DOLITTLE_PASSWORD")

    # Validación de seguridad: Si no hay variables, paramos.
    if not all([pass_admin, pass_house, pass_grey, pass_dolittle]):
        print("❌ ERROR DE SEGURIDAD: Faltan contraseñas en el archivo .env")
        print("ℹ️  Asegúrate de definir: ADMIN_PASSWORD, VET_PASSWORD, GREY_PASSWORD, DOLITTLE_PASSWORD")
        return

    # 2. Reiniciar Base de Datos
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos limpiada y recreada.")
    except Exception as e:
        print(f"❌ Error en DB: {e}")
        return

    session = SessionLocal()

    try:
        # --- 3. CREAR PERSONAL (VETERINARIOS) ---
        print("👤 Creando equipo médico...")
        
        # Usamos las variables cargadas, NO escribimos nada aquí
        admin = Veterinario(nombre="Admin General", especialidad="Dirección", num_colegiado="admin", password=pass_admin)
        vet1 = Veterinario(nombre="Dr. Gregory House", especialidad="Diagnóstico", num_colegiado="100", password=pass_house)
        vet2 = Veterinario(nombre="Dra. Meredith Grey", especialidad="Cirugía", num_colegiado="200", password=pass_grey)
        vet3 = Veterinario(nombre="Dr. John Dolittle", especialidad="Exóticos", num_colegiado="300", password=pass_dolittle)

        session.add_all([admin, vet1, vet2, vet3])
        session.commit()

        # --- 4. CREAR CLIENTES Y MASCOTAS ---
        print("👥 Creando clientes y pacientes...")

        c1 = Cliente(dni="1111A", nombre="Ana García", telefono="600111222")
        m1 = Mascota(nombre="Thor", especie="Perro")
        c1.mascotas.append(m1)

        c2 = Cliente(dni="2222B", nombre="Luis Gómez", telefono="600333444")
        m2_a = Mascota(nombre="Garfield", especie="Gato")
        m2_b = Mascota(nombre="Odie", especie="Perro")
        c2.mascotas.extend([m2_a, m2_b])

        c3 = Cliente(dni="3333C", nombre="María López", telefono="600555666")
        m3 = Mascota(nombre="Piolín", especie="Ave")
        c3.mascotas.append(m3)

        c4 = Cliente(dni="4444D", nombre="Carlos Ruiz", telefono="600777888")
        m4 = Mascota(nombre="Rocky", especie="Perro")
        c4.mascotas.append(m4)
        
        c5 = Cliente(dni="5555E", nombre="Elena White", telefono="600999000")
        m5 = Mascota(nombre="Stuart", especie="Roedor")
        c5.mascotas.append(m5)

        session.add_all([c1, c2, c3, c4, c5])
        session.commit()

        # Recuperamos objetos frescos para las relaciones
        # Nota: Podríamos usar los objetos anteriores, pero recargar asegura que tienen ID real de la DB
        vet1 = session.query(Veterinario).filter_by(num_colegiado="100").first()
        vet2 = session.query(Veterinario).filter_by(num_colegiado="200").first()
        vet3 = session.query(Veterinario).filter_by(num_colegiado="300").first()

        # --- 5. GENERAR CITAS ---
        print("📅 Generando agenda de citas...")
        
        lista_citas = []
        hoy = date.today()
        manana = hoy + timedelta(days=1)
        pasado = hoy + timedelta(days=2)

        # Citas HOY
        lista_citas.append(Cita(fecha=hoy, hora=time(9,0), motivo="Vacunación Anual", id_mascota=m1.id, id_veterinario=vet1.id))
        lista_citas.append(Cita(fecha=hoy, hora=time(10,30), motivo="Revisión Cirugía", id_mascota=m4.id, id_veterinario=vet2.id))
        lista_citas.append(Cita(fecha=hoy, hora=time(12,0), motivo="Pico inflamado", id_mascota=m3.id, id_veterinario=vet3.id))
        lista_citas.append(Cita(fecha=hoy, hora=time(16,0), motivo="Chequeo General", id_mascota=m2_a.id, id_veterinario=vet1.id))

        # Citas FUTURAS
        lista_citas.append(Cita(fecha=manana, hora=time(11,0), motivo="Esterilización", id_mascota=m2_b.id, id_veterinario=vet2.id))
        lista_citas.append(Cita(fecha=pasado, hora=time(17,0), motivo="Revisión dientes", id_mascota=m5.id, id_veterinario=vet3.id))

        session.add_all(lista_citas)

        # --- 6. HISTORIAL MÉDICO ---
        print("📜 Generando historiales médicos antiguos...")
        
        h1 = HistorialMedico(
            fecha=hoy - timedelta(days=30),
            diagnostico="Gastroenteritis leve",
            descripcion="Se prescribe dieta blanda durante 3 días y reposo.",
            id_mascota=m1.id,
            id_veterinario=vet1.id
        )
        
        h2 = HistorialMedico(
            fecha=hoy - timedelta(days=7),
            diagnostico="Sobrepeso",
            descripcion="El paciente excede el peso ideal. Se recomienda cambio de pienso.",
            id_mascota=m2_a.id,
            id_veterinario=vet1.id
        )

        session.add_all([h1, h2])
        session.commit()

        print("✅ ¡TODO LISTO! Base de datos cargada con éxito.")
        print("-" * 50)
        print("ℹ️  USUARIOS DISPONIBLES (Contraseñas ocultas):")
        
        print("   1. Admin: admin           | (Ver clave ADMIN_PASSWORD en .env)")
        print("   2. House: 100             | (Ver clave VET_PASSWORD en .env)")
        print("   3. Grey: 200              | (Ver clave GREY_PASSWORD en .env)")
        print("   4. Dolittle: 300          | (Ver clave DOLITTLE_PASSWORD en .env)")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Ocurrió un error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    cargar_datos_prueba()