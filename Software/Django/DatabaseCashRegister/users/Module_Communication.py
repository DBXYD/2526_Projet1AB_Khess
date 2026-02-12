import socket

def send_bluetooth_command(address, command):
    """
    Envoie une commande au périphérique Bluetooth via BLE.
    :param address: Adresse MAC du périphérique Bluetooth (HC-05 ou autre).
    :param command: Commande à envoyer (chaîne de caractères).
    :return: Réponse du périphérique (si disponible).
    """
    try:
        # Créer une socket Bluetooth RFCOMM
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        
        # Se connecter au périphérique
        sock.connect((address, 1))  # Le port 1 est généralement utilisé pour le HC-05
        print(f"Connecté à {address}")
        
        # Envoyer la commande
        sock.send(command.encode())
        print(f"Commande envoyée : {command}")
        
        # Lire une réponse (si nécessaire)
        response = ""
        n=0
        while n<15:
            n+=1
            data = sock.recv(1024).decode('utf-8')
            response += data
            if '\n' in data:  # Arrêter la lecture si le caractère de fin est détecté
                break
            
        
        # Fermer la connexion
        sock.close()
        
        return response
    except Exception as e:
        return f"Erreur : {e}"

if __name__ == "__main__":
    address = "98:D3:41:F6:FF:4F"  # Remplacez par l'adresse MAC de votre HC-05
    command = "Votrecomma"  # Remplacez par la commande que vous voulez envoyer
    response = send_bluetooth_command(address, command)
    print(response)
    
