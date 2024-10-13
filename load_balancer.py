import socket
import threading

# Daftar server yang tersedia
servers = [('192.168.56.1', 50001), ('192.168.56.1', 50002)]

def handle_client(client_socket):
    """Fungsi untuk mengarahkan permintaan ke server yang tersedia."""
    server_index = 0
    while True:
        try:
            # Menerima data dari client
            request = client_socket.recv(1024)
            if not request:
                print("Tidak ada data dari client, menutup koneksi.")
                break  # Jika tidak ada data, keluar
            
            # Menggunakan round-robin untuk memilih server
            server_address = servers[server_index]

            # Membuat socket server baru untuk menghubungkan ke server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect(server_address)

                print(f"Menerima permintaan dari client: {request.decode()}")
                
                # Kirim permintaan ke server
                server_socket.send(request)

                # Terima respons dari server
                response = server_socket.recv(1024)
                print(f"Menerima respons dari server: {response.decode()}")
                
                # Kirim kembali respons ke client
                client_socket.send(response)
                
                # Pindah ke server berikutnya untuk permintaan berikutnya
                server_index = (server_index + 1) % len(servers)

        except socket.error as e:
            print(f"Terjadi kesalahan socket: {e}")
            break
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")
            break

    client_socket.close()  # Tutup koneksi klien setelah loop berakhir

def start_load_balancer(host='0.0.0.0', port=50000):
    """Fungsi untuk memulai load balancer."""
    load_balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    load_balancer_socket.bind((host, port))
    load_balancer_socket.listen(5)
    print(f"Load balancer dimulai di {host}:{port}, menunggu koneksi...")

    while True:
        client_socket, addr = load_balancer_socket.accept()
        print(f"Koneksi diterima dari {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_load_balancer()
