import streamlit as st
import pandas as pd # Importante para los gráficos
from app.database import SessionLocal

# --- IMPORTACIÓN DE REPOSITORIOS (Acceso a Datos) ---
from app.repositories.veterinario_repository import VeterinarioRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.cita_repository import CitaRepository
from app.repositories.historial_repository import HistorialRepository

# --- IMPORTACIÓN DE SERVICIOS (Lógica de Negocio) ---
from app.services.auth_service import AuthService
from app.services.clinic_service import ClinicService
from app.services.cita_service import CitaService
from app.services.medical_service import MedicalService

# --- IMPORTACIÓN DE VISTAS (Interfaz Gráfica) ---
from app.ui.login import mostrar_login
from app.ui.gestion_clientes import mostrar_gestion_clientes
from app.ui.gestion_citas import mostrar_gestion_citas
from app.ui.gestion_historiales import mostrar_gestion_historiales

# Configuración de la página
st.set_page_config(page_title="VetManager Pro", page_icon="🐾", layout="wide")

class ServiceContainer:
    """
    CONTENEDOR DE INYECCIÓN DE DEPENDENCIAS (SOLID - DIP)
    Inicializa todos los repositorios y servicios una sola vez.
    """
    def __init__(self):
        # 1. Sesión de Base de Datos
        self.db = SessionLocal()
        
        # 2. Repositorios (Capa de Datos)
        self.vet_repo = VeterinarioRepository(self.db)
        self.client_repo = ClienteRepository(self.db)
        self.cita_repo = CitaRepository(self.db)
        self.historial_repo = HistorialRepository(self.db)
        
        # 3. Servicios (Capa de Lógica)
        self.auth_service = AuthService(self.vet_repo)
        self.clinic_service = ClinicService(self.client_repo)
        
        # El servicio de citas coordina Citas, Veterinarios y Clientes
        self.cita_service = CitaService(self.cita_repo, self.vet_repo, self.client_repo)
        
        # El servicio médico necesita acceder al historial y buscar clientes
        self.medical_service = MedicalService(self.historial_repo, self.client_repo)

def main():
    # Instanciamos el contenedor
    services = ServiceContainer()

    # --- LÓGICA DE LOGIN ---
    if 'usuario' not in st.session_state:
        mostrar_login(services.auth_service)
    
    # --- APLICACIÓN PRINCIPAL ---
    else:
        usuario = st.session_state['usuario']
        
        # --- SIDEBAR (Menú Lateral) ---
        with st.sidebar:
            st.title("🏥 VetManager")
            st.markdown(f"**Dr/a:** {usuario.nombre}")
            st.markdown(f"**Nº Col:** {usuario.num_colegiado}")
            st.divider()
            
            # Menú de Navegación
            menu = st.radio(
                "Menú Principal", 
                [
                    "📊 Panel de Control", 
                    "👥 Gestión Clientes", 
                    "📅 Gestión Citas", 
                    "📋 Historial Médico"
                ]
            )
            
            st.divider()
            if st.button("🚪 Cerrar Sesión"):
                del st.session_state['usuario']
                st.rerun()

        # --- ÁREA DE CONTENIDO ---
        
        if menu == "📊 Panel de Control":
            st.title(f"Bienvenido al Sistema, {usuario.nombre}")
            st.markdown("---")
            
            # 1. Obtenemos datos frescos de los servicios (Lógica de Negocio)
            clientes = services.clinic_service.obtener_todos_clientes()
            stats_citas = services.cita_service.obtener_estadisticas_dashboard()
            
            # 2. FILA DE MÉTRICAS (KPIs)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="👥 Total Clientes", 
                    value=len(clientes),
                    delta="Activos"
                )
            
            with col2:
                # Calculamos total mascotas sumando las de cada cliente
                total_mascotas = sum(len(c.mascotas) for c in clientes)
                st.metric(
                    label="🐾 Pacientes", 
                    value=total_mascotas
                )

            with col3:
                st.metric(
                    label="📅 Citas Totales", 
                    value=stats_citas["total_citas"]
                )
                
            with col4:
                # Destacamos las citas de hoy
                citas_hoy = stats_citas["citas_hoy"]
                st.metric(
                    label="🔔 Citas HOY", 
                    value=citas_hoy,
                    delta=f"{citas_hoy} pendientes" if citas_hoy > 0 else "Agenda libre",
                    delta_color="inverse" # Rojo si sube (ocupado), verde si baja
                )

            st.markdown("---")

            # 3. GRÁFICOS Y ACCESOS RÁPIDOS
            col_chart, col_actions = st.columns([2, 1])
            
            with col_chart:
                st.subheader("📊 Carga de Trabajo por Veterinario")
                datos_grafico = stats_citas["citas_por_vet"]
                
                if datos_grafico:
                    # Convertimos el diccionario a DataFrame para Streamlit
                    df_chart = pd.DataFrame.from_dict(datos_grafico, orient='index', columns=['Citas'])
                    st.bar_chart(df_chart)
                else:
                    st.info("No hay datos suficientes para generar gráficos.")

            with col_actions:
                st.subheader("🚀 Accesos Rápidos")
                with st.expander("¿Qué quieres hacer?", expanded=True):
                    if st.button("➕ Nuevo Paciente", use_container_width=True):
                        st.info("Ve a la pestaña 'Gestión Clientes'")
                    
                    if st.button("📅 Ver Agenda Completa", use_container_width=True):
                        st.info("Ve a la pestaña 'Gestión Citas'")
                    
                    if st.button("📋 Escribir Historial", use_container_width=True):
                        st.info("Ve a la pestaña 'Historial Médico'")

        elif menu == "👥 Gestión Clientes":
            mostrar_gestion_clientes(services.clinic_service)
            
        elif menu == "📅 Gestión Citas":
            mostrar_gestion_citas(services.cita_service)
            
        elif menu == "📋 Historial Médico":
            mostrar_gestion_historiales(services.medical_service)

if __name__ == "__main__":
    main()