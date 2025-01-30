# WDIC_Projekt
Ziel unseres WDIC Projekts war es die Daten eines DHT2402 (Temperatursensors) auszulesen und diese via WLAN zu einem anderem Raspberry zu schiken. Dafür haben wir folgenden Aufbau benötigt.

![Image](https://github.com/user-attachments/assets/9a124d5c-8693-411b-bd51-60a1cc4a68ea)

# Code auf Sender

Damit wir die Daten des Sensors auslesen können haben ich mithilfe von VNC Real Viewer direk auf dem raspberry pi mit thonny programmiert.

```
import adafruit_dht
import board
import socket
import time

sensor = adafruit_dht.DHT11(board.D4)

SERVER_IP = "192.168.1.102"  
PORT = 5000  

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

while True:
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        data = f"Temperature: {temperature}C, Humidity: {humidity}%"
        print("Sending:", data)
        
        client_socket.sendall(data.encode())  

    except RuntimeError as error:
        print("Error:", error.args[0])
    
    time.sleep(2)  

client_socket.close()
```
Dieses script gab uns folgende ausgabe

![Image](https://github.com/user-attachments/assets/beb415cb-7561-4342-84ff-72dc90a9ffbe)

Wie man hier sehen kann wurde die Temperatur und die Luffeuchtigkeit erfolgreich ausgelesen und an den Zweiten Raspberry gesendet.
