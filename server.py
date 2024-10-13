import socket
import threading
from datetime import datetime

# Fungsi untuk log dengan timestamp
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# Fungsi untuk menangani klien yang terhubung
def handle_client(conn, addr):
    log_message(f"Koneksi diterima dari {addr}")
    
    conn.settimeout(60)  # Set timeout untuk 60 detik

    try:
        while True:
            try:
                data = conn.recv(1024).decode()  # Terima pesan dari client
                if not data:
                    break
                log_message(f"Pesan dari {addr}: {data}")
                
                # Kirim balasan ke client
                response = "Pesan diterima oleh server"
                conn.send(response.encode())  # Balasan ke client
                log_message(f"Balasan ke {addr}: {response}")

            except socket.timeout:
                log_message(f"Koneksi dengan {addr} tidak aktif, menunggu pesan...")
                continue  # Jika timeout terjadi, teruskan menunggu pesan

    except Exception as e:
        log_message(f"Terjadi kesalahan dengan {addr}: {e}")
    finally:
        log_message(f"Koneksi dengan {addr} ditutup")
        conn.close()

# Fungsi untuk memulai server
def start_server(host='192.168.56.1', port=50001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Maksimum 5 klien dalam antrean
    log_message(f"Server dimulai di {host}:{port}, menunggu koneksi...")

    clients = []  # Daftar untuk menyimpan koneksi klien

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)  # Simpan koneksi klien
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

        # Jalankan thread untuk mendengarkan input dari operator server
        threading.Thread(target=send_message_to_clients, args=(clients,), daemon=True).start()

# Fungsi untuk mengirim pesan dari server ke semua klien
def send_message_to_clients(clients):
    while True:
        message = input("Masukkan pesan untuk semua klien: ")  # Operator server memasukkan pesan
        for client in clients:
            try:
                client.send(message.encode())  # Kirim pesan ke klien
                log_message(f"Pesan '{message}' dikirim ke klien")
            except Exception as e:
                log_message(f"Error mengirim pesan ke klien: {e}")

if __name__ == "__main__":
    start_server()
