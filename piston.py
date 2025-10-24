import RPi.GPIO as GPIO
import time
from datetime import datetime

# --- Configuration ---
SOLENOID_PIN = 21            # GPIO utilisé
ACTIVATION_TIME = "14:30:00" # Heure d'activation (HH:MM:SS)
ACTIVATION_DURATION = 2      # Durée d'activation en secondes

# --- Initialisation ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOLENOID_PIN, GPIO.OUT)
GPIO.output(SOLENOID_PIN, GPIO.LOW)

try:
    print(f"Attente de l'heure d'activation ({ACTIVATION_TIME})...")

    while True:
        now = datetime.now().strftime("%H:%M:%S")
        if now == ACTIVATION_TIME:
            print("Activation du solénoïde...")
            GPIO.output(SOLENOID_PIN, GPIO.HIGH)
            time.sleep(ACTIVATION_DURATION)
            GPIO.output(SOLENOID_PIN, GPIO.LOW)
            print("Solénoïde désactivé.")
            break
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Arrêt par l'utilisateur.")

finally:
    GPIO.cleanup()
