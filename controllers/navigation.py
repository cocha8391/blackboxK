"""
Controlador de navegación - Gestiona swipes y cambios de página.
"""

from utils.constants import TOTAL_PAGES, PAGE_SPLASH
from utils.logger import get_logger

logger = get_logger()


class NavigationController:
    """
    Controlador de navegación.
    Interpreta gestos (swipes) del usuario y navega entre páginas.
    """

    def __init__(self):
        """Inicializa con la página splash."""
        self.current_page = PAGE_SPLASH
        logger.info("NavigationController", f"Página inicial: {self.current_page}")

    def on_splash_touched(self) -> None:
        """
        Usuario tocó splash.
        Transiciona a la primera página no-splash.
        """
        self.current_page = 1
        logger.info("NavigationController", "Splash tocado → Página 1")

    def on_swipe_left(self) -> bool:
        """
        Usuario hizo swipe hacia izquierda.
        Avanza a la siguiente página.

        Returns:
            bool: True si la navegación fue válida, False si ya está en última página
        """
        if self.current_page < TOTAL_PAGES - 1:
            self.current_page += 1
            logger.debug("NavigationController", f"Swipe izq → Página {self.current_page}")
            return True
        return False

    def on_swipe_right(self) -> bool:
        """
        Usuario hizo swipe hacia derecha.
        Retrocede a la página anterior.

        Returns:
            bool: True si la navegación fue válida, False si ya está en página 0
        """
        if self.current_page > PAGE_SPLASH + 1:
            self.current_page -= 1
            logger.debug("NavigationController", f"Swipe der → Página {self.current_page}")
            return True
        return False

    def go_to_page(self, page: int) -> bool:
        """
        Navega a una página específica.

        Args:
            page: Número de página (0-3)

        Returns:
            bool: True si es válida y se navega, False si es inválida
        """
        if 0 <= page < TOTAL_PAGES:
            self.current_page = page
            logger.debug("NavigationController", f"Ir a página {page}")
            return True
        return False

    def get_current_page(self) -> int:
        """Obtiene la página actual."""
        return self.current_page

    def get_scroll_position(self) -> float:
        """
        Obtiene la posición de scroll normalizada (0.0-1.0).

        Returns:
            float: Posición: 0.0 (splash), 0.33, 0.66, 1.0 (última)
        """
        return self.current_page / (TOTAL_PAGES - 1)
