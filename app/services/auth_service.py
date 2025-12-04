from app.repositories.veterinario_repository import VeterinarioRepository

class AuthService:
    def __init__(self, veterinario_repo: VeterinarioRepository):
        self.repo = veterinario_repo

    def login(self, num_colegiado, password):
        """
        Verifica credenciales.
        Devuelve el objeto Veterinario si es correcto, None si falla.
        """
        # 1. Buscamos al usuario en la DB
        veterinario = self.repo.buscar_por_colegiado(num_colegiado)
        
        # 2. Si existe, comprobamos la contraseña
        # NOTA: En un sistema real, aquí usaríamos 'bcrypt' para hashear contraseñas.
        # Por simplicidad ahora, comparamos texto plano.
        if veterinario and veterinario.password == password:
            return veterinario
        
        return None