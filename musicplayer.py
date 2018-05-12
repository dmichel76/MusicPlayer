#!/usr/bin/env python

from __future__ import division
import os
import sys
import math

import vlc

import kivy
kivy.require('1.0.0')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.clock import Clock



def get_image(file_name):
    directory = os.path.join(sys.path[0], ".") 
    return os.path.join(directory, file_name)
    

#################################################
class Model():
    
    PLAYING = "playing"
    PAUSED = "paused"
    IDLE = "idle"

    def __init__(self, music_file):
        #TODO add file validation
        self.media = vlc.MediaPlayer(music_file)
        self.state = Model.IDLE

    def get_state(self): return self.state

    def get_length(self): return self.media.get_length()
    def get_time(self): return self.media.get_time()

    def play(self):
        self.media.play()
        self.state = Model.PLAYING
        
    def pause(self):
        self.media.pause()
        self.state = Model.PAUSED
        
    def stop(self):
        self.media.stop()
        self.state = Model.IDLE

    def goto(self, value):
        current = 100* self.media.get_position()
        print "%f %f" % (current, value)
        if math.fabs(value-current) > 1: self.media.set_position(value/100)
        
        
#################################################        
class ImageButton(ButtonBehavior, Image):

    def __init__(self, image, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.source = image
    	self.on_press_callback = None

    def set_source(self, source):
        self.source =  source

    def set_on_press_callback(self, func): 
        self.on_press_callback = func

    def on_press(self): 
        if self.on_press_callback: self.on_press_callback()


class View():
        
    IMAGE_STOP = get_image( "stop_small.png")
    IMAGE_PLAY = get_image( "play_small.png")
    IMAGE_PAUSE = get_image( "pause_small.png")

    def __init__(self):
        self.playButton = ImageButton(View.IMAGE_PLAY)
        self.stopButton = ImageButton(View.IMAGE_STOP)
        self.progressBar = self.build_progress_bar()

        self.currentTimeLabel= Label(text="--", size_hint=(.15, 1))
        self.lengthLabel = Label(text="-",size_hint=(.15, 1))

    def get_play_button(self): return self.playButton
    def get_stop_button(self): return self.stopButton
    def get_progress_bar(self): return self.progressBar
    def get_current_time_label(self): return self.currentTimeLabel
    def get_length_label(self): return self.lengthLabel

    def toggle_play_button(self, state):
        if state==Model.IDLE or state==Model.PAUSED: self.playButton.set_source(View.IMAGE_PLAY)
        if state==Model.PLAYING: self.playButton.set_source(View.IMAGE_PAUSE)

    def build_progress_bar(self):
        progressBar = Slider(size_hint=(.7, 1))
        progressBar.range=(0,100)
        progressBar.value=0
        progressBar.ortientation='horizontal'
        progressBar.value_track=True
        progressBar.value_track_color=[0, 0.5, 0.5, 1]
        progressBar.value_track_width = 5
        progressBar.cursor_size = (0,0)
        progressBar.background_width = 20
        return progressBar

    def build(self):

        vl = BoxLayout(orientation='vertical')

        hl = BoxLayout(orientation='horizontal')
        hl.add_widget(Image(source=os.path.join(sys.path[0],"cover.jpg")))
        vl0 = BoxLayout(orientation='vertical')
        vl0.add_widget(Label(text="Money for nothing"))
        vl0.add_widget(Label(text="Dire Straits"))
        hl.add_widget(vl0)
        vl.add_widget(hl)

        hl0 = BoxLayout(orientation='horizontal')
        hl0.add_widget(self.currentTimeLabel)
        hl0.add_widget(self.progressBar)
        hl0.add_widget(self.lengthLabel)
        vl.add_widget(hl0)

        hl1 = BoxLayout(orientation='horizontal')
        hl1.add_widget(self.stopButton)
        hl1.add_widget(self.playButton)
        vl.add_widget(hl1)
        
        return vl

#################################################
class MusicPlayerController(App):

    def __init__(self, **kwargs):
        super(MusicPlayerController, self).__init__(**kwargs)

        #TODO only works for one preloaded song
        self.model = Model(os.path.join(sys.path[0], "money.mp3"))

        self.view = View()
        self.view.get_play_button().set_on_press_callback(self.play_or_pause) 
        self.view.get_stop_button().set_on_press_callback(self.stop) 
        
        self.view.get_progress_bar().bind(value=self.on_progress_bar_change)

    def on_progress_bar_change(self, instance, value):
        self.model.goto(value)

    def nicetime(self, ms):
        minutes=int((ms/(1000*60))%60)
        seconds=int((ms/1000)%60)
        return "%02d" % minutes + ":" + "%02d" % seconds 

    def update(self, dt):

        # update length in case it has changed        
        length = self.model.get_length()
        current_time = self.model.get_time()

        # update progress bar
        prog = 100* current_time/(length*1.0)
        self.view.get_progress_bar().value = prog

        # update labels 
        self.view.get_length_label().text = self.nicetime(length)
        self.view.get_current_time_label().text = self.nicetime(current_time)

    def goto(self, value): 
        self.model.goto(value)

    def stop(self):
        self.model.stop()
        Clock.unschedule(self.update)
        self.view.get_progress_bar().value = 0
        self.view.get_current_time_label().text = "00:00"
        self.view.toggle_play_button(self.model.get_state())

    def play_or_pause(self):
        state = self.model.get_state()
        if state == Model.IDLE or state == Model.PAUSED:
            self.model.play()
            Clock.schedule_interval(self.update, 0.1) 
        else:
            self.model.pause()
            Clock.unschedule(self.update)
         
        self.view.toggle_play_button(self.model.get_state())

    def build(self):
        self.title = "Music Player"
        widget = self.view.build()
        return widget


#################################################
if __name__ in ('__android__', '__main__'):
    MusicPlayerController().run()

