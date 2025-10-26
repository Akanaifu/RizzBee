from machine import Pin
import time

# --- Configuration ---
# Tout fonctionnels
ACTIVATION_DURATION = 0.375  # Durée d'activation

# --- Initialisation ---
solenoids = [
    Pin(2, Pin.OUT),  # bread verte
    Pin(4, Pin.OUT),  # bread bleue
    Pin(5, Pin.OUT),  # grande bread far away
    Pin(6, Pin.OUT),  # grande bread coté alim
    Pin(7, Pin.OUT),  # bread rouge
]

# --- Activation des solénoïdes ---
try:
    while True:
        # Activer les solénoïdes l’un après l’autre
        for solenoid in solenoids:
            solenoid.value(1)  # Activer
            print(f"activation solenoid {solenoid}")
            time.sleep(ACTIVATION_DURATION)  # Attendre
            solenoid.value(0)  # Désactiver

        break

except KeyboardInterrupt:
    print("Arrêt par l'utilisateur.")

finally:
    # Remet toutes les sorties à 0 pour sécurité
    for solenoid in solenoids:
        solenoid.value(0)
