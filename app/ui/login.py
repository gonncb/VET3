import streamlit as st
from app.services.auth_service import AuthService

def mostrar_login(auth_service: AuthService):
    """
    Muestra el formulario de login.
    Recibe el servicio de autenticación ya instanciado (Inyección de dependencias).
    """
    st.title("🔐 Acceso Veterinarios")
    
    with st.form("login_form"):
        col1, col2 = st.columns(2)
        usuario = col1.text_input("Número de Colegiado")
        password = col2.text_input("Contraseña", type="password")
        
        submit = st.form_submit_button("Entrar")
        
        if submit:
            # Aquí es donde la UI llama a la Lógica de Negocio
            veterinario = auth_service.login(usuario, password)
            
            if veterinario:
                st.success(f"¡Bienvenido, {veterinario.nombre}!")
                # Guardamos en sesión
                st.session_state['usuario'] = veterinario
                st.rerun()
            else:
                st.error("Credenciales incorrectas")