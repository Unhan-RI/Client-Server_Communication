import socket
import threading
from datetime import datetime

# Fungsi untuk mencatat log dengan timestamp ke terminal dan file log
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)  # Cetak ke terminal

    # Simpan log ke file client.log
    with open("client.log", "a") as log_file:
        log_file.write(log_entry + "\n")

def start_client(load_balancer_host='192.168.56.3', load_balancer_port=50000):
    # Membuat socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mengukur waktu koneksi
    start_time = datetime.now()
    client_socket.connect((load_balancer_host, load_balancer_port))
    end_time = datetime.now()
    connection_time = (end_time - start_time).total_seconds()

    log_message(f"Terhubung ke load balancer {load_balancer_host}:{load_balancer_port}")
    log_message(f"Waktu koneksi: {connection_time:.4f} detik")


def receive_messages(client_socket, send_start, message_size):
    """Fungsi untuk menerima pesan dari server dan menghitung metrik."""
    try:
        # Terima pesan dari server dan hitung waktu respons
        response = client_socket.recv(1024).decode()
        if not response:
            log_message("Koneksi terputus dari server.")
            return None

        # Catat waktu saat respons diterima
        receive_time = datetime.now()
        response_time = (receive_time - send_start).total_seconds()

        # Hitung latency sebagai setengah dari waktu respons
        latency = response_time / 2

        # Hitung throughput sebagai ukuran pesan dibagi dengan waktu respons (byte/detik)
        if response_time > 0:
            throughput = message_size / response_time
        else:
            throughput = 0

        # Log waktu respons, latency, dan throughput
        log_message(f"Pesan dari server: {response}")
        log_message(f"Waktu respon: {response_time:.4f} detik")
        log_message(f"Latency: {latency:.4f} detik")
        log_message(f"Throughput: {throughput:.4f} byte/detik")

        return response_time
    except Exception as e:
        log_message(f"Terjadi kesalahan saat menerima pesan: {e}")
        return None

def start_client(server_host='192.168.56.1', server_port=50001):
    # Membuat socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mengukur waktu koneksi
    start_time = datetime.now()
    client_socket.connect((server_host, server_port))
    end_time = datetime.now()
    connection_time = (end_time - start_time).total_seconds()

    log_message(f"Terhubung ke server {server_host}:{server_port}")
    log_message(f"Waktu koneksi: {connection_time:.4f} detik")

    try:
        while True:
            # Mengirim pesan ke server
            message = input("Masukkan pesan untuk server (ketik 'exit' untuk keluar): ")
            if message.lower() == 'exit':
                log_message("Keluar dari program...")
                break

            # Hitung ukuran pesan untuk throughput (dalam byte)
            message_size = len(message.encode())

            # Catat waktu pengiriman
            send_start = datetime.now()
            client_socket.send(message.encode())

            # Terima respons dari server dan catat waktu respons, latency, throughput
            receive_messages(client_socket, send_start, message_size)

    except Exception as e:
        log_message(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup koneksi
        client_socket.close()

if __name__ == "__main__":
    start_client()
