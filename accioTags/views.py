from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from rest_framework import status
from nltk.corpus import stopwords
from textblob import TextBlob
from accio_tags.settings import BASE_DIR
import nltk
import re
import mmap
import os


class FetchTags(APIView):
    def post(self,request):
        try:
            data = request.data

            validate = URLValidator()
            try:
                validate(data['input_url'])
            except:
                return Response({'Message':'No URL given. Please provide a valid url to get tags!'},status=status.HTTP_200_OK)

            words = list()
            new_list = list()
            relevant_tags = list()
            s = ""

            tags = urlparse(data['input_url']) #get path from url
            pattern = re.compile(r'(\w+)')
            matches = pattern.finditer(tags.path + tags.fragment) # get all words from url
            
            for match in matches:
                words.append(match.group()) #storing words in a list

            #removing stop words using nltk corpus module
            filtered_words = [word for word in words if word not in stopwords.words('english')]

            #getting revelant tags from local dataset
            file_to_open = os.path.join(BASE_DIR, 'accioTags/datasets.txt')
            with open(file_to_open,'r') as file, \
                mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                for word in filtered_words:
                    word = str.encode(word)
                    if s.find(word) != -1:
                        relevant_tags.append(word.decode())

            #removing duplicates
            relevant_tags = list(dict.fromkeys(relevant_tags))
            words_str = " ".join(relevant_tags)
            blob = TextBlob(words_str)
            phrases = blob.noun_phrases #getting nouns from the relevant tags

            for phrase in phrases:
                new_list.append(phrase.split())

            # storing resulting phrases in a list and make a flat list out of it
            new_list =  [item for sublist in new_list for item in sublist]
            final_list = new_list + relevant_tags
            #removing duplicates
            final_list = list(dict.fromkeys(final_list))

            return Response(final_list)
        except Exception as e:
            raise
