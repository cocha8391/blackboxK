"""
Funciones de conversión de datos.
Convierte valores ADC a corriente (mA) y luego a unidades de usuario.
"""

from utils.constants import ADC_MAX, ADC_MIN, MA_MAX, MA_MIN


def adc_to_milliamps(adc_counts: int) -> float:
    """
    Convierte conteos ADC a miliamperios (4-20mA).

    Args:
        adc_counts: Valor crudo del ADC

    Returns:
        Valor en miliamperios (float)

    Fórmula:
        mA = ((ADC - ADC_MIN) / (ADC_MAX - ADC_MIN)) * (MA_MAX - MA_MIN) + MA_MIN
    """
    if adc_counts is None:
        return 0.0

    ma = ((adc_counts - ADC_MIN) / (ADC_MAX - ADC_MIN)) * (MA_MAX - MA_MIN) + MA_MIN
    return round(ma, 2)


def milliamps_to_uservalue(ma: float, min_scale: float, max_scale: float) -> float:
    """
    Convierte miliamperios a unidades de usuario (PSI, °C, etc).

    Args:
        ma: Valor en miliamperios
        min_scale: Valor mínimo en unidades de usuario (ej: 0 PSI)
        max_scale: Valor máximo en unidades de usuario (ej: 232 PSI)

    Returns:
        Valor en unidades de usuario (float)

    Fórmula (escala lineal 4-20mA):
        user_value = ((mA - 4) / 16) * (max_scale - min_scale) + min_scale
    """
    if ma is None:
        return 0.0

    user_value = ((ma - MA_MIN) / (MA_MAX - MA_MIN)) * (max_scale - min_scale) + min_scale
    return round(user_value, 1)


def adc_to_uservalue(
    adc_counts: int, min_scale: float, max_scale: float
) -> float:
    """
    Conversión completa: ADC → mA → Unidades de usuario.

    Es la combinación de adc_to_milliamps() + milliamps_to_uservalue().

    Args:
        adc_counts: Valor crudo del ADC
        min_scale: Valor mínimo en unidades de usuario
        max_scale: Valor máximo en unidades de usuario

    Returns:
        Valor final en unidades de usuario (float)
    """
    ma = adc_to_milliamps(adc_counts)
    return milliamps_to_uservalue(ma, min_scale, max_scale)
