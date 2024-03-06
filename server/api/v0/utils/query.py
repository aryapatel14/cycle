from ..services.get_aws import FloAws
from boto3.dynamodb.conditions import Key
from ..utils import response

def res(resp):
    if response.is_valid_response(resp):
        if not resp["Items"]:
            # Empty record
            return response.ok_json_response()
        return resp["Items"]

def query_all(userid):
    return FloAws.periodTable.query(
                KeyConditionExpression=Key("userId").eq(userid),
                ScanIndexForward=False,
                ProjectionExpression="dateStr, flow, moods, symptoms, discharge",
            )

def query_start_end(userid, startEpoch, endEpoch): 
    try:
        resp = FloAws.periodTable.query(
                KeyConditionExpression=Key("userId").eq(userid)
                & Key("timestamp").between(startEpoch, endEpoch)
        )
        return res(resp)
    except Exception as e:
        return response.error_json_response(e)
    
def query_exact(userid, time): 
    try:
        resp = FloAws.periodTable.query(
            KeyConditionExpression=Key("userId").eq(userid)
            & Key("timestamp").eq(time)
        )
        return res(resp)
    except Exception as e:
        return response.error_json_response(e)
    
def query_lastest(userid):
    return FloAws.periodTable.query(
            KeyConditionExpression=Key("userId").eq(userid),
            ScanIndexForward=False,
            Limit=1,
        )