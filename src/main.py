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
from Converter import ConvertPdfToText
from glob import glob

def prompt(msg,default,options=None):
    if options:
        print(msg)
        for i in range(0,len(options)):
            print(f"{i+1}. {options[i]}")
        val = input("\n")
        if val == "":
            return options[default-1]
        elif val.isnumeric():
                return options[int(val)-1] if int(val)-1 < len(options) else options[default-1]
        else:
            return val
    else:
        val = input(msg)
    return default if val == "" else val

#find pdf in all subdirectories
def find_all_pdfs():
    return glob("**/*.pdf", recursive=True)

if __name__ == "__main__":
    file_prompt = "Select the pdf file to convert or input the path:"
    file_options = find_all_pdfs()
    file_path = prompt(file_prompt, 1, options = file_options)
    language_prompt = "Select the language of the pdf file (default is en-US):"
    language_options = ["en-US", "en-GB", "en-AU", "en-IN", "de-DE", "es-ES", "fr-FR", "it-IT", "ja-JP", "pt-BR", "zh-CN"]
    language = prompt(language_prompt, 1, options = language_options)
    start = int(prompt("Enter the start page (default is beginning, page 1): ", 1))
    end = int(prompt("Enter the end page (default to end of pdf): ", 0))
    print(file_path, language, start, end)
    converter = ConvertPdfToText(file_path, language=language, start_page=start, end_page=end)
    converter.generate_speech()