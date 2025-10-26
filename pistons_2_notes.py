from machine import Pin
import time
import random

# --- Configuration ---
ACTIVATION_DURATION = 0.375  # Durée d'activation d'une note (en secondes)
PAUSE_BETWEEN_NOTES = 0.1  # Petite pause entre deux notes
PAUSE_BETWEEN_SEQUENCES = 1.0

# --- Initialisation des solénoïdes ---
# L’ordre ici correspondra à : do, fa, si, ré, la
solenoids = {
    "do": Pin(2, Pin.OUT),  # bread verte
    "fa": Pin(4, Pin.OUT),  # bread bleue
    "si": Pin(5, Pin.OUT),  # grande bread far away
    "re": Pin(6, Pin.OUT),  # grande bread coté alim
    "la": Pin(7, Pin.OUT),  # bread rouge
}

# --- Définition des séquences de notes ---
sequence1 = [[("do", 0.5)], [("fa", 0.5)], [("si", 0.5)], [("re", 0.5)], [("la", 0.5)]]
sequence2 = [
    [("do", 0.4)],
    [("re", 0.4)],
    [("fa", 0.4)],
    [("la", 0.4)],
    [("si", 0.6)],
    [("la", 0.6)],
    [("fa", 0.6)],
    [("re", 0.6)],
    [("do", 1.0)],
]
sequence3 = [
    [("si", 0.3)],
    [("do", 0.8)],
    [("la", 0.4)],
    [("re", 0.7)],
    [("fa", 0.5)],
    [("si", 0.6)],
    [("fa", 0.3)],
    [("la", 0.8)],
    [("re", 0.4)],
    [("do", 1.0)],
]

seq_rand = [
    [("si", 0.3), ("do", 0.8)],
    [("do", 0.8), ("la", 0.4)],
    [("la", 0.4), ("re", 0.7)],
    [("re", 0.7), ("fa", 0.5)],
    [("fa", 0.5), ("si", 0.6)],
    [("si", 0.6), ("fa", 0.3)],
    [("la", 0.8), ("re", 0.4)],
    [("re", 0.4), ("do", 1.0)],
]

sequences = [sequence1, sequence2, sequence3]


# --- Fonction pour activer une note ---
def play_note(note, duration):
    pin = solenoids[note]
    pin.value(1)
    print(f"🎵 Activation : {note}")
    time.sleep(duration)
    pin.value(0)
    time.sleep(PAUSE_BETWEEN_NOTES)


def play_2_notes(notes):
    note1, note2 = notes
    duration1 = note1[1]
    duration2 = note2[1]
    pin1 = solenoids[note1[0]]
    pin2 = solenoids[note2[0]]
    pin1.value(1)
    pin2.value(1)
    print(f"🎵 Activation simultanée : {note1[0]} et {note2[0]}")
    time.sleep(max(duration1, duration2))
    pin1.value(0)
    pin2.value(0)
    time.sleep(PAUSE_BETWEEN_NOTES)


# --- Fonction pour jouer une séquence complète ---
def play_sequence(sequence):
    for notes in sequence:
        if len(notes) == 1:
            play_note(notes[0][0], notes[0][1])
        elif len(notes) == 2:
            play_2_notes(notes)


def full_sequence_random():
    """
    crée et joue une séquence complète ou tout est aléatoire.
    Le nombre de note jouée est aussi aléatoire. Deux notes peuvent être jouées en même temps.
    """
    print("full random")
    sequence = []
    keys = list(solenoids.keys())
    num_notes = random.randint(5, 15)  # Nombre aléatoire de notes dans la séquence
    for _ in range(num_notes):
        if random.choice([True, False]):
            # Jouer une note simple
            note = random.choice(keys)
            duration = 0.3 + (random.random() * 0.7)
            sequence.append([(note, duration)])
        else:
            # Jouer deux notes simultanément
            note1 = random.choice(keys)
            note2 = random.choice(keys)
            while note2 == note1:
                note2 = random.choice(keys)
            duration1 = 0.3 + (random.random() * 0.7)
            duration2 = 0.3 + (random.random() * 0.7)
            sequence.append([(note1, duration1), (note2, duration2)])
        play_sequence(sequence)


if __name__ == "__main__":
    # --- Boucle principale ---
    try:
        #         print("Piano automatique en marche. Ctrl+C pour arrêter.")
        #         full_sequence_random()
        while True:
            seq = random.choice(sequences)  # Choisit une séquence au hasard
            play_sequence(seq)
            time.sleep(PAUSE_BETWEEN_SEQUENCES)

    except KeyboardInterrupt:
        print("\nArrêt par l'utilisateur.")

    finally:
        # Remet toutes les sorties à 0 pour sécurité
        for solenoid in solenoids.values():
            solenoid.value(0)
        print("Toutes les sorties ont été remises à 0.")
