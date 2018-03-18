import random
import os
import json
import datetime
import string


def getSign(boolean, status, id):
    sign = '<span class="fa %s" style="color:%s; cursor:pointer;"  title=\'Toggle %s\' onclick=\"javascript:window.location.href=\'changestatus%s/%s\'\" />'
    if status == 'PGactive':
        if boolean:
            sign = sign%('fa-check-circle','#42AD3F','Active', '/active' , id)
        else:
            sign = sign%('fa-minus-circle','#DE2121','Active', '/active' , id)

    elif status == 'MDactive':
        if boolean:
            sign = sign%('fa-check-circle','#42AD3F','Active', '/active' , id)
        else:
            sign = sign%('fa-minus-circle','#DE2121','Active', '/active' , id)

    elif status == 'userActive':
        if boolean:
            sign = sign%('fa-check-circle','#42AD3F','Active', '' , id)
        else:
            sign = sign%('fa-minus-circle','#DE2121','Active', '' , id)

    elif status == 'verified':
        if boolean:
            sign = sign%('fa-check-circle','#42AD3F','Verified Status', '/verified' , id)
        else:
            sign = sign%('fa-minus-circle','#DE2121','Verified Status', '/verified' , id)
    return sign


# Checks if a value is an int
def isInt(*args):
    try:
        for value in args:
            int(value)
        return True
    except:
        return False


# Gets pagination values for view page tables
def get_pagination_start(request, numOfRecords):
    pageLength = int(request.POST['pageLength'])
    recordStart = int(request.POST['recordStart'])
    recordEnd = int(request.POST['recordEnd'])
    if 'paginate' in request.POST:
        paginate = request.POST['paginate']
        if paginate == 'next':
            recordStart = recordEnd + 1
        elif paginate == 'prev':
            recordStart -= pageLength
        elif paginate == 'first':
            recordStart = 1
        elif paginate == 'last':
            recordStart = numOfRecords - pageLength + 1
    if recordStart > numOfRecords:
        recordStart = numOfRecords
    if recordStart < 1 or 'firstSearch' in request.POST:
        recordStart = 1

    return pageLength, recordStart

# convert a datetime variable into the format django displays in template pages
def djangoDate(datetimevar):
    monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    datetimeStr = '%s. %s, %s, ' % (monthNames[datetimevar.month - 1], datetimevar.day, datetimevar.year)
    minStr = ''
    if datetimevar.hour >= 12:
        hourStr = str(datetimevar.hour - 12)
        timeAMPM = ' p.m.'
    else:
        hourStr = str(datetimevar.hour)
        timeAMPM = ' a.m.'
    if not datetimevar.minute == 0:
        minStr = str(datetimevar.minute)
        if len(minStr) == 1:
            minStr = ':0' + minStr
        else:
            minStr = ':' + minStr
    datetimeStr += hourStr + minStr + timeAMPM
    return datetimeStr


# Returns true if val = string "True"(case insensitive), else returns false; useful for converting string "True"/"False" to boolean
def str2bool(val):
    return val.lower() in 'true'


# Safe way of deleting session, deletes the specified session if it exists, will not result in error if it doesn't exist
def safeDelSession(request, key):
    if key in request.session:
        del request.session[key]


# Saves value to a temporary session variable
def saveTSession(request, key, value):
    request.session['tEmP_' + key] = value


# Checks if temporary session variable exists
def checkTSession(request, key):
    return 'tEmP_' + key in request.session


# Retrives value stored in temporary session variable
def getTSession(request, key):
    return request.session['tEmP_' + key]


# Delete temporary session variable
def delTSession(request, key):
    if 'tEmP_' + key in request.session:
        del request.session['tEmP_' + key]


# Checks multiple temporary session variables to see if they exists, returns False if one of them doesn't exist, else returns True if all exist
def checkMulTSession(request, keyList):
    for key in keyList:
        if not ('tEmP_' + key in request.session):
            return False
    return True


# Gets the object specified if it exists, returns None when it does not
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


# Random character challenge for captcha

# Parse JSON file
def parseJSON(path):
    json_str = ''
    with open(path, 'r') as json_data:
        for line in json_data:
            line = (line.partition('###')[0]).lstrip().rstrip()  # Removes all comments before loading json:
            line = line.replace('<script>', '')  # Removes script entries
            line = line.replace('</script>', '')
            line = line.replace('^s', ' ')  # for adding space in case of multiline
            json_str += line
    return json.loads(json_str)


# Check if a directory exists, creates it if it does not
def checkDir(directory):
    """ checkDir(directory)

        Check if the specified directory exist. If not it creates it.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


# Make file name?
def makeFileName(minlength=5, maxlength=10):
    length = random.randint(minlength, maxlength)
    letters = string.ascii_lowercase + string.digits
    return ''.join([random.choice(letters) for _ in range(length)])


# Save uploaded file
def save_uploaded_file(dir_to_save, uploaded_file):
    """

    Little helper to save a file
    :param uploadedfile:
    """
    try:
        checkDir(dir_to_save)

        filename = uploaded_file._get_name()
        fd = open('%s/%s' % (dir_to_save, str(filename)), 'w+')
        for chunk in uploaded_file.chunks():
            fd.write(chunk)
            fd.flush()
        fd.close()
        return True
    except Exception as e:
        return False

# Generate a random string
def randomStringGenerator(size=None, chars=None):
    size = size or 6
    chars = chars or string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


# Get substring between two characters (multiple)
def getStrBetweenChars(strToSearch, startChar, endChar, occurrences=1):
    returnList = []
    startIndex = 0
    endIndex = 0
    while occurrences > 0:
        startIndex = strToSearch.find(startChar, endIndex)
        if startIndex != -1:
            endIndex = strToSearch.find(endChar, startIndex)
            if endIndex != -1:
                # print strToSearch[startIndex+1:endIndex]
                returnList.append(strToSearch[startIndex+1:endIndex])
            else:
                # print strToSearch[startIndex+1:]
                returnList.append(strToSearch[startIndex+1:])
            occurrences -= 1
        else:
            break
    # print strToSearch[endIndex+1:].strip()
    returnList.append(strToSearch[endIndex+1:].strip())
    return returnList


# Get datetime in seconds since epoch
def get_time_in_seconds(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return int(delta.total_seconds() * 1000)

