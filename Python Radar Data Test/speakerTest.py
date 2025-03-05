from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

speakerLow = TonalBuzzer(18)
speakerHigh = TonalBuzzer(13)

speakerLow.play(Tone(220.0))
sleep(1)
speakerLow.stop()

speakerHigh.play(Tone(220.0))
sleep(1)
speakerHigh.stop()