import json 


if __name__ == '__main__':
    with open("myDict.json") as readFile:
        # converts json into dictionary
        myDict = json.loads(readFile.read())
        print(myDict)