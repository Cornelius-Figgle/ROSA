#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/ROSA/
# ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
ROBOTICALLY OBNOXIOUS SERVING ASSISTANT - an emotional voice assistant
'''

'''
This file was authored by [jez](https://stackoverflow.com/users/3019689/jez) on
StackOverflow - for more info please see the [corresponding answer](https://stackoverflow.com/a/58808060/19860022)
THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX 
HARRISON, AS OF 2023

It may work separately and independently of the main repo, it may not

- DuckTypedMicrophone solution (c) jez 2019
- Adaptation (c) Max Harrison 2023

- Code (c) Max Harrison 2023
- Ideas (c) Callum Blumfield 2023
- Ideas (c) Max Harrison 2023
- Vocals (c) Evie Peacock 2023
- Art (c) Ashe Ceaton 2023

Thanks also to everyone else for support throughout (sorry for the
spam). also thanks to all the internet peoples that helped with this
as well 
'''

# note: view associated GitHub info as well
__version__ = 'v0.8.0'  
__author__ = 'jez'
__email__ = 'https://stackoverflow.com/a/58808060/19860022'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2019 Jez'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['jez', 'Max Harrison', 'Callum Blumfield', 'Evie Peacock', 'Ashe Ceaton']


import audiomath; audiomath.RequireAudiomathVersion( '1.12.0' )
import speech_recognition


class DuckTypedMicrophone(speech_recognition.AudioSource): # descent from AudioSource is required purely to pass an assertion in Recognizer.listen()
    def __init__( self, device=None, chunkSeconds=1024/44100.0 ):  # 1024 samples at 44100 Hz is about 23 ms
        self.recorder = None
        self.device = device
        self.chunkSeconds = chunkSeconds
    def __enter__( self ):
        self.nSamplesRead = 0
        self.recorder = audiomath.Recorder( audiomath.Sound( 5, nChannels=1 ), loop=True, device=self.device )
        # Attributes required by Recognizer.listen():
        self.CHUNK = audiomath.SecondsToSamples( self.chunkSeconds, self.recorder.fs, int )
        self.SAMPLE_RATE = int( self.recorder.fs )
        self.SAMPLE_WIDTH = self.recorder.sound.nbytes
        return self
    def __exit__( self, *blx ):
        self.recorder.Stop()
        self.recorder = None
    def read( self, nSamples ):
        sampleArray = self.recorder.ReadSamples( self.nSamplesRead, nSamples )
        self.nSamplesRead += nSamples
        return self.recorder.sound.dat2str( sampleArray )
    @property
    def stream( self ): # attribute must be present to pass an assertion in Recognizer.listen(), and its value must have a .read() method
        return self if self.recorder else None