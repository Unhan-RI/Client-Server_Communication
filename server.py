import socket
import threading
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def handle_client(conn, addr):
    log_message(f"Koneksi diterima dari {addr}")
    
    conn.settimeout(60)  # Set timeout untuk 60 detik

    try:
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                log_message(f"Pesan dari {addr}: {data}")
                
                # Kirim balasan ke klien
                conn.send("Pesan diterima oleh server".encode())
            except socket.timeout:
                log_message(f"Koneksi dengan {addr} tidak aktif, menunggu pesan...")
                continue  # Jika timeout terjadi, teruskan menunggu pesan
    except Exception as e:
        log_message(f"Terjadi kesalahan dengan {addr}: {e}")
    finally:
        log_message(f"Koneksi dengan {addr} ditutup")
        conn.close()

def start_server(host='192.168.137.226', port=50001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    log_message(f"Server dimulai di {host}:{port}, menunggu koneksi...")

    clients = []  # Daftar untuk menyimpan koneksi klien

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)  # Simpan koneksi klien
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

        # Thread untuk mendengarkan input dari operator
        threading.Thread(target=send_message_to_clients, args=(clients,)).start()

def send_message_to_clients(clients):
    while True:
        message = input("Masukkan pesan untuk semua klien: ")
        for client in clients:
            try:
                client.send(message.encode())
            except Exception as e:
                log_message(f"Error mengirim pesan ke klien: {e}")

if __name__ == "__main__":
    start_server()
