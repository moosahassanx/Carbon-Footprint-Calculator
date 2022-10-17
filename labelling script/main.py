# managing imports
import json

# retrieve the file as an object
fileObject = open("hundred-dataset.json")
jsonContent = fileObject.read()
aList = json.loads(jsonContent)

# all the valid tags
validTags = [
    'electricity',      # 105
    'gas',              # 105
    'fuel',             # forbes asks for actual mileage FAKE: 200
    'short flight',     # 1100
    'long flight',      # 4400

    # idk what multiplication goes on these (THEY ARE ALL FAKE)
    'entertainment',    # 50
    'food',             # 50
    'rent',             # 50
    'miscellaneous',    # 80
    'electronics',      # 100
    'industrial',       # 80
    'residency',        # 50
    'health',           # 40
]

# function to validate tag input value
def validateTag(inputTag):
    if inputTag in validTags:
        return True
    else:
        print('List of tags: ', validTags)
        return False

# function to add "tag": "inputVal" to correct index
def addTag():
        print('nothing')

print('aList len(): ', len(aList))

# reading the file and adding tag values
for index, i in enumerate(aList):
    # check if tag does not exist in the object and is actually expenditure
    if 'tag' not in i and float(i['amount']) < 0:
        # print description for the user to see
        print('\n[', index ,'/' , len(aList) , ']')
        print('description: ', i['description'])

        # user input for tag key in object
        tagInput = input('INPUT TAG: ')
        while(validateTag(tagInput) == False):
            tagInput = input('INPUT TAG: ')

        # assign the key and value and display confirmation
        i['tag'] = tagInput
        print('tag set: ', tagInput)

# saving new JSON object to new JSON object
jsonString = json.dumps(aList, sort_keys=True, indent=4, separators=(',', ': '))
jsonFile = open('ready-dataset.json', 'w')
jsonFile.write(jsonString)
jsonFile.close()

# showing changes to modified JSON file
for index, i in enumerate(aList):
    print('\n[', index ,'/' , len(aList) , ']')
    print('description: ', i['description'])
    print('tag: ', i['tag'])

# closing program
fileObject.close()