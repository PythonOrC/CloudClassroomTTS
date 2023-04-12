# Copyright (C) 2023 ethan
# 
# This file is part of CloudClassroomTTS.
# 
# CloudClassroomTTS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# CloudClassroomTTS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with CloudClassroomTTS.  If not, see <http://www.gnu.org/licenses/>.

'''
Python script to convert pdf to text and generate speech from it.

Author: Ethan Hu
Creation Date: 2022-12-29
Version: 1.1
License: GNU General Public License v3.0
'''
from json import load

from azure.cognitiveservices.speech import (AudioConfig, ResultReason,
                                            SpeechConfig, SpeechSynthesizer)
from PyPDF2 import PdfFileReader


class ConvertPdfToText:
    def __init__(self, pdf_path, language="en-US", start_page=1, end_page=0, voice="en-US-JessaNeural"):
        self.source_path = pdf_path
        self.language = language
        self.start_page = start_page-1
        self.end_page = end_page
        self.voice = voice
        self.read_book()
        self.read_secret()
        self.config_speech()
        

    #open the json file and read the secret key
    def read_secret(self):
        with open("private/secret.json") as f:
            secret = load(f)
        if secret["key"] == "":
            raise InvalidSecretException("Secret key is empty")
        if secret["region"] == "":
            raise InvalidSecretException("Service region is empty")
        self.secret_key = secret["key"]
        self.service_region = secret["region"]

    #read the pdf file and extract text
    def read_book(self):
        self.pdf = open(self.source_path,"rb")
        pdf_reader = PdfFileReader(self.pdf)
        self.end_page = pdf_reader.numPages if self.end_page == 0 else self.end_page
        self.text = ""
        print("Extracting text from page {} to {}".format(self.start_page + 1, self.end_page))
        for page in range(self.start_page, self.end_page):
            self.text += pdf_reader.getPage(page).extractText()
        self.pdf.close()
        print(self.text)
        
    # configure speech sythesizer
    def config_speech(self):
        print("Configuring speech synthesizer to language {}".format(self.language))
        speech_config = SpeechConfig(subscription=self.secret_key, region=self.service_region)
        speech_config.speech_synthesis_language = self.language
        speech_config.speech_synthesis_voice_name = self.voice
        audio_config = AudioConfig(filename="Speech/output.mp3")
        self.speech_synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    #generate speech and save as a mp3 file
    def generate_speech(self):
        print("Generating speech...")
        result = self.speech_synthesizer.speak_text_async(self.text).get()
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print("Speech generated successfully")
        else:
            print("Error: {}".format(result.reason))

class InvalidSecretException(Exception):
    pass
