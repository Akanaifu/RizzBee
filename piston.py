import RPi.GPIO as GPIO
import time

# --- Configuration ---
# SOLENOID_PINS = [26, 19, 13, 6, 5]  # GPIO utilisés (modifier la liste si nécessaire)
SOLENOID_PINS = [26, 19, 13]  # GPIO utilisés (modifier la liste si nécessaire)

ACTIVATION_DURATION = 0.25  # Durée d'activation en secondes

# --- Initialisation ---
GPIO.setmode(GPIO.BCM)
for pin in SOLENOID_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


# --- Activation des solénoïdes ---
try:
    while True:
        # Activer tous les solénoïdes en même temps
        for pin in SOLENOID_PINS:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(ACTIVATION_DURATION)
            GPIO.output(pin, GPIO.LOW)

        break

except KeyboardInterrupt:
    print("Arrêt par l'utilisateur.")

finally:
    GPIO.cleanup()

