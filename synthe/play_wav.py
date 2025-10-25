from machine import Pin, I2S
from rp2 import PIO, StateMachine, asm_pio
import os, array, ustruct

# Pins (adapter si besoin)
BCLK, WS, SD, MCLK = 18, 19, 20, 21
FILENAME = "/piano.wav"   # ton WAV PCM 16-bit LE (stéréo/mono), 24 kHz ici

@asm_pio(sideset_init=PIO.OUT_LOW)
def mclk_prog():
    wrap_target()
    nop().side(1)
    nop().side(0)
    wrap()

def start_mclk(freq_hz):
    # 2 instructions par période -> sortie = sm.freq / 2
    sm = StateMachine(0, mclk_prog, freq=freq_hz*2, sideset_base=Pin(MCLK))
    sm.active(1)
    return sm

def parse_wav(f):
    h = f.read(12)
    if len(h) < 12 or h[:4] != b"RIFF" or h[8:12] != b"WAVE":
        raise ValueError("WAV invalide (RIFF/WAVE)")
    fmt = None; data_ofs = None; data_size = None
    while True:
        hdr = f.read(8)
        if len(hdr) < 8: break
        ck, size = ustruct.unpack("<4sI", hdr)
        if ck == b"fmt ":
            fmt = f.read(size)
        elif ck == b"data":
            data_ofs = f.tell()
            data_size = size
            f.seek(size, 1)
        else:
            f.seek(size, 1)
        if size & 1: f.seek(1, 1)
    if not fmt or data_ofs is None:
        raise ValueError("Chunks fmt/data manquants")
    audio_fmt, nch, rate, _, _, bps = ustruct.unpack("<HHIIHH", fmt[:16])
    if audio_fmt != 1 or bps != 16:
        raise ValueError("PCM 16-bit uniquement")
    return nch, rate, data_ofs, data_size

def play():
    st = os.stat(FILENAME); size = st[6] if len(st)>6 else st[0]
    print("Fichier:", FILENAME, "taille:", size)
    if size <= 44: raise ValueError("WAV trop petit")
    with open(FILENAME, "rb") as f:
        nch, rate, ofs, data_size = parse_wav(f)
        print("WAV:", {"ch": nch, "rate": rate, "data": data_size})
        f.seek(ofs)

        # MCLK ≈ 256 * Fs (OK pour CS4344)
        mclk = start_mclk(256 * rate)

        i2s = I2S(0, sck=Pin(BCLK), ws=Pin(WS), sd=Pin(SD),
                  mode=I2S.TX, bits=16, format=I2S.STEREO, rate=rate, ibuf=4096)

        FRAMES = 512
        if nch == 2:
            bpp = FRAMES * 2 * 2
            while True:
                raw = f.read(bpp)
                if not raw: break
                i2s.write(raw)
        else:
            in_bytes = FRAMES * 2
            out = array.array("h", [0]*(FRAMES*2))
            mv = memoryview(out)
            while True:
                raw = f.read(in_bytes)
                if not raw: break
                n = len(raw)//2
                for i in range(n):
                    v = ustruct.unpack_from("<h", raw, i*2)[0]
                    out[2*i] = v; out[2*i+1] = v
                i2s.write(mv[:n*2])

        i2s.deinit()
        mclk.active(0)
        print("Lecture terminée.")

try:
    play()
except Exception as e:
    print("Erreur:", e)