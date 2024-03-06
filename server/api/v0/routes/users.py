import json
from flask import Blueprint, request, url_for, current_app
from dotenv import load_dotenv

from ..services.get_aws import FloAws
from ..services.get_firebase import FloFirebase
from ..utils import response, conversion

users_api = Blueprint('users_api', __name__)
Flo_aws = FloAws()
Flo_firebase = FloFirebase()

load_dotenv()

@users_api.get('/users/<userid>')
def users_get(userid):
    resp = flo_aws.userTable.get_item(Key={"userId": userid})
    current_app.logger.info(f"[GET] response: {resp}")
    if response.is_valid_response(resp):
        return resp.get("Item", response.ok_json_response())
    else:
        return response.error_json_response(userid)

@users_api.post('/users/<userid>')
def users_post(userid):


    data = request.data.decode("utf-8")
    user_obj = json.loads(data)
    print(f"user_obj is {user_obj}")
    current_app.logger.info("[POST] received data: ", user_obj)
    try:
        flo_aws.userTable.put_item(Item=user_obj)
        print(f"put object {user_obj} into userTable")
        return user_obj
    except Exception as e:
        return response.error_json_response(e)

@users_api.put('/users/<userid>')
def users_put(userid):
    data = request.data.decode("utf-8")
    received_json_data = json.loads(data)
    print(f"received_json_data: {received_json_data}")

    data2update = dict()
    for k, v in received_json_data.items():
        if (k == "userId"): continue
        data2update[k] = {"Value": v}
    try:
        flo_aws.userTable.update_item(Key={"userId": userid}, AttributeUpdates=data2update)
        return response.ok_json_response()
    except Exception as e:
        print(f"error! {e}")
        return response.error_json_response(e)

@users_api.delete('/users/<userid>')
def users_delete(userid):

    all_history = url_for('periods', userid=userid, returnRaw=True)
    dateToDelete = [x["dateStr"] for x in all_history]
    try:
        flo_aws.userTable.delete_item(Key={"userId": userid})
        # Must delete with a composite primary key (both the partition key and the sort key)
        for d in dateToDelete:
            flo_aws.periodTable.delete_item(
                Key={"userId": userid, "timestamp": conversion.convert_dateStr_epoch(d)}
            )
        flo_aws.s3.delete_object(Bucket=flo_aws.S3_BUCKET, Key=f"profile-images/{userid}.jpg")
        flo_firebase.auth.delete_user(uid=userid)
        return response.ok_json_response()
    except Exception as e:
        return response.error_json_response(e)
