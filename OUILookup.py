import subprocess
import getopt
import sys

# Redes
RED_HOST = "192.168.1.30"
MASK = "255.255.255.0"
# Operación entre RED_HOST y MASK (AND por cada octeto)
NET_ID = ".".join([str(i & j) for i, j in zip(map(int, RED_HOST.split(".")), map(int, MASK.split(".")))])
# Strings de respuesta
MISMA_RED = "MAC address: {mac}\nFabricante: {manufacturer}\n"
OTRA_RED = "Error: ip is outside the host network\n"
MAC_EN_BASE_DE_DATOS = "MAC address: {mac}\nFabricante: {manufacturer}\n"
AYUDA = """Use: ./OUILookup --ip <IP> | --mac <IP> | --arp | [--help]
--ip : IP del host a consultar.
--mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.
--arp: muestra los fabricantes de los host
disponibles en la tabla arp.
--help: muestra este mensaje y termina."""

# Base de datos parametrizada
db: dict = {
    NET_ID: {
        "mac": "ss:ss:ss:ss:ss:ss",
        "manufacturer": "Unknown"
    },
    RED_HOST: {
        "mac": "00:00:00:00:00:01",
        "manufacturer": "Apple, Inc",
    },
    "192.168.1.1": {
        "mac": "0a:bb:cd:01:50:aa",
        "manufacturer": "Cisco Systems, Inc"
    },
    "192.168.1.2": {
        "mac": "aa:bb:cc:dd:ee:ff",
        "manufacturer": "Netgear"
    },
    "192.162.1.3": {
        "mac": "",
        "manufacturer": "D-Link"
    },
    "192.168.1.4": {
        "mac": "dd:ee:ff:00:00:00",
        "manufacturer": "Huawei"
    },
    "192.168.1.5": {
        "mac": "ab:cd:ef:12:34:56",
        "manufacturer": "TP-Link"
    }
}

# Función para obtener los datos de fabricación de una tarjeta de red por IP
def obtener_datos_por_ip(ip: str) -> str:
    """
    Obtiene los datos de fabricación de una tarjeta de red por IP.
    
    Parámetros:
        ip : IP del host a consultar.
    
    Retorna:
        Datos de fabricación de la tarjeta de red o "Not found" si no se encuentra.
    """
    if ip in db:
        if "manufacturer" in db[ip]:
            return db[ip]["manufacturer"]
        else:
            return "Not found"
    else:
        return ""

# Función para obtener los datos de fabricación de una tarjeta de red por MAC
def obtener_datos_por_mac(mac: str) -> str:
    """
    Obtiene los datos de fabricación de una tarjeta de red por MAC.
    
    Parámetros:
        mac : MAC del host a consultar.
        
    Retorna:
        Datos de fabricación de la tarjeta de red o "Not found" si no se encuentra.
    """
    for ip, datos in db.items():
        if mac in datos["mac"]:
            return datos["manufacturer"]
        else:
            pass
    else:
        return "Not found"
    
def obtener_mac_por_ip(ip: str) -> str:
    """
    Obtiene la MAC de una tarjeta de red por IP.

    Parámetros:
        ip (str): IP del host a consultar.

    Retorna:
        MAC de la tarjeta de red o "Not found" si no se encuentra.
    """
    if ip in db:
        # Si la MAC no está vacía, retorna la MAC, de lo contrario retorna "Not found"
        if "mac" in db[ip]:
            return db[ip]["mac"]
        else:
            return "Not found"
    # Si la IP no está en la base de datos, retorna "Not found"
    else:
        return "Not found"

# Función para obtener la tabla ARP
def obtener_tabla_arp():
    """
    Obtiene la tabla ARP.
    
    Retorna:
        Texto con la tabla ARP.
    """
    tabla_arp = f"IP\t\t/\tMAC\t\t\t/\tVENDOR\n"
    for ip, datos in db.items():
        # Si la MAC no está vacía, se agrega a la tabla (ya que si está vacía, no se conoce la MAC y por ende aún no se ha hecho ARP)
        if datos["mac"] != "":
            tabla_arp += f"{ip}\t/\t{obtener_mac_por_ip(ip)}\t/\t{obtener_datos_por_ip(ip)}\n"
    return tabla_arp


def main(argv):
    ip = None

    try:
        opts, args = getopt.getopt(argv, "i:", ["ip=", "mac=", "arp", "help"])

    except getopt.GetoptError:
        #Modificar para coincidir con tarea
        print("Use: python OUILookup.py --ip <IP> | --Arg2 <Arg2> | --Arg3 | [--help] \n --ip : IP del host a consultar. \n --Arg2:  \n --Atg3: \n --help:")
        sys.exit(2)
        
    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            if arg in db:
                print(MISMA_RED.format(mac=obtener_mac_por_ip(arg), manufacturer=obtener_datos_por_ip(arg)))
            else:
                print(OTRA_RED)
        elif opt in ("--mac"):
            print(MAC_EN_BASE_DE_DATOS.format(mac=arg, manufacturer=obtener_datos_por_mac(arg)))
        elif opt in ("--arp"):
            print(obtener_tabla_arp())
        elif opt in ("--help"):
            print(AYUDA)
        else:
            print("Debe proporcionar una opción válida (-i, -m o -a).")
            sys.exit(2)
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])