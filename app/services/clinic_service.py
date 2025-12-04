from app.repositories.cliente_repository import ClienteRepository
from app.models.cliente import Cliente
from app.models.mascota import Mascota

class ClinicService:
    def __init__(self, cliente_repo: ClienteRepository):
        self.repo = cliente_repo

    def registrar_cliente_completo(self, dni, nombre, telefono, nombre_mascota, especie):
        """
        Registra un cliente nuevo y su primera mascota.
        Devuelve True si tiene éxito, False si el DNI ya existe.
        """
        # 1. Validación de Negocio: ¿Existe el DNI?
        if self.repo.buscar_por_dni(dni):
            return False  # El cliente ya existe
        
        # 2. Crear Entidades
        nuevo_cliente = Cliente(dni=dni, nombre=nombre, telefono=telefono)
        # Aquí creamos la mascota pero NO la guardamos todavía
        nueva_mascota = Mascota(nombre=nombre_mascota, especie=especie)
        
        # 3. Asociar (La magia de ORM)
        # Al añadir la mascota a la lista del cliente, SQLAlchemy entiende la relación
        nuevo_cliente.mascotas.append(nueva_mascota)
        
        # 4. Persistir (Guardar padre e hijo a la vez)
        self.repo.guardar(nuevo_cliente)
        return True
    
    def obtener_todos_clientes(self):
        return self.repo.buscar_todos()