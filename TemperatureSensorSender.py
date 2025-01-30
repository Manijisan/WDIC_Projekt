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
