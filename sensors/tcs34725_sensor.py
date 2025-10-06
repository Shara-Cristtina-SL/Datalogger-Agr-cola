"""
Sensor: TCS34725 (Cor RGB)
Descrição:
- Lê os valores de vermelho, verde e azul (RGB).
- Utiliza barramento I2C da Labrador 32.
- Pode ser usado para detectar mudanças de cor em folhas ou luz ambiente.
"""

from machine import I2C, Pin
import tcs34725  # Biblioteca MicroPython para TCS34725

# Inicializa I2C (usar a mesma instância ou criar nova)
i2c = I2C(1, scl=Pin(5), sda=Pin(3), freq=100000)
sensor = tcs34725.TCS34725(i2c)

def read_TCS34725():
    """
    Retorna:
        r (int): componente vermelho
        g (int): componente verde
        b (int): componente azul
    """
    r, g, b, _ = sensor.read()  # O quarto valor é o clear, ignorado
    return r, g, b
