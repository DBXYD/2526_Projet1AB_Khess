import time
from gpiozero import OutputDevice

GPIO_PIN = 17

# 2. Initialisation de la broche de contrôle
# active_high=True signifie qu'un signal 3.3V active le MOSFET
tiroir_caisse = OutputDevice(GPIO_PIN, active_high=True, initial_value=False)

def ouvrir_tiroir():
    print("Envoi du signal d'ouverture...")
    
    # Active le GPIO (Envoie du 3.3V au MOSFET)
    tiroir_caisse.on()

    time.sleep(0.2) 
    
    # Désactive le GPIO (Retour à 0V)
    tiroir_caisse.off()
    
    print("Tiroir-caisse déverrouillé avec succès.")

if __name__ == "__main__":
    ouvrir_tiroir()