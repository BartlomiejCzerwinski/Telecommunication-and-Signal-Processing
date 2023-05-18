import sounddevice as sd
import scipy.io.wavfile as wav

def start_recording():
    global is_recording, recorded_audio
    print("Rozpoczynam nagrywanie... (Wpisz 'stop' i naciśnij Enter, aby zatrzymać nagrywanie)")
    recorded_audio = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1)
    is_recording = True

def stop_recording():
    global is_recording, recorded_audio, recording_time
    if is_recording:
        print("Zatrzymuję nagrywanie...")
        recorded_audio = recorded_audio[:recording_time * sample_rate]
        wav.write("recorded_audio.wav", sample_rate, recorded_audio)
        is_recording = False

def play_recorded_audio():
    print("Odtwarzanie nagranego dźwięku...")
    sample_rate, recorded_audio = wav.read("recorded_audio.wav")
    sd.play(recorded_audio, sample_rate, blocking=True)

sample_rate = 44100
duration = 10

is_recording = False
recorded_audio = []
recording_time = 0

while True:
    print("Menu:")
    print("1. Nagrywanie dźwięku")
    print("2. Odtwarzanie nagranego dźwięku")
    print("3. Wyjście")
    choice = input("Wybierz opcję: ")

    if choice == "1":
        if is_recording:
            print("Nagrywanie już trwa...")
        else:
            start_recording()
            stop_input = input()
            if stop_input.lower() == "stop":
                recording_time = len(recorded_audio) // sample_rate
                stop_recording()
                print("Nagranie zapisane.")
    elif choice == "2":
        if is_recording:
            print("Zatrzymaj nagrywanie przed odtwarzaniem.")
        elif len(recorded_audio) == 0:
            print("Brak nagranego dźwięku.")
        else:
            play_recorded_audio()
    elif choice == "3":
        if is_recording:
            stop_recording()
        break
    else:
        print("Nieprawidłowy wybór.")