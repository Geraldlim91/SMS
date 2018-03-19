import simplejson as json
from src.settings import BASE_DIR

def symptomcheck(symptoms):
    diagnoses = []
    with open(BASE_DIR+'/src/util/json/symptoms.json') as json_data:
        data = json.load(json_data)
        for d in data:
            for s in symptoms:
                if (d.has_key(s)):
                    diagnoses.append(d)
    json_data.close()

    possible_diagnoses = list()
    for diag in diagnoses:
        key_list = diag.keys()
        for k in key_list:
            possible_diagnoses += diag[k]

    diagnosis_list = list()
    for di in possible_diagnoses:
        diagnosis_list.append(di['diagnosis'])

    return diagnosis_list


def issueinformation(issue):
    des_list = list()
    with open(BASE_DIR + '/src/util/json/issue.json') as json_data:
        data = json.load(json_data)
        for d in data:
            if (d.has_key(issue)):
                des_list.append(d[issue]['Description'])
                des_list.append(d[issue]['TreatmentDescription'])

    json_data.close()
    return des_list


print issueinformation('German measles')[0]
print issueinformation('German measles')[1]


# Checks if a value is an int
def isInt(*args):
    try:
        for value in args:
            int(value)
        return True
    except:
        return False

# Gets the object specified if it exists, returns None when it does not
def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)

    except model.DoesNotExist:
        return None
