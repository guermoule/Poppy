# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 20:36:10 2015

@author: guermoule
"""
import tempfile
import re
import subprocess
import os

class PicoTTS():
    """
    Uses the svox-pico-tts speech synthesizer
    Requires pico2wave to be available
    """
    SLUG = "pico-tts"
    
    def __init__(self, language="fr-FR"):
        self.language = language

    @property
    def languages(self):
        cmd = ['pico2wave', '-l', 'NULL',
                            '-w', os.devnull,
                            'NULL']
        with tempfile.SpooledTemporaryFile() as f:
            subprocess.call(cmd, stderr=f)
            f.seek(0)
            output = f.read()
        pattern = re.compile(r'Unknown language: NULL\nValid languages:\n' +
                             r'((?:[a-z]{2}-[A-Z]{2}\n)+)')
        matchobj = pattern.match(output)
        if not matchobj:
            raise RuntimeError("pico2wave: valid languages not detected")
        langs = matchobj.group(1).split()
        return langs
        
    def play(self, filename):
        cmd = ['aplay', str(filename)]
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)   

    def say(self, phrase):
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd = ['pico2wave', '--wave', fname]
        if self.language not in self.languages:
                raise ValueError("Language '%s' not supported by '%s'",
                                 self.language, self.SLUG)
        cmd.extend(['-l', self.language])
        cmd.append(phrase)
        
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)

        self.play(fname)
        os.remove(fname)