from machine import Pin, I2S
import array, ustruct, utime

# -------------------
# CONFIGURATION I2S
# -------------------
bclk_pin = Pin(18)   # Bit Clock
lrclk_pin = Pin(19)  # Word Select / LRCLK
data_pin = Pin(20)   # Serial Data

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

# -------------------
# FICHIER WAV
# -------------------
filename = "Ivory_Tower.wav"  # Nom exact du fichier sur le Pico

try:
    with open(filename, "rb") as wav_file:
        # Sauter l'en-tête WAV standard (44 octets)
        wav_file.seek(44)

        buffer_size = 512
        buffer = array.array("h", [0]*buffer_size*2)  # *2 pour stéréo

        while True:
            raw_data = wav_file.read(buffer_size*2*2)  # 2 octets par échantillon, stéréo
            if not raw_data:
                break

            # Conversion bytes → signed 16-bit
            for i in range(len(raw_data)//2):
                val = ustruct.unpack("<h", raw_data[2*i:2*i+2])[0]
                buffer[2*i] = val       # Canal gauche
                buffer[2*i+1] = val     # Canal droit

            audio_out.write(buffer)

    print("Lecture WAV terminée !")

except OSError:
    print("Fichier WAV introuvable. Check le nom et l'emplacement.")

finally:
    audio_out.deinit()