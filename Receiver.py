import socket
 
def start_server(host='192.168.1.102', port=5000):
    """Startet einen Server, der Daten über WLAN empfängt."""
   
    # Erstelle einen TCP/IP-Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
   
    print(f"Server gestartet auf {host}:{port}")
   
    while True:
        # Warte auf eine Verbindung
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