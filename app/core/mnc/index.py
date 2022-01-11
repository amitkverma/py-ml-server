import requests
import json

async def validateClaim(clientData):
    claimReq = getApiRequestWithCredentials(clientData)
    response = callCceApi(claimReq)
    formattedResponse = formatApiResponse(json.loads(response.content))
    return formattedResponse

def formatApiResponse(apiResponse):
    status = {}
    if('claimEdits' in apiResponse):
        claimEdits = apiResponse['claimEdits']
        claimStatusCodes = []
        claimStatusDesc = []
        claimStatusComments = []
        for index, value in enumerate(claimEdits):
            claimStatusCodes.append(claimEdits[index]['editType']['serviceCode'])
            claimStatusDesc.append(claimEdits[index]['editType']['description'])
            claimStatusComments.append(claimEdits[index]['editComment'])
        status['code'] = list(set(claimStatusCodes))
        status['desc'] = list(set(claimStatusDesc))
        status['comments'] = list(set(claimStatusComments))
        return status
    else:
        return status


def callCceApi(reqBody):
    url = 'https://cce.dimensions-healthcare.com/cce/getClaimsEdits'
    result = requests.post(url, json.dumps(reqBody), headers={"Content-Type":"application/json"})
    return result

def getApiRequestWithCredentials(claimData):
    req = {}
    req['username'] = "csingh"
    req['password'] = 'w@0syK@7r_@@v!U!@15O6nFUd_'
    req['services'] = '1'
    req['isStrictCheck'] = 0
    req['claims'] = prepareCceRequest(claimData)
    return req


def prepareCceRequest(data):
    diagsList = prepareDiagnosisList(data.diagnosisList)
    activityList = prepareActivityList(data.activityList)
    claims = []
    singleClaim = {}
    singleClaim["claimID"] = "test"
    singleClaim["payerId"] = ""
    singleClaim["providerId"] = "22018480319"
    singleClaim['claimSubmissionAllergyList'] = []
    singleClaim['claimSubmissionDiagnosisList'] = diagsList
    singleClaim['claimSubmissionActivityList'] = activityList
    singleClaim['claimSubmissionEncounter'] = []
    claims.append(singleClaim)
    return claims

def prepareActivityList(activities):
    activityList = []
    for i in range(len(activities)):
        single_activity = {}
        single_activity['activityId'] = i+1
        single_activity['activityType'] = activities[i]['type']
        single_activity['activitySource'] = "CURRENT"
        single_activity['quantity'] = activities[i]['quantity']
        single_activity['activityStart'] = '20/08/2020'#str(row['StartDate'])
        single_activity['duration'] = 1
        single_activity['unit'] = 'GRANULAR'
        single_activity['activityCode'] = activities[i]['code']
        activityList.append(single_activity)    
    return activityList


def prepareDiagnosisList(diagnoses):
    diagsList = []
    for i in range(len(diagnoses)):
        single_diag_dict = {}
        single_diag_dict['diagnosisType'] = diagnoses[i]['type']
        single_diag_dict['diagnosisSource'] = 'CURRENT'
        single_diag_dict['diagnosisCode'] = diagnoses[i]['code']
        diagsList.append(single_diag_dict)
    return diagsList
