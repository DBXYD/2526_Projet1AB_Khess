"""
Lecture NFC via le module Elechouse PN532 V3 en mode UART (HSU).
Le module doit avoir ses dip-switches configurés sur HSU : SW1=1, SW2=0.
Branchement : GND→GND, VCC→3.3V ou 5V, TXD→RX du Raspberry/PC, RXD→TX du Raspberry/PC.

Dépendance : pip install pyserial
"""
import serial
import time

# --- Trames PN532 (protocole HSU) ---

# Commande Wake-up : réveille le module après une période d'inactivité
WAKEUP = bytes([0x55, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

# Commande GetFirmwareVersion : permet de tester si le module répond correctement
GET_FIRMWARE_VERSION = bytes([
    0x00, 0x00, 0xFF,  # Préambule
    0x02, 0xFE,        # Longueur + complément
    0xD4, 0x02,        # TFI + commande GetFirmwareVersion
    0x2A, 0x00         # Checksum + postambule
])

# Commande InListPassiveTarget : demande au module de chercher une carte RFID/NFC
# MaxTg=1 (1 carte max), BrTy=0x00 (ISO 14443A, format des cartes Mifare classiques)
IN_LIST_PASSIVE_TARGET = bytes([
    0x00, 0x00, 0xFF,  # Préambule
    0x04, 0xFC,        # Longueur (4 octets) + complément
    0xD4, 0x4A,        # TFI + commande InListPassiveTarget
    0x01, 0x00,        # MaxTg=1, BrTy=ISO14443A
    0xE1, 0x00         # Checksum + postambule
])


def _open_port(port: str, baudrate: int = 115200) -> serial.Serial:
    """Ouvre le port série avec les paramètres PN532."""
    return serial.Serial(
        port=port,
        baudrate=baudrate,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1.0
    )


def _send_and_receive(ser: serial.Serial, command: bytes, wait: float = 0.1) -> bytes:
    """Envoie une commande et lit la réponse brute."""
    ser.reset_input_buffer()
    ser.write(command)
    time.sleep(wait)
    return ser.read(ser.in_waiting or 64)


def test_connection(port: str = '/dev/ttyUSB0', baudrate: int = 115200) -> bool:
    """
    Vérifie que le module PN532 répond.
    Retourne True si le firmware est détecté, False sinon.

    :param port: Port série (ex: '/dev/ttyUSB0' sur Linux, 'COM3' sur Windows)
    :param baudrate: Vitesse (115200 par défaut pour le PN532 en HSU)
    """
    try:
        with _open_port(port, baudrate) as ser:
            ser.write(WAKEUP)
            time.sleep(0.1)
            response = _send_and_receive(ser, GET_FIRMWARE_VERSION, wait=0.2)
            # La réponse valide contient 0xD5, 0x03 (réponse GetFirmwareVersion)
            return b'\xD5\x03' in response
    except Exception as e:
        return False


def read_nfc_uid(port: str = '/dev/ttyUSB0', baudrate: int = 115200, timeout: float = 5.0) -> str | None:
    """
    Attend qu'une carte NFC/RFID soit présentée et retourne son UID (identifiant unique).

    :param port: Port série du module (ex: '/dev/ttyUSB0')
    :param baudrate: Vitesse de communication (115200 par défaut)
    :param timeout: Durée max d'attente en secondes (default: 5s)
    :return: UID de la carte sous forme de chaîne hex (ex: "A3:F2:01:BC") ou None si timeout/erreur
    """
    try:
        with _open_port(port, baudrate) as ser:
            # Réveil du module
            ser.write(WAKEUP)
            time.sleep(0.1)

            deadline = time.time() + timeout

            while time.time() < deadline:
                response = _send_and_receive(ser, IN_LIST_PASSIVE_TARGET, wait=0.15)

                # Analyse de la réponse InListPassiveTarget (0xD5, 0x4B)
                # Format : ... 0xD5 0x4B NbTg Tg ATQA[2] SAK UID_Len UID[n] ...
                if b'\xD5\x4B' in response:
                    idx = response.index(b'\xD5\x4B')
                    # NbTg est à idx+2 : nombre de cartes trouvées
                    if len(response) > idx + 2 and response[idx + 2] >= 1:
                        # UID_Len est à idx+7, UID commence à idx+8
                        if len(response) > idx + 7:
                            uid_length = response[idx + 7]
                            uid_start = idx + 8
                            uid_end = uid_start + uid_length

                            if len(response) >= uid_end:
                                uid_bytes = response[uid_start:uid_end]
                                uid_str = ':'.join(f'{b:02X}' for b in uid_bytes)
                                return uid_str

                time.sleep(0.3)

        return None  # Timeout dépassé sans carte détectée

    except serial.SerialException as e:
        raise ConnectionError(f"Impossible d'ouvrir le port {port} : {e}")
    except Exception as e:
        raise RuntimeError(f"Erreur NFC inattendue : {e}")


def read_nfc_uid_once(port: str = '/dev/ttyUSB0', baudrate: int = 115200) -> str | None:
    """
    Tente une seule lecture NFC (pas de boucle d'attente).
    Utile pour les appels Ajax depuis Django.

    :return: UID string ou None
    """
    return read_nfc_uid(port=port, baudrate=baudrate, timeout=2.0)
