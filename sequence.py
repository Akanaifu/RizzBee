from machine import Pin
import time
import random

# --- Configuration ---
ACTIVATION_DURATION = 0.375  # Durée d'activation d'une note (en secondes)
PAUSE_BETWEEN_NOTES = 0.1    # Petite pause entre deux notes
PAUSE_BETWEEN_SEQUENCES = 1.0

# --- Initialisation des solénoïdes ---
# L’ordre ici correspondra à : do, fa, si, ré, la
solenoids = {
    "do": Pin(2, Pin.OUT),   # bread verte
    "fa": Pin(4, Pin.OUT),   # bread bleue
    "si": Pin(5, Pin.OUT),   # grande bread far away
    "re": Pin(6, Pin.OUT),   # grande bread coté alim
    "la": Pin(7, Pin.OUT),   # bread rouge
}

# --- Définition des séquences de notes ---
sequence1 = [("do", 0.5), ("fa", 0.5), ("si", 0.5), ("re", 0.5), ("la", 0.5)]
sequence2 = [("do", 0.4), ("re", 0.4), ("fa", 0.4), ("la", 0.4), ("si", 0.6),
              ("la", 0.6), ("fa", 0.6), ("re", 0.6), ("do", 1.0)]
sequence3 = [("si", 0.3), ("do", 0.8), ("la", 0.4), ("re", 0.7), ("fa", 0.5),
              ("si", 0.6), ("fa", 0.3), ("la", 0.8), ("re", 0.4), ("do", 1.0)]

sequences = [sequence1, sequence2, sequence3]

# --- Fonction pour activer une note ---
def play_note(note, duration):
    pin = solenoids[note]
    pin.value(1)
    print(f"🎵 Activation : {note}")
    time.sleep(duration)
    pin.value(0)
    time.sleep(PAUSE_BETWEEN_NOTES)

# --- Fonction pour jouer une séquence complète ---
def play_sequence(sequence):
    for note, duration in sequence:
        play_note(note, duration)

# --- Boucle principale ---
try:
    print("🎹 Piano automatique en marche. Ctrl+C pour arrêter.")
    while True:
        seq = random.choice(sequences)     # Choisit une séquence au hasard
        play_sequence(seq)
        time.sleep(PAUSE_BETWEEN_SEQUENCES)

except KeyboardInterrupt:
    print("\nArrêt par l'utilisateur.")

finally:
    # Remet toutes les sorties à 0 pour sécurité
    for solenoid in solenoids.values():
        solenoid.value(0)
    print("Toutes les sorties ont été remises à 0.")

