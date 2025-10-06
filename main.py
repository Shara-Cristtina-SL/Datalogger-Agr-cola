import machine, sdcard, uos, time
from datetime import datetime
from sensors.aht10_sensor import read_AHT10
from sensors.bh1750_sensor import read_BH1750
from sensors.tcs34725_sensor import read_TCS34725

# ----------------------------
# Inicializa cartão SD (SPI0)
# ----------------------------
spi = machine.SPI(0, baudrate=1_000_000,
                  sck=machine.Pin(23),   # GPIOC22
                  mosi=machine.Pin(19),  # GPIOC25
                  miso=machine.Pin(21))  # GPIOC24
cs = machine.Pin(24, machine.Pin.OUT)    # GPIOC23
sd = sdcard.SDCard(spi, cs)

# Monta SD na pasta /sd
uos.mount(sd, "/sd")

DATA_FOLDER = "/sd/data"
INTERVAL = 60  # segundos

if not uos.path.exists(DATA_FOLDER):
    uos.mkdir(DATA_FOLDER)

# ----------------------------
# Função para criar arquivo diário
# ----------------------------
def get_log_file():
    today = datetime.now().strftime("%Y-%m-%d")
    folder = DATA_FOLDER + "/" + today
    if not uos.path.exists(folder):
        uos.mkdir(folder)
    return folder + "/log.txt"

# ----------------------------
# Função principal
# ----------------------------
def log_data():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        temp, hum = read_AHT10()
        lux = read_BH1750()
        r, g, b = read_TCS34725()

        log_line = f"{timestamp}, Temp: {temp} °C, Umid: {hum}%, Lux: {lux}, RGB: ({r},{g},{b})\n"

        with open(get_log_file(), "a") as f:
            f.write(log_line)

        print(log_line.strip())
        time.sleep(INTERVAL)

if __name__ == "__main__":
    log_data()
