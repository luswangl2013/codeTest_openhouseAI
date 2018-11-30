# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 22:46:42 2018

@author: lin

python version 2.7.14
flask version 0.12.2
"""

from flask import Flask, render_template, request
import json
import re
app = Flask(__name__)
f = open("king-i.txt", "r")#text corpus
kingi = f.read()

@app.route('/')
def index():
    return render_template("main_index.html", text= kingi)

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        string = request.form
        string = string['string']# get the query string
        text = kingi
        result_dict = {}
        result_dict["query_text"] = string
        result_dict["number_of_occurrences"] = text.count(string)
        if result_dict["number_of_occurrences"] == 0:# search result == 0
            js = json.dumps(result_dict, indent=4, separators=(',\n', ': '))
            with open('application/json.json', 'w') as outfile:
                json.dump(js, outfile)
            return render_template("result.html", string = js)
        #text = kingi.splitlines()
        text= kingi.split("\n")#split into different line
        regex = re.compile(r"\.|\?|!")#sentence segmentation
        occurrences = []
        for i in range(len(text)):
            index = text[i].find(string)
            if index != -1:
                occurrence = {}
                occurrence["line"] = i+1
                occurrence["start"] = index + 1
                occurrence["end"] = index + len(string) + 1
                if i == 0:#extend the line to define sentence
                    origin = text[i] + " " + text[i+1]
                elif i == len(text) - 1:
                    origin = text[i-1] + " " + text[i]
                else:
                    origin = text[i-1] + " " + text[i]+ " " + text[i+1]
                
                if re.search(regex, origin) == None:#no sentence segment in extended text
                    occurrence["in_sentence"] = text[i]
                else:
                    '''
                    sentence_end = re.search(regex, origin).span()
                    pos = index + len(text[i-1]) + 1
                    begin = sentence_end[0]
                    while sentence_end[0] < pos:
                        begin = sentence_end[0]
                        sentence_end = re.search(regex, origin[begin+1:]).span()
                    end = sentence_end[0]
                    '''
                    pos = index + len(text[i-1]) + 1
                    begin = pos - 1
                    end = pos + len(string) + 1
                    while origin[begin] not in ".?!":
                        begin -= 1
                    while origin[end] not in ".?!":
                        end += 1
                    occurrence["in_sentence"] = origin[begin+2:end+1]

                occurrences.append(occurrence)
        result_dict["occurrences"] = occurrences
        js = json.dumps(result_dict, indent=4, separators=(',\n', ': '))
        with open('application/json.txt', 'w') as outfile:
            json.dump(js, outfile)
        return render_template("result.html", string = js)

if __name__ == '__main__':
    app.run()
