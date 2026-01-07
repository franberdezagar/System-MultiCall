# WordPress XML-RPC Multicall Exploit

Script de ataque de fuerza bruta contra WordPress utilizando el método XML-RPC `system.multicall`.

## Características

- 🎯 Ataque XML-RPC multicall contra WordPress
- ⚙️ Configuración interactiva de parámetros
- 📊 Selección de tamaño de lote (100, 200, 300, 400, 500 passwords)
- 🎨 Interfaz colorida y amigable
- 📝 Registro de resultados exitosos
- ⏸️ Soporte para interrumpir con Ctrl+C

## Requisitos

- Python 3.7+
- Módulos: `requests`, `colorama`

## Instalación

```bash
git clone <repository-url>
cd System-MultiCall
pip install -r requirements.txt
```

## Uso

```bash
python System-MultiCall.py
```

El script te pedirá:

1. **URL del target** - La URL de xmlrpc.php (ej: https://example.com/xmlrpc.php)
2. **Nombre de usuario** - El usuario a atacar
3. **Ruta del diccionario** - Archivo con lista de passwords
4. **Tamaño del lote** - Cantidad de passwords por solicitud (100, 200, 300, 400, 500)

## Ejemplos

```bash
$ python System-MultiCall.py

 ██╗    ██╗ ██████╗ ██████╗ ██████╗ ██████╗ ███████╗███████╗███████╗
 ██║    ██║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔════╝
 ██║ █╗ ██║██║   ██║██████╔╝██████╔╝██████╔╝███████╗███████╗███████╗
 ██║███╗██║██║   ██║██╔══██╗██╔═══╝ ██╔══██╗╚════██║╚════██║╚════██║
 ╚███╔███╝╚██████╔╝██║  ██║██║     ██║  ██║███████║███████║███████║
  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝

 ╔═══════════════════════════════════════════════════════════════╗
 ║     XML-RPC MULTI-CALL ATTACK SYSTEM v1.0                     ║                                                      
 ║      WordPress Brute Force Exploitation Tool                  ║                       
 ╠═══════════════════════════════════════════════════════════════╣
 ║  ⚡ Created by: b3rd3                                          ║                           
 ║  🔓 Attack Type: XML-RPC System.Multicall                     ║             
 ║  ⚙️  Method: Parallel Password Batching                       ║
 ╚═══════════════════════════════════════════════════════════════╝                  
    

[+] Ingresa la URL target: https://mywordpress.com/xmlrpc.php
[+] Ingresa el nombre de usuario: admin
[+] Ingresa la ruta del diccionario: /path/to/wordlist.txt
[*] Elige el tamaño del lote:
    1. 100 passwords por lote
    2. 200 passwords por lote
    3. 300 passwords por lote
    4. 400 passwords por lote
    5. 500 passwords por lote

[+] Selecciona una opción (1-5): 2
```

## Salida

Si encuentra credenciales válidas, creará un archivo `resultado_exitoso.txt` con:
- Usuario encontrado
- Password encontrado
- Respuesta completa del servidor

## Advertencia

⚠️ **USO EDUCATIVO ÚNICAMENTE** - Este script está diseñado para pruebas autorizadas en tus propios servidores o con permiso explícito. Su uso no autorizado es ilegal.

## Licencia

MIT

## Autor

Sistema de Ataque XML-RPC WordPress
