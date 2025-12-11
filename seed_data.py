import os
import random
from datetime import date, time, timedelta
from dotenv import load_dotenv

# Importamos DB y Modelos
from app.database import SessionLocal, engine, Base
from app.models.veterinario import Veterinario
from app.models.cliente import Cliente
from app.models.mascota import Mascota
from app.models.cita import Cita
from app.models.historial import HistorialMedico
from app.models.producto import Producto

load_dotenv()

# --- CONSTANTES PARA GENERACIÓN ALEATORIA ---
NOMBRES_PERSONAS = ["Laura", "Carlos", "Ana", "David", "Elena", "Jorge", "Sofía", "Miguel", "Lucía", "Pablo", "Marta", "Daniel", "Carmen", "Alejandro", "Paula", "Javier", "Cristina", "Álvaro", "Isabel", "Adrián"]
APELLIDOS = ["García", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Fernández", "Moreno", "Jiménez", "Ruiz", "Hernández", "Díaz", "Álvarez", "Muñoz"]
NOMBRES_PERROS = ["Thor", "Luna", "Max", "Nala", "Kira", "Rocky", "Lola", "Zeus", "Coco", "Bimba", "Simba", "Noa", "Bruno", "Dana", "Duke", "Mia", "Jack", "Maya", "Toby", "Duna"]
NOMBRES_GATOS = ["Garfield", "Luna", "Simba", "Nala", "Pelusa", "Oreo", "Mishifu", "Salem", "Nina", "Loki", "Coco", "Mia", "Felix", "Gris", "Sombra"]
NOMBRES_OTROS = ["Piolín", "Bugs", "Stuart", "Nemo", "Dory", "Sonic", "Pikachu", "Yoshi", "Rayo", "Manchitas"]
DIAGNOSTICOS = [
    ("Otitis externa", "Inflamación del conducto auditivo. Se aplica limpieza y gotas."),
    ("Gastroenteritis", "Vómitos y diarrea. Dieta blanda y suero."),
    ("Vacunación Anual", "Aplicación de vacuna polivalente y revisión general."),
    ("Dermatitis alérgica", "Picores y rojeces. Se prescribe corticoide y cambio de dieta."),
    ("Revisión Dental", "Acumulación de sarro leve. Se programa limpieza."),
    ("Cuerpo extraño", "Ha ingerido un juguete. Se realiza radiografía."),
    ("Conjuntivitis", "Ojos llorosos. Se aplica colirio antibiótico."),
    ("Control de Peso", "El paciente ha bajado 200g. Evolución favorable.")
]

def obtener_telefono():
    return f"6{random.randint(0,9)}{random.randint(0,9)}{random.randint(100000, 999999)}"

def obtener_dni():
    return f"{random.randint(10000000, 99999999)}{random.choice('TRWAGMYFPDXBNJZSQVHLCKE')}"

def cargar_datos_prueba():
    print("🌱 INICIANDO CARGA PROFESIONAL DE DATOS (V4.0 - Agenda Mañana Tarde)...")

    # 1. Seguridad
    pass_admin = os.getenv("ADMIN_PASSWORD")
    pass_house = os.getenv("VET_PASSWORD")
    pass_grey = os.getenv("GREY_PASSWORD")
    pass_dolittle = os.getenv("DOLITTLE_PASSWORD")

    if not all([pass_admin, pass_house, pass_grey, pass_dolittle]):
        print("❌ ERROR: Faltan contraseñas en el .env")
        return

    # 2. Reset DB
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos recreada desde cero.")
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return

    session = SessionLocal()

    try:
        # --- 3. STAFF MÉDICO ---
        print("👨‍⚕️ Contratando personal...")
        admin = Veterinario(nombre="Director General", especialidad="Dirección", num_colegiado="admin", password=pass_admin)
        vet1 = Veterinario(nombre="Dr. Gregory House", especialidad="Diagnóstico", num_colegiado="100", password=pass_house)
        vet2 = Veterinario(nombre="Dra. Meredith Grey", especialidad="Cirugía", num_colegiado="200", password=pass_grey)
        vet3 = Veterinario(nombre="Dr. John Dolittle", especialidad="Exóticos", num_colegiado="300", password=pass_dolittle)
        
        vets = [vet1, vet2, vet3]
        session.add_all([admin] + vets)
        session.commit()

        # --- 4. INVENTARIO FARMACÉUTICO ---
        print("📦 Abasteciendo farmacia y almacén...")
        productos_lista = [
            Producto(nombre="Nobivac Rabia", categoria="Vacuna", precio=25.00, stock=45),
            Producto(nombre="Eurican Polivalente", categoria="Vacuna", precio=35.50, stock=30),
            Producto(nombre="Feligen (Gatos)", categoria="Vacuna", precio=28.00, stock=20),
            Producto(nombre="Amoxicilina 500mg", categoria="Medicamento Oral", precio=12.50, stock=100),
            Producto(nombre="Meloxicam (Antiinf.)", categoria="Medicamento Oral", precio=15.00, stock=80),
            Producto(nombre="Prednisona", categoria="Medicamento Oral", precio=8.50, stock=60),
            Producto(nombre="Suero Fisiológico 500ml", categoria="Inyectable", precio=6.00, stock=8),
            Producto(nombre="Apomorphina", categoria="Inyectable", precio=18.00, stock=5),
            Producto(nombre="Pipeta Frontline (S)", categoria="Medicamento Externo", precio=22.00, stock=25),
            Producto(nombre="Collar Scalibor", categoria="Accesorio", precio=28.00, stock=15),
            Producto(nombre="Bravecto Masticable", categoria="Medicamento Oral", precio=32.00, stock=40),
            Producto(nombre="Collar Isabelino (M)", categoria="Accesorio", precio=8.00, stock=12),
            Producto(nombre="Venda Cohesiva", categoria="Accesorio", precio=3.50, stock=50),
            Producto(nombre="Royal Canin Gastro Intestinal", categoria="Alimentación", precio=45.00, stock=10),
            Producto(nombre="Hill's Prescription Diet", categoria="Alimentación", precio=48.00, stock=6)
        ]
        session.add_all(productos_lista)
        session.commit()
        
        todos_productos = session.query(Producto).all()

        # --- 5. GENERACIÓN MASIVA DE CLIENTES Y MASCOTAS ---
        print("👥 Registrando base de datos de clientes...")
        
        clientes_generados = []
        for _ in range(30): # 30 Clientes
            nombre = f"{random.choice(NOMBRES_PERSONAS)} {random.choice(APELLIDOS)}"
            c = Cliente(dni=obtener_dni(), nombre=nombre, telefono=obtener_telefono())
            
            num_mascotas = random.choices([1, 2], weights=[80, 20])[0]
            
            for _ in range(num_mascotas):
                tipo = random.choices(["Perro", "Gato", "Exótico"], weights=[55, 35, 10])[0]
                
                if tipo == "Perro":
                    nombre_m = random.choice(NOMBRES_PERROS)
                    especie = "Perro"
                elif tipo == "Gato":
                    nombre_m = random.choice(NOMBRES_GATOS)
                    especie = "Gato"
                else:
                    nombre_m = random.choice(NOMBRES_OTROS)
                    especie = random.choice(["Ave", "Roedor", "Reptil"])
                
                m = Mascota(nombre=nombre_m, especie=especie)
                c.mascotas.append(m)
            
            clientes_generados.append(c)
        
        session.add_all(clientes_generados)
        session.commit()

        todas_mascotas = session.query(Mascota).all()

        # --- 6. HISTORIAL MÉDICO (PASADO) ---
        print("📜 Digitalizando expedientes antiguos...")
        
        historiales = []
        for _ in range(60): # 60 Consultas pasadas
            mascota = random.choice(todas_mascotas)
            vet = random.choice(vets)
            
            dias_atras = random.randint(1, 120)
            fecha_consulta = date.today() - timedelta(days=dias_atras)
            
            diag_titulo, diag_desc = random.choice(DIAGNOSTICOS)
            
            h = HistorialMedico(
                fecha=fecha_consulta,
                diagnostico=diag_titulo,
                descripcion=diag_desc,
                id_mascota=mascota.id,
                id_veterinario=vet.id
            )
            
            num_prods = random.randint(0, 2)
            if num_prods > 0:
                prods_usados = random.sample(todos_productos, num_prods)
                for p in prods_usados:
                    h.productos_utilizados.append(p)
                    if p.stock > 0: p.stock -= 1
            
            historiales.append(h)
        
        session.add_all(historiales)
        session.commit()

        # --- 7. AGENDA DE CITAS ---
        print("📅 Organizando la agenda (Inicio: Mañana por la tarde)...")
        
        citas = []
        hoy = date.today()
        manana = hoy + timedelta(days=1)
        
        # A. CITAS DE MAÑANA (Solo Tarde)
        # Definimos horas específicas empezando a las 16:00
        horas_tarde_manana = [time(16,0), time(16,30), time(17,0), time(17,45), time(18,15), time(19,0)]
        
        for hora in horas_tarde_manana:
            m = random.choice(todas_mascotas)
            v = random.choice(vets)
            motivo = random.choice(["Revisión de tarde", "Vacuna", "Urgencia leve", "Consulta general"])
            # Añadimos la cita para MAÑANA
            citas.append(Cita(fecha=manana, hora=hora, motivo=motivo, id_mascota=m.id, id_veterinario=v.id))
            
        # B. CITAS DEL RESTO DE LA SEMANA (Pasado mañana en adelante)
        for i in range(2, 8): # Desde pasado mañana hasta dentro de 7 días
            dia = hoy + timedelta(days=i)
            # Generamos entre 3 y 6 citas aleatorias por día
            for _ in range(random.randint(3, 6)):
                m = random.choice(todas_mascotas)
                v = random.choice(vets)
                # Horario aleatorio comercial (9:00 a 19:30)
                h = time(random.randint(9, 19), random.choice([0, 30]))
                citas.append(Cita(fecha=dia, hora=h, motivo="Consulta programada", id_mascota=m.id, id_veterinario=v.id))

        session.add_all(citas)
        session.commit()

        print("✅ ¡CARGA PROFESIONAL COMPLETADA!")
        print("📊 Estadísticas:")
        print(f"   - {len(clientes_generados)} Clientes")
        print(f"   - {len(todas_mascotas)} Pacientes")
        print(f"   - {len(historiales)} Historiales")
        print(f"   - {len(citas)} Citas Futuras (Empiezan mañana a las 16:00)")
        print("-" * 60)
        print("ℹ️  Nota: Al no haber citas 'HOY', el Dashboard mostrará 0 en 'Citas Hoy'.")

    except Exception as e:
        print(f"❌ Error fatal: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    cargar_datos_prueba()