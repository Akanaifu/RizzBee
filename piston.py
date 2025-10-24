import RPi.GPIO as GPIO


# --- Configuration ---
SOLENOID_PIN = 26  # GPIO utilisé
ACTIVATION_DURATION = 1  # Durée d'activation en secondes

# --- Initialisation ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOLENOID_PIN, GPIO.OUT)
GPIO.output(SOLENOID_PIN, GPIO.LOW)

try:
    print(f"Attente de l'heure d'activation ({ACTIVATION_TIME})...")

    while True:
        print("Activation du solénoïde...")
        GPIO.output(SOLENOID_PIN, GPIO.HIGH)
        time.sleep(ACTIVATION_DURATION)
        GPIO.output(SOLENOID_PIN, GPIO.LOW)
        print("Solénoïde désactivé.")
        break


except KeyboardInterrupt:
    print("Arrêt par l'utilisateur.")

finally:
    GPIO.cleanup()
