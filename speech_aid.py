import pyttsx3
import random
import Levenshtein
import speech_recognition as sr


def normal_pronounce_word(word, voice_id, slow_pronunciation=False):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech (words per minute)
    engine.setProperty('volume', 0.8)  # Volume level (0.0 to 1.0)

    if slow_pronunciation:
        engine.setProperty('rate', 100)  # Slower speed of speech

    engine.setProperty('voice', voice_id)
    engine.say(word)
    engine.runAndWait()

def slow_pronounce_word(word, voice_id, slow_pronunciation=False):
    if slow_pronunciation:
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)  
        engine.setProperty('volume', 0.8) 

        engine.setProperty('voice', voice_id)
        engine.say(word)
        engine.runAndWait()


def score_pronunciation(word, spoken_word):
    distance = Levenshtein.distance(word, spoken_word)
    max_distance = max(len(word), len(spoken_word))
    similarity = 1 - (distance / max_distance)
    score = similarity * 100
    return score


def listen_and_score(word):
    recognizer = sr.Recognizer()

    print("Please speak the word:", word)
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        spoken_word = recognizer.recognize_google(audio)
        print("You pronounced:", spoken_word)

        score = score_pronunciation(word, spoken_word)
        print("Your score:", score)

    except sr.UnknownValueError:
        print("Sorry, could not understand your pronunciation.")


def main():
    words = ["Pa", "Ka", "Ma", "Sa", "Co", "Ga", "Gu"]

    # Initialize the engine
    engine = pyttsx3.init()

    while True:
        # Get the list of available voices
        voices = engine.getProperty('voices')

        # Print voice attributes
        print("Available Voices:")
        for index, voice in enumerate(voices):
            print(f"{index+1}. Voice ID: {voice.id}")
            print(f"   Name: {voice.name}")
            print(f"   Languages Spoken: {voice.languages}")
            print(f"   Gender: {voice.gender}")
            print("")

        print("enter 1 for hearing the pronounciation in a man's voice and 2 for hearing the same in woman's voice")
        print("")

        # Let the user select a voice
        voice_choice = int(input("Select a voice (enter the corresponding number): "))
        voice_id = voices[voice_choice - 1].id
        sequence_length = int(input("Enter the length of the sequence: "))
        sequence = random.choices(words, k=sequence_length)
        word = "".join(sequence)

        print("Word to pronounce:", word)

        normal_pronounce_word(word, voice_id)

        choice_slow = input("Do you want to hear the pronounced word slowly? (y/n): ")
        slow_pronunciation = choice_slow.lower() == "y"

        normal_pronounce_word(word, voice_id, slow_pronunciation)
        listen_and_score(word)

        choice = input("Do you want to hear the correct pronunciation? (y/n): ")
        if choice.lower() == "y":
            slow_pronounce_word(word, voice_id)

        repeat = input("Do you want to try again? (y/n): ")
        if repeat.lower() != "y":
            break


if __name__ == "__main__":
    main()


