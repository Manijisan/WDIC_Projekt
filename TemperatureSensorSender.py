import adafruit_dht
import board
import socket
import time

# Sensor setup
sensor = adafruit_dht.DHT11(board.D4)

# Configure server details
SERVER_IP = "192.168.1.102"  # Replace with your friend's Raspberry Pi IP
PORT = 5000  # Same port as in the server script

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

while True:
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        data = f"Temperature: {temperature}C, Humidity: {humidity}%"
        print("Sending:", data)
        
        client_socket.sendall(data.encode())  # Send data

    except RuntimeError as error:
        print("Error:", error.args[0])
    
    time.sleep(2)  # Send data every 2 seconds

client_socket.close()
