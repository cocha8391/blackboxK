"""
Ventana principal y canvas - Gestiona la interfaz base.
"""

import tkinter as tk
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FULLSCREEN_MODE, TOTAL_PAGES
from utils.logger import get_logger

logger = get_logger()


class MainWindow:
    """
    Ventana principal de la aplicación.
    Proporciona el canvas para desplazamiento horizontal y métodos de navegación.
    """

    def __init__(self):
        """Inicializa la ventana."""
        self.root = tk.Tk()
        self.root.title("Black Box K - Dashboard")

        # Configurar ventana
        if FULLSCREEN_MODE:
            self.root.attributes("-fullscreen", True)
            self.window_width = self.root.winfo_screenwidth()
            self.window_height = self.root.winfo_screenheight()
        else:
            self.window_width = WINDOW_WIDTH
            self.window_height = WINDOW_HEIGHT
            self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Canvas principal con desplazamiento
        self.container = tk.Canvas(
            self.root,
            width=self.window_width,
            height=self.window_height,
            highlightthickness=0,
        )
        self.container.pack(fill="both", expand=True)
        self.container.configure(scrollregion=(0, 0, self.window_width * TOTAL_PAGES, self.window_height))

        logger.info("MainWindow", f"Ventana creada ({WINDOW_WIDTH}x{WINDOW_HEIGHT})")

        # Diccionario para almacenar frames de páginas
        self.frames = {}

    def add_frame(self, frame_name: str, frame: tk.Frame, page_index: int) -> None:
        """
        Añade un frame a una página específica.

        Args:
            frame_name: Nombre identificador del frame
            frame: El frame de Tkinter
            page_index: Índice de página (0-3)
        """
        self.frames[frame_name] = frame
        self.container.create_window(
            (WINDOW_WIDTH * page_index, 0),
            window=frame,
            anchor="nw",
        )
        logger.debug("MainWindow", f"Frame '{frame_name}' añadido a página {page_index}")

    def navigate_to_page(self, page_index: int) -> None:
        """
        Navega a una página específica con animación suave.

        Args:
            page_index: Índice de página (0-3)
        """
        if page_index < 0 or page_index >= TOTAL_PAGES:
            return

        scroll_x = page_index / TOTAL_PAGES
        self.container.xview_moveto(scroll_x)
        logger.debug("MainWindow", f"Navegando a página {page_index}")

    def bind_event(self, event: str, handler) -> None:
        """
        Vincula un evento a un manejador.

        Args:
            event: Nombre del evento (ej: "<ButtonPress-1>")
            handler: Función manejadora
        """
        self.root.bind(event, handler)

    def get_root(self) -> tk.Tk:
        """Obtiene la ventana raíz."""
        return self.root

    def after(self, ms: int, func, *args) -> str:
        """Programa una función para ejecutarse después de ms milisegundos."""
        return self.root.after(ms, func, *args)

    def run(self) -> None:
        """Inicia el loop principal de Tkinter."""
        logger.info("MainWindow", "Iniciando mainloop")
        self.root.mainloop()

    def quit(self) -> None:
        """Cierra la aplicación."""
        logger.info("MainWindow", "Cerrando aplicación")
        self.root.quit()
