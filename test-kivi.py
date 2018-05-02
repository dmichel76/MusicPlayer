import vlc

import kivy
kivy.require('1.0.0')
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.clock import Clock


font_size = 30

class StopButton(ButtonBehavior, Image):

    def __init__(self, player, **kwargs):
        super(StopButton, self).__init__(**kwargs)
	self.source = './stop.png'
	self.player = player

    def on_press(self):
        self.player.stop()

class PlayButton(ButtonBehavior, Image):

    def __init__(self, player, **kwargs):
        super(PlayButton, self).__init__(**kwargs)
        self.source = './play.png'
	self.mode = "paused"
	self.player = player
	
    def on_press(self):

	if self.mode == "playing":  
		self.source = 'play.png'
		self.mode = "paused"
		self.player.pause()

	elif self.mode == "paused":
		self.source = 'pause.png'
		self.mode = "playing"
		self.player.play()

class MyApp(App):

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
	self.player = vlc.MediaPlayer('money.mp3')

        self.progressBar = ProgressBar()
	self.progressBar.value = 0

	self.stopButton = StopButton(self.player)
	self.playButton = PlayButton(self.player)

	self.songTime = Label(text="0")
	self.songLength = Label(text="0")

    def update_progressbar(self, dt):

        if self.player.get_time() >=0:
		value = 100 * float(self.player.get_time())/float(self.player.get_length())
		self.progressBar.value = value
		self.songTime.text = str(self.player.get_time())
		self.songLength.text = str(self.player.get_length())
	else:
		self.progressBar.value = 0
		self.playButton.source = ' ./play.png'

    def build(self):
	self.title = "Music Player"

	Clock.schedule_interval(self.update_progressbar, 0.1)
	
	vl = BoxLayout(orientation='vertical')

	hl1 = BoxLayout(orientation='horizontal')
	hl1.add_widget(self.songTime)
	hl1.add_widget(self.progressBar)
	hl1.add_widget(self.songLength)
	vl.add_widget(hl1)

	hl2 = BoxLayout(orientation='horizontal')
	hl2.add_widget(self.stopButton)
	hl2.add_widget(self.playButton)
	vl.add_widget(hl2)

	return vl

if __name__ in ('__android__', '__main__'):
    MyApp().run()


