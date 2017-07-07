import requests
import json
import urllib.request
import os

class ImageScraper(object):

    def __init__(self, apiKey):
        
        self.baseUrl = "https://www.googleapis.com/customsearch/v1"
        self.apiKey = apiKey

        self.params = {"searchType": "image",
                       "imgColorType": "color",
                       "imgType": "photo",
                       "filter": "0",
                       "safe": "medium",
                       "key": apiKey}

    def sendRequest(self, query, numImages, start=0):
        # query - string the query to be sent in the Custom Search
        # numImages - int number of images to return, rounded down to nearest 10

        self.params["q"] = query
        self.params["cx"] = "002614461317739606024:pdrv0eu2ihq"

        imageLinks = []
        for i in range(start, start + int(numImages/10)):
            self.params["start"] = i+1

            response = requests.get(self.baseUrl, params=self.params).content
            response = json.loads(response)

            if "error" in response:
                print("The API request has encountered an error: " +
                      response["error"]["errors"][0]["reason"])
                return imageLinks
                
            
            imageLinks.extend([val["image"]["thumbnailLink"]
                          for val in response["items"]])
        # end loop
        
        return imageLinks

    def downloadImages(self, word, numImages):
        # params - see sendRequest()

        links = self.sendRequest(word, numImages)

        if links is None:
            return
        
        if not os.path.exists("trainingData/" + word):
            os.makedirs("trainingData/" + word)
        
        for i in range(len(links)):
            name = "img"
            new_name = name
            n = 0
            while os.path.exists("trainingData/" + word + "/" + new_name + ".png"):
                new_name = name + str(n)
                n += 1
            urllib.request.urlretrieve(links[i], "trainingData/" + word + "/" +  new_name + ".png")