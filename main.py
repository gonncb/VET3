import streamlit as st
from app.database import SessionLocal
# hola 
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
            
            # Menú de Navegación Actualizado
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
            st.info("Selecciona un módulo en el menú lateral para comenzar.")
            
            # Métricas rápidas (Dashboard)
            col1, col2, col3 = st.columns(3)
            with col1:
                n_clientes = len(services.clinic_service.obtener_todos_clientes())
                st.metric("Total Clientes", n_clientes)
            with col2:
                n_citas = len(services.cita_service.obtener_historial_citas())
                st.metric("Citas Agendadas", n_citas)
            with col3:
                st.metric("Consultas Hoy", "0")

        elif menu == "👥 Gestión Clientes":
            mostrar_gestion_clientes(services.clinic_service)
            
        elif menu == "📅 Gestión Citas":
            mostrar_gestion_citas(services.cita_service)
            
        elif menu == "📋 Historial Médico":
            # Pasamos el nuevo servicio médico a la vista
            mostrar_gestion_historiales(services.medical_service)

if __name__ == "__main__":
    main()