# function used to determin if a required file was already proccessed
def isFileWritten(path, filename):
    file = open(path + '/written.txt').read().splitlines()
    for l in file:
        if filename == str(l):
            return True
    return False

def writeToFile(path: str, filename: str, content):
    store = open(path + filename, 'a')
    store.write(content)