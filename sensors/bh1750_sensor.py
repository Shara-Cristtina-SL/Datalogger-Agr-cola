"""
Sensor: BH1750 (Luminosidade)
Descrição:
- Lê intensidade de luz em lux.
- Utiliza barramento I2C da Labrador 32.
- Retorna valor inteiro, adequado para gravação em arquivos de log.
"""

from machine import I2C, Pin
import bh1750  # Biblioteca MicroPython para BH1750

# Inicializa I2C (usar a mesma instância ou criar nova)
i2c = I2C(1, scl=Pin(5), sda=Pin(3), freq=100000)
sensor = bh1750.BH1750(i2c)

def read_BH1750():
    """
    Retorna:
        lux (int): intensidade de luz em lux
    """
    lux = sensor.luminance(bh1750.BH1750.CONT_HIRES_1)
    return int(lux)
