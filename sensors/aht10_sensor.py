"""
Sensor: AHT10 (Temperatura e Umidade)
Descrição:
- Lê temperatura e umidade relativa do ar.
- Utiliza barramento I2C da Labrador 32.
- Retorna valores arredondados para facilitar registro no datalogger.
"""

from machine import I2C, Pin
import ahtx0  # Biblioteca MicroPython para AHT10

# Inicializa I2C (ajuste pinos conforme a sua conexão)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
sensor = ahtx0.AHT10(i2c)

def read_AHT10():
    """
    Retorna:
        temp (float): temperatura em °C
        hum (float): umidade relativa em %
    """
    temp = sensor.temperature
    hum = sensor.relative_humidity
    return round(temp, 1), round(hum, 1)
