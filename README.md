# tequ-bee-nest-scale-v2
This repository is of the Bee Nest scale device. This version uses a cellular 4G network for data sending, instead of the LoRaWAN network, which the old version used. 

## Hardware
Table of all hardware used, the XBee 3 Global LTE-M/NB-IoT module shouldbe connected to the XBee Explorer Regulated board.
| Hardware               | Model         | Placement       | Link          |
| -------------          |:-------------:| :-------------: | :-------------:|
| Cellular module                  | XBee 3 Global LTE-M/NB-IoT       | Control box     | <a href="https://www.digi.com/products/embedded-systems/digi-xbee/cellular-modems/digi-xbee-3-global-lte-m-nb-iot">Link</a>|
| Board                  | XBee Explorer Regulated board       | Control box     | <a href="https://www.sparkfun.com/products/22032">Link</a>|
| Sparkfun OpenScale     | SEN-13261     | Control box     | <a href="https://www.sparkfun.com/products/13261">Link</a>|
| Temperature sensor     | DS18B20       | Control box     | <a href="https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf">Data sheet</a>|
| Scale unit             | Zemic L6W-C3-200kg-3G6   | Control box    | <a href="https://www.zemiceurope.com/media/Documentation/L6W_Datasheet.pdf">Data sheet</a>|
| Adafruit MiniBoost 5V @ 1A        | TPS61023       | Control box     | <a href="https://www.adafruit.com/product/4654">Data sheet</a>| |
| Battery holder         | CA 3 GS       | Control box     | |
| Batteries              | 3 x 1.5 AA    | Control box     | |
| Antenna                | 868 MHz    | Control box     | |

## Connections
Connections of the hardware used in prototype.
| Device                 | PIN           | Device         | PIN            | 
| -------------          |:-------------:| :-------------:| :-------------:|
| XBee Explorer Regulated board                | Vin           |  Battery                           | +              |
| XBee Explorer Regulated board                | GND           |  Battery                           | -              |
| XBee Explorer Regulated board                | TX            |  SEN-13261                         | TX             |
| XBee Explorer Regulated board                | RX            |  SEN-13261                         | RX             |
| XBee Explorer Regulated board                | DIO9            |  TPS61023                          | EN             |
| 868 MHz antenna        | uFl plug      |  XBee Explorer Regulated board                           | 868 MHz connector |
| DS18B20                | 5V SIG GND    |  SEN-13261                         | TEMP connector    |
| TPS61023               | OUT           |  SEN-13261                         | 5V             |
| Battery                | -             |  SEN-13261                         | GND            |
| SEN-13261              | E+            |  Zemic L6W-C3-200kg-3G6            | Input (+)      |
| SEN-13261              | E-            |  Zemic L6W-C3-200kg-3G6            | Input (-)      |
| SEN-13261              | A+            |  Zemic L6W-C3-200kg-3G6            | Output (+)     |
| SEN-13261              | A-            |  Zemic L6W-C3-200kg-3G6            | Output (-)     |
| SEN-13261              | SHD           |  Zemic L6W-C3-200kg-3G6            | Shield         |


## Development

### 1. Install XCTU
First you'll need to install XCTU <a href="https://hub.digi.com/support/products/xctu/?_gl=1*1st7wxh*_gcl_au*MTI2NjE3MzcwMS4xNzE3NDE0MjQz*_ga*MTY5OTkxNjUuMTcxNzQxNDI0Mw..*_ga_RZXDK3PM3B*MTcxNzY3MTgxNi4xNC4wLjE3MTc2NzE4MTYuNjAuMC4w">here</a>, from the Resources & Utilites, scroll down to find it.

### 2. Connect and verify XBee 3 Global LTE-M/NB-IoT configuration
1. After installation is complete, open the program.
2. Connect the XBee 3 Global LTE-M/NB-IoT to a breakout board with USB connection, for example <a href="https://www.digi.com/products/models/xbib-cu-th">this</a>.
3. Connect the Dev board to your computer via the USB-C port.
4. Press the board search button in the upper-left corner and select the port on which you've connected the Dev Board.
5. Once the board is found, press the Add selected devices button.
6. Double click the added device on the left menu and wait for it to load.
7. Find the Serial Interfacing dropdown and switch the API Enable setting to `MicroPython REPL [4]`
8. Finally press the Write button to write your changes to the device. 

### 3. Install PyCharm
First you'll need to install PyCharm, the version has to be 2024.1.2 or below. You can find the professional and community versions <a href="https://www.jetbrains.com/pycharm/download/?section=windows">here</a>. Run the donwloaded installer file and follow given instructions. You can skip this step if you already have the correct version installed.

### 4. Install the Digi XBee plugin
Next you'll need to install the Digi XBee plugin in PyCharm. When opening PyCharm you should see a Plugins tab on a menu on the left, from here search for `Digi XBee` and install the plugin. You can also install it from the settings menu, just open up settings and search for plugins.

### 5. Clone this repository
You can clone the repository with the command:
```
git clone https://github.com/Lapland-UAS-Tequ/tequ-bee-nest-scale-v2.git
```
or by downloading and unzipping the repository.

### 6. Modify config
In the repository you'll find a config.json file. In here you can modify the MQTT url, port and password. By default here they are left blank.
Example config:
```
{
  "url": "",
  "password": "",
  "port": ""
```

### 7. Upload code and verify operation
