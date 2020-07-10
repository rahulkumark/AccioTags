# AccioTags
Fetch relevant tags/keywords from a URL

To setup and run the app

1. Install Python & pip V3+
2. Install Django V3+
3. Navigate to root directory and run 'pip install --upgrade pip && pip install -r  requirements.txt'
4. Start the server by running python manage.py runserver 0:8000

Note  :

This project uses NLTK
to install and import nltk

1. Run pip install nltk
2. Run python
3. type 'import nltk' hit enter
4. type 'nltk.download()' //downloads nltk modules *select nltk corpus(required) module only from the list*


Example request body :

{
"input_url":"https://www.machinelearningplus.com/python/python-regex-tutorial-examples/"
}

Response :

[
  "python",
  "regex",
  "tutorial"
]

cURL for the above request:

replace ngrok link with base URL

curl --request POST \
  --url https://f8a943a40814.ngrok.io/tag_generator \
  --header 'content-type: application/json' \
  --data '{
"input_url":"https://www.machinelearningplus.com/python/python-regex-tutorial-examples/"
}'
