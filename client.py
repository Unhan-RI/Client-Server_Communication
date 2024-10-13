import socket
import threading

def receive_messages(client_socket):
    """Fungsi untuk menerima pesan dari server secara terus-menerus."""
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                print("Koneksi terputus dari server.")
                break
            print(f"Pesan dari server: {response}")
        except Exception as e:
            print(f"Terjadi kesalahan saat menerima pesan: {e}")
            break

def start_client(server_host='192.168.56.1', server_port=50000):
    # Membuat socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect ke server
    client_socket.connect((server_host, server_port))
    print(f"Terhubung ke server {server_host}:{server_port}")

    # Thread untuk menerima pesan dari server
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    try:
        while True:
            # Mengirim pesan ke server
            message = input("Masukkan pesan untuk server (ketik 'exit' untuk keluar): ")
            if message.lower() == 'exit':
                print("Keluar dari program...")
                break

            client_socket.send(message.encode())
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup koneksi
        client_socket.close()

if __name__ == "__main__":
    start_client()
