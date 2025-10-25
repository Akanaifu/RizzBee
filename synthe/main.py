from machine import Pin, I2S
import array, ustruct

# Configuration des pins I2S
bclk_pin = Pin(18)
lrclk_pin = Pin(19)
data_pin = Pin(20)

# Initialisation de la sortie audio I2S
audio_out = I2S(
    0,
    sck=bclk_pin,
    ws=lrclk_pin,
    sd=data_pin,
    mode=I2S.TX,
    bits=16,
    format=I2S.STEREO,
    rate=22050,
    ibuf=1024
)

# Ouvrir le fichier WAV
with open("Ivory_Tower.wav", "rb") as wav_file:
    # Sauter l'entête WAV (44 octets)
    wav_file.seek(44)
    
    # Taille du buffer
    buffer_size = 512
    buffer = array.array("h", [0] * buffer_size * 2)  # Stéréo, donc *2
    
    while True:
        # Lire un bloc de données
        raw_data = wav_file.read(buffer_size * 2 * 2)  # 2 octets par échantillon, 2 canaux
        if not raw_data:
            break
        
        # Convertir les données brutes en échantillons 16 bits
        for i in range(len(raw_data) // 2):
            sample = ustruct.unpack("<h", raw_data[2 * i:2 * i + 2])[0]
            buffer[2 * i] = sample  # Canal gauche
            buffer[2 * i + 1] = sample  # Canal droit
        
        # Écrire le buffer dans la sortie audio
        audio_out.write(buffer)

# Libérer les ressources
audio_out.deinit()