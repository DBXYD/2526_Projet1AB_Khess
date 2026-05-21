"""
Communication Bluetooth RFCOMM avec le matériel de la KFET.
Le module envoie une commande texte au HC-05 puis récupère une réponse éventuelle.
"""
import socket


def send_bluetooth_command(address, command):
    """
    Envoie une commande texte à un périphérique Bluetooth RFCOMM.

    :param address: Adresse MAC du périphérique.
    :param command: Commande à envoyer.
    :return: Réponse du périphérique, ou message d'erreur lisible.
    """
    sock = None
    try:
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        sock.settimeout(5.0)

        # Le HC-05 utilise généralement le canal 1.
        sock.connect((address, 1))
        sock.sendall(command.encode('utf-8'))

        response = ""
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break

                decoded = data.decode('utf-8', errors='replace')
                response += decoded

                if '\n' in decoded:
                    break
            except socket.timeout:
                break

        return response.strip() if response.strip() else "Envoyé"

    except Exception as e:
        return f"Erreur Bluetooth : {e}"

    finally:
        if sock:
            sock.close()
'''
"""
Ce module est indépendant de Django. Son seul rôle est de parler avec 
le matériel physique de la KFET (le module Bluetooth HC-05 connecté à un Arduino/Raspberry).
"""
import socket

def send_bluetooth_command(address, command):
    """
    Ouvre une connexion sans fil, envoie un texte, et referme la connexion.

    :param address: Adresse MAC du périphérique Bluetooth (HC-05 ou autre).
    :param command: Commande à envoyer (chaîne de caractères).
    :return: Réponse du périphérique (si disponible).
    """
    sock = None
    try:
        # Création d'une "prise" virtuelle pour le Bluetooth (RFCOMM)
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        
        # SÉCURITÉ : limite de temps (5 secondes)
        sock.settimeout(5.0) 
        
        # Connexion à l'adresse MAC sur le canal 1
        sock.connect((address, 1))
        print(f"Connecté à {address}")
        
        # Envoi de la commande
        sock.send(command.encode())
        print(f"Commande envoyée : {command}")

        # Lecture de la réponse
        response = ""
        n = 0
        while n < 15:
            n += 1
            try:
                data = sock.recv(1024).decode('utf-8')
                response += data
                if '\n' in data:  # Fin de message
                    break
            except socket.timeout:
                # Pas de réponse dans le délai
                break
        
        return response if response else "Envoyé (pas de réponse du matériel)"

    except Exception as e:
        return f"Erreur Bluetooth : {e}"

    finally:
        # Fermeture propre de la connexion
        if sock:
            sock.close()


if __name__ == "__main__":
    address = "98:D3:41:F6:FF:4F"  # Remplacez par l'adresse MAC de votre HC-05
    command = "Votrecomma"         # Remplacez par la commande à envoyer

    response = send_bluetooth_command(address, command)
    print(response)


"""
Ce module est indépendant de Django. Son seul rôle est de parler avec 
le matériel physique de la KFET (le module Bluetooth HC-05 connecté à un Arduino/Raspberry).
"""
import socket

def send_bluetooth_command(address, command):
    """
    Ouvre une connexion sans fil, envoie un texte, et referme la connexion.
    """
        """
    Envoie une commande au périphérique Bluetooth via BLE.
    :param address: Adresse MAC du périphérique Bluetooth (HC-05 ou autre).
    :param command: Commande à envoyer (chaîne de caractères).
    :return: Réponse du périphérique (si disponible).
    """
    try:
        # Création d'une "prise" virtuelle pour le Bluetooth (RFCOMM)
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        
        # SÉCURITÉ : On impose une limite de temps (5 secondes). 
        # Si le module Bluetooth est éteint, le site web n'attendra pas à l'infini et ne plantera pas.
        sock.settimeout(5.0) 
        
        # On se connecte à l'adresse MAC fournie, sur le canal 1
        sock.connect((address, 1))
        print(f"Connecté à {address}")
        
        # On encode le texte en "octets" pour qu'il puisse voyager dans les ondes, puis on l'envoie.
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

        try:
            # On écoute pour voir si l'Arduino nous répond "OK"
            response = sock.recv(1024).decode('utf-8')
        except socket.timeout:
            # Si l'Arduino ne répond pas assez vite, on considère que c'est envoyé quand même.
            response = "Envoyé (pas de réponse du matériel)"
            
        sock.close() # On coupe la communication proprement
        return response
        
    except Exception as e:
        # Si le Bluetooth est éteint ou hors de portée, on renvoie une erreur lisible.
        return f"Erreur Bluetooth : {str(e)}"
        return f"Erreur : {e}"
    
if __name__ == "__main__":
    address = "98:D3:41:F6:FF:4F" # Remplacez par l'adresse MAC de votre HC-05
    command = "Votrecomma" # Remplacez par la commande que vous voulez envoyer
    response = send_bluetooth_command(address, command)
    print(response)

    '''