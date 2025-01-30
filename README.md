# WDIC_Projekt
Ziel unseres WDIC Projekts war es die Daten eines DHT2402 (Temperatursensors) auszulesen und diese via WLAN zu einem anderem Raspberry zu senden. Dafür haben wir folgenden Aufbau benötigt.

![Image](https://github.com/user-attachments/assets/9a124d5c-8693-411b-bd51-60a1cc4a68ea)

# Code auf Sender

Damit wir die Daten des Sensors auslesen können haben ich mithilfe von VNC Real Viewer direkt auf dem raspberry pi mit thonny programmiert.

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
# Ausgabe des Script

![Image](https://github.com/user-attachments/assets/beb415cb-7561-4342-84ff-72dc90a9ffbe)

Wie man hier sehen kann wurde die Temperatur und die Luffeuchtigkeit erfolgreich ausgelesen und an den Zweiten Raspberry gesendet. Die Daten werden nun an den Zweiten Raspi (Patricks Raspi), der in unserem fall als TCP Server aggiert.

# Code auf Raspberry Pi, um die Daten, welche gesendet worden sind zu empfangen:

Auf Visual Studio Code habe ich eine Remote Verbindung (ssh) hergestellt. So kann das Python-file, welches programmiert wird direkt auf dem Raspberry Pi gespeichert werden, aber man kann gleichzeitig die Funktionen von VS Code nutzen.

```
import socket
 
def start_server(host='192.168.1.102', port=5000):
    """Startet einen Server, der Daten über WLAN empfängt."""

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
   
    print(f"Server gestartet auf {host}:{port}")
   
    while True:
       
        client_socket, client_address = server_socket.accept()
        print(f"Verbindung von {client_address} hergestellt")
       
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Empfangene Daten: {data.decode('utf-8')}")
        except Exception as e:
            print(f"Fehler: {e}")
        finally:
            client_socket.close()
            print("Verbindung geschlossen")
 
if __name__ == "__main__":
    start_server()

```

Das Programm startet einen einfachen TCP-Server auf dem Raspberry Zero 2W, der Daten über WLAN empfängt. Mit Hilfe des socket-Moduls wird eine Netzwerkverbindung geöffnet, um auf eingehende Verbindungen zu warten. Sobald ein Client (Raspberry Pi mit dem Sensor) eine Verbindung herstellt, empfängt der Server die gesendeten Daten und gibt sie in der Konsole aus. Wenn keine Daten mehr eintreffen, wird die Verbindung geschlossen. Das Programm läuft in einer Endlosschleife, um kontinuierlich neue Verbindungen eingehen zu können/ neue Verbindungen zu akzeptieren.

# Ausgabe der empfangenen Daten bzw. den Messwerten

![Image](https://github.com/user-attachments/assets/6a753022-4e82-4ac6-86af-02bd1998adec)

Der Server läuft auf dem Raspberry Pi mit der IP-Adresse 192.168.1.102 und ist jetzt bereit Daten zu empfangen.
Sobald das Programm auf dem zweiten Raspberry Pi gestartet worden ist, misst der Sensor zunächst die Temperatur und die Luftfeuchtigkeit. Diese Daten werden jetzt per WLAN an den Raspberry Pi gesendet, auf dem der Server läuft.

![Image](https://github.com/user-attachments/assets/b736cf07-8214-4cd3-a3b1-2c3bf803ba1a)

Hier wird bestätigt, dass jetzt ein Client (192.168.1.162) verbunden ist und der Client versendet daraufhin die Daten und Messwerte. Die Messwerte im Bild oben wurden bei Raumtemperatur gemessen.
Bei der Messung von Außentemperaturen sehen die Werte wie folgt aus:

![Image](https://github.com/user-attachments/assets/fcbed4c3-8ada-4c6b-bc60-e51f681a7cbd)

Die Außentemperatur betrug zu diesem Zeitpunkt weniger als 12°C, der Sensor braucht relativ lange um die Temperaturänderungen wahrzunehmen.
