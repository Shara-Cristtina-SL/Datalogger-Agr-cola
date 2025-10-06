
---

## 📋 Objetivo do Projeto

Criar um sistema autônomo que:
- Coleta dados de múltiplos sensores (temperatura, umidade, luminosidade e cor);
- Registra periodicamente as leituras em um **arquivo .txt** no **cartão microSD**;
- Inclui **timestamp** (data e hora) em cada registro;
- Garante gravação confiável e organizada dos dados.

---

## ⚙️ Arquitetura Geral

O sistema é composto pelos seguintes módulos:

| Módulo / Arquivo | Função |
|------------------|--------|
| `main.py` | Gerencia o fluxo principal: coleta, formatação e gravação dos dados. |
| `sd_logger.py` | Responsável por montar o cartão SD via SPI e gravar os dados em arquivos. |
| `sensors/aht10_sensor.py` | Leitura de temperatura e umidade (sensor AHT10). |
| `sensors/bh1750_sensor.py` | Leitura de luminosidade em lux (sensor BH1750). |
| `sensors/tcs34725_sensor.py` | Leitura de cor RGB (sensor TCS34725). |

---

## 🧠 Funcionamento do Sistema

1. **Inicialização:**  
   O `main.py` configura o cartão SD e inicializa os sensores I²C.

2. **Coleta de Dados:**  
   A cada intervalo (por padrão, 60 segundos), o código lê:
   - Temperatura e umidade (AHT10);
   - Luminosidade (BH1750);
   - Cor RGB (TCS34725).

3. **Registro:**  
   Cada linha do arquivo contém:
```

YYYY-MM-DD HH:MM:SS, Temp: 24.8 °C, Umid: 58.3%, Lux: 832, RGB: (120,45,38)

```
O arquivo é salvo em `/sd/data/YYYY-MM-DD/log.txt`, com **um novo diretório para cada dia**.

4. **Armazenamento:**  
O módulo `sd_logger.py` utiliza o barramento **SPI** para comunicação com o SD card, controlando o chip select (CS), clock (SCK), entrada e saída de dados (MOSI/MISO).

---

## 📡 Sensores e Endereços I²C

| Sensor | Tipo | Endereço I²C | Pinos (Labrador) | Variáveis medidas |
|--------|------|---------------|------------------|-------------------|
| AHT10 | Temperatura / Umidade | `0x38` | SDA=3, SCL=5 | °C e % |
| BH1750 | Luminosidade | `0x23` | SDA=3, SCL=5 | Lux |
| TCS34725 | Cor RGB | `0x29` | SDA=3, SCL=5 | R, G, B |

🧩 Todos compartilham o **mesmo barramento I²C**, diferenciados por seus **endereços únicos**.

---

## 💾 Cartão microSD

O SD card é conectado via **SPI**, utilizando os seguintes pinos:

| Sinal | Função | Pino Labrador |
|--------|---------|---------------|
| MISO | Master In Slave Out | GPIOC24 (pino 21) |
| MOSI | Master Out Slave In | GPIOC25 (pino 19) |
| SCK | Clock | GPIOC22 (pino 23) |
| CS | Chip Select | GPIOC23 (pino 24) |
| VCC | Alimentação | 3.3V |
| GND | Terra | GND |

📁 Os arquivos de log são gravados em:
```

/sd/data/2025-10-05/log.txt

````

---

## 🧰 Bibliotecas Utilizadas

Para sensores reais (MicroPython):

```bash
micropython-ahtx0
micropython-bh1750
micropython-tcs34725
````

Para simulação no PC (Python):

```bash
python-periphery==2.4.1
```

---

## ▶️ Execução

### 🔹 Simulação (no PC)

```bash
python main.py
```

### 🔹 Versão Real (na Labrador 32)

Copie todos os arquivos para o sistema de arquivos da Labrador e execute:

```bash
python3 main.py
```

ou, em MicroPython:

```bash
import main
```

---

## 🧾 Estrutura de Diretórios

```
📂 datalogger_agricola/
├── main.py
├── sd_logger.py
├── sensors/
│   ├── aht10_sensor.py
│   ├── bh1750_sensor.py
│   └── tcs34725_sensor.py
└── data/              # Criado automaticamente
```

---

## 🧩 Explicação Técnica do SD Card

A gravação é feita com:

```python
with open(get_log_file(), "a") as f:
    f.write(log_line)
```

📍 O arquivo é aberto no modo **append (“a”)**, garantindo que:

* Nenhum dado antigo seja sobrescrito;
* Novas linhas sejam adicionadas ao final do arquivo;
* O sistema seja resiliente a reinicializações.

O caminho do arquivo é gerado dinamicamente conforme a data do sistema:

```python
def get_log_file():
    today = datetime.now().strftime("%Y-%m-%d")
    folder = DATA_FOLDER + "/" + today
    if not uos.path.exists(folder):
        uos.mkdir(folder)
    return folder + "/log.txt"
```

---

## 📊 Aplicações Possíveis

* Monitoramento ambiental de estufas agrícolas 🌱
* Controle de iluminação e temperatura em viveiros ☀️
* Estudos de microclimas urbanos 🌆
* Registro de dados experimentais em campo 🧪

---



