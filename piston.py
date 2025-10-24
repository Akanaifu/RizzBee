import RPi.GPIO as GPIO
import time

# --- Configuration ---
SOLENOID_PINS = [26, 19, 13, 6, 5]  # GPIO utilisés (modifier la liste si nécessaire)

ACTIVATION_DURATION = 1  # Durée d'activation en secondes

# --- Initialisation ---
GPIO.setmode(GPIO.BCM)
for pin in SOLENOID_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


# --- Activation des solénoïdes ---
try:
    while True:
        print("Activation des solénoïdes...")
        # Activer tous les solénoïdes en même temps
        for pin in SOLENOID_PINS:
            GPIO.output(pin, GPIO.HIGH)

        time.sleep(ACTIVATION_DURATION)

        # Désactiver tous les solénoïdes
        for pin in SOLENOID_PINS:
            GPIO.output(pin, GPIO.LOW)

        print("Solénoïdes désactivés.")
        break

except KeyboardInterrupt:
    print("Arrêt par l'utilisateur.")

finally:
    GPIO.cleanup()
