import socket
import threading
from datetime import datetime

# Fungsi untuk mencatat log ke file
def log_to_file(log_message):
    with open('client.log', 'a') as log_file:
        log_file.write(f"{log_message}\n")

def receive_messages(client_socket):
    """Fungsi untuk menerima pesan dari server secara terus-menerus."""
    while True:
        try:
            start_receive_time = datetime.now()  # Catat waktu mulai menerima pesan
            response = client_socket.recv(1024).decode()
            end_receive_time = datetime.now()  # Catat waktu pesan diterima
            if not response:
                print("Koneksi terputus dari server.")
                break
            
            print(f"Pesan dari server: {response}")
            # Catat waktu penerimaan balasan ke log
            log_to_file(f"[{end_receive_time}] Respons diterima: {response} (waktu penerimaan: {end_receive_time - start_receive_time})")
        except Exception as e:
            print(f"Terjadi kesalahan saat menerima pesan: {e}")
            break

def start_client(server_host='192.168.56.1', server_port=50000):
    # Membuat socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect ke server
    start_connect_time = datetime.now()  # Catat waktu koneksi
    client_socket.connect((server_host, server_port))
    end_connect_time = datetime.now()  # Catat waktu koneksi selesai
    print(f"Terhubung ke server {server_host}:{server_port}")

    # Catat ke log
    log_to_file(f"[{start_connect_time}] Koneksi dibuka ke server {server_host}:{server_port} (waktu koneksi: {end_connect_time - start_connect_time})")

    # Thread untuk menerima pesan dari server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        while True:
            # Mengirim pesan ke server
            message = input("Masukkan pesan untuk server (ketik 'exit' untuk keluar): ")
            if message.lower() == 'exit':
                print("Keluar dari program...")
                break

            start_send_time = datetime.now()  # Catat waktu pengiriman pesan
            client_socket.send(message.encode())
            end_send_time = datetime.now()  # Catat waktu setelah pesan dikirim

            # Catat pengiriman pesan ke log
            log_to_file(f"[{start_send_time}] Pesan dikirim: {message} (waktu pengiriman: {end_send_time - start_send_time})")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup koneksi
        client_socket.close()
        log_to_file(f"[{datetime.now()}] Koneksi ditutup.")

if __name__ == "__main__":
    start_client()
