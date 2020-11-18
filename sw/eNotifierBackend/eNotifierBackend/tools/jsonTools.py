import json
import os


def prettyJson(arg):
    js = json.dumps(get_clean_dict(arg), indent=4, sort_keys=True, default=str)
    return js

def get_clean_dict(arg):

    # If arg is a list
    if isinstance(arg, list):
        return [get_clean_dict(item) for item in arg]

    # If arg is a dictionary
    if type(arg) is dict:
        myDict = arg

    # If arg is a object containing a dictionary
    elif getattr(arg, "__dict__", None):
        myDict = arg.__dict__

    # If obj is not a class object, nor a dictionary (simple variable)
    else:
        return arg

    # Create clean dictionary
    retval = {}
    for key in myDict:
        # Filter out _sa_instance_state
        if key[:4] != '_sa_':
            retval[key] = get_clean_dict(myDict[key])
    return retval

def readJsonFile(file):
    if (os.path.isfile(file)):
        with open(file, 'r') as openfile:
            return json.load(openfile)
    else:
        print('Error loading file ' + str(file))
        return {}

def writeJsonFile(file, dict):
    with open(file, "w") as outfile:
        outfile.write(prettyJson(dict))