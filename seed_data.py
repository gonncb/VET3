import os
import random
from datetime import date, time, timedelta
from dotenv import load_dotenv

# Importamos la base de datos y todos los modelos
from app.database import SessionLocal, engine, Base
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from app.models.producto import Producto  # <--- IMPORTANTE: Modelo de Productos

# Cargar variables de entorno
load_dotenv()

def cargar_datos_prueba():
    print("🌱 INICIANDO CARGA MASIVA DE DATOS (V2.0)...")

    # 1. Obtener contraseñas del .env
    pass_admin = os.getenv("ADMIN_PASSWORD")
    pass_house = os.getenv("VET_PASSWORD")
    pass_grey = os.getenv("GREY_PASSWORD")
    pass_dolittle = os.getenv("DOLITTLE_PASSWORD")

    # Validación de seguridad
    if not all([pass_admin, pass_house, pass_grey, pass_dolittle]):
        print("❌ ERROR DE SEGURIDAD: Faltan contraseñas en el archivo .env")
        print("ℹ️  Asegúrate de definir: ADMIN_PASSWORD, VET_PASSWORD, GREY_PASSWORD, DOLITTLE_PASSWORD")
        return

    # 2. Reiniciar Base de Datos (Borrón y cuenta nueva)
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos limpiada y recreada.")
    except Exception as e:
        print(f"❌ Error al reiniciar la DB: {e}")
        return

    session = SessionLocal()

    try:
        # --- 3. CREAR PERSONAL (VETERINARIOS) ---
        print("👤 Creando equipo médico...")
        
        admin = Veterinario(nombre="Admin General", especialidad="Dirección", num_colegiado="admin", password=pass_admin)
        vet1 = Veterinario(nombre="Dr. Gregory House", especialidad="Diagnóstico", num_colegiado="100", password=pass_house)
        vet2 = Veterinario(nombre="Dra. Meredith Grey", especialidad="Cirugía", num_colegiado="200", password=pass_grey)
        vet3 = Veterinario(nombre="Dr. John Dolittle", especialidad="Exóticos", num_colegiado="300", password=pass_dolittle)

        session.add_all([admin, vet1, vet2, vet3])
        session.commit() # Commit para generar IDs

        # --- 4. CREAR INVENTARIO (PRODUCTOS) ---
        print("📦 Llenando el almacén y farmacia...")
        
        # Productos variados con distinto stock
        p1 = Producto(nombre="Vacuna Polivalente", categoria="Vacuna", precio=35.00, stock=50)
        p2 = Producto(nombre="Antibiótico Oral 500mg", categoria="Medicamento Oral", precio=12.50, stock=100)
        p3 = Producto(nombre="Collar Isabelino (M)", categoria="Accesorio", precio=8.00, stock=15)
        p4 = Producto(nombre="Suero Fisiológico", categoria="Inyectable", precio=5.00, stock=5) # STOCK BAJO (Alerta Dashboard)
        p5 = Producto(nombre="Pipeta Antipulgas", categoria="Medicamento Externo", precio=22.00, stock=30)

        session.add_all([p1, p2, p3, p4, p5])
        session.commit()

        # --- 5. CREAR CLIENTES Y MASCOTAS (Variedad de especies) ---
        print("👥 Creando clientes y pacientes...")

        # Cliente 1: Ana con Thor (Perro)
        c1 = Cliente(dni="1111A", nombre="Ana García", telefono="600111222")
        m1 = Mascota(nombre="Thor", especie="Perro")
        c1.mascotas.append(m1)

        # Cliente 2: Luis con Garfield (Gato) y Odie (Perro)
        c2 = Cliente(dni="2222B", nombre="Luis Gómez", telefono="600333444")
        m2_a = Mascota(nombre="Garfield", especie="Gato")
        m2_b = Mascota(nombre="Odie", especie="Perro")
        c2.mascotas.extend([m2_a, m2_b])

        # Cliente 3: María con Piolín (Ave)
        c3 = Cliente(dni="3333C", nombre="María López", telefono="600555666")
        m3 = Mascota(nombre="Piolín", especie="Ave")
        c3.mascotas.append(m3)

        # Cliente 4: Carlos con Rocky (Perro) y Bugs (Roedor)
        c4 = Cliente(dni="4444D", nombre="Carlos Ruiz", telefono="600777888")
        m4_a = Mascota(nombre="Rocky", especie="Perro")
        m4_b = Mascota(nombre="Bugs", especie="Roedor")
        c4.mascotas.extend([m4_a, m4_b])
        
        # Cliente 5: Elena con Stuart (Roedor)
        c5 = Cliente(dni="5555E", nombre="Elena White", telefono="600999000")
        m5 = Mascota(nombre="Stuart", especie="Roedor")
        c5.mascotas.append(m5)

        session.add_all([c1, c2, c3, c4, c5])
        session.commit()

        # Recuperamos objetos frescos para usar sus IDs en citas
        # Nota: Usamos query para asegurar que están vinculados a la sesión actual
        vet1 = session.query(Veterinario).filter_by(num_colegiado="100").first()
        vet2 = session.query(Veterinario).filter_by(num_colegiado="200").first()
        vet3 = session.query(Veterinario).filter_by(num_colegiado="300").first()
        
        prod_vacuna = session.query(Producto).filter_by(nombre="Vacuna Polivalente").first()
        prod_ab = session.query(Producto).filter_by(nombre="Antibiótico Oral 500mg").first()

        # --- 6. GENERAR CITAS (AGENDA) ---
        print("📅 Generando agenda de citas...")
        
        lista_citas = []
        hoy = date.today()
        manana = hoy + timedelta(days=1)
        pasado = hoy + timedelta(days=2)

        # Citas HOY (Para activar contadores del Dashboard)
        lista_citas.append(Cita(fecha=hoy, hora=time(9,0), motivo="Vacunación Anual", id_mascota=m1.id, id_veterinario=vet1.id))
        lista_citas.append(Cita(fecha=hoy, hora=time(10,30), motivo="Revisión Cirugía", id_mascota=m4_a.id, id_veterinario=vet2.id))
        lista_citas.append(Cita(fecha=hoy, hora=time(12,0), motivo="Pico inflamado", id_mascota=m3.id, id_veterinario=vet3.id))
        lista_citas.append(Cita(fecha=hoy, hora=time(16,0), motivo="Chequeo General", id_mascota=m2_a.id, id_veterinario=vet1.id))

        # Citas FUTURAS
        lista_citas.append(Cita(fecha=manana, hora=time(11,0), motivo="Esterilización", id_mascota=m2_b.id, id_veterinario=vet2.id))
        lista_citas.append(Cita(fecha=pasado, hora=time(17,0), motivo="Revisión dientes", id_mascota=m5.id, id_veterinario=vet3.id))

        session.add_all(lista_citas)

        # --- 7. HISTORIAL MÉDICO CON PRODUCTOS ---
        print("📜 Generando historiales médicos y consumiendo stock...")
        
        # Historial 1: Thor se puso una vacuna
        h1 = HistorialMedico(
            fecha=hoy - timedelta(days=30),
            diagnostico="Sano - Vacunación correcta",
            descripcion="Se aplica vacuna anual. El paciente reacciona bien.",
            id_mascota=m1.id,
            id_veterinario=vet1.id
        )
        # Aquí simulamos que se usó un producto en el pasado
        h1.productos_utilizados.append(prod_vacuna)
        
        # Historial 2: Garfield con infección
        h2 = HistorialMedico(
            fecha=hoy - timedelta(days=7),
            diagnostico="Infección leve",
            descripcion="Se prescribe antibiótico durante 5 días.",
            id_mascota=m2_a.id,
            id_veterinario=vet1.id
        )
        h2.productos_utilizados.append(prod_ab)

        session.add_all([h1, h2])
        session.commit()

        print("✅ ¡TODO LISTO! Base de datos cargada con éxito.")
        print("-" * 60)
        print("ℹ️  RESUMEN DE ACCESO (Contraseñas en tu archivo .env):")
        print("   1. Admin:    admin")
        print("   2. House:    100")
        print("   3. Grey:     200")
        print("   4. Dolittle: 300")
        print("-" * 60)

    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    cargar_datos_prueba()