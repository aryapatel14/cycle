from flask import Blueprint, request
from ..services.get_aws import FloAws
from ..utils import response

mixed_api = Blueprint('mixed_api', __name__)
flo_aws =  FILES_CONTAINS_LOCAL_IPAws()

@mixed_api.route("/imagepresigned/<imageId>")
def imagePresignedUrl(imageId):
    """
    Get Pre-signed URL to view (GET method) / upload (POST method) image to S3
    """
    if request.method == "GET":
        # print('[imagePresignedUrl] GET: ', imageId)
        url = flo_aws.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": flo_aws.S3_BUCKET, "Key": f"profile-images/{imageId}"},
            ExpiresIn=3600,
        )
        if url is not None:
            return {"presignedUrl": url}

    elif request.method == "POST":
        url = flo_aws.s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": flo_aws.S3_BUCKET,
                "Key": f"profile-images/{imageId}",
                "ContentType": "image/jpeg",
            },
            ExpiresIn=3600,
        )
        # print('[imagePresignedUrl POST] ', url)
        if url is not None:
            return {"presignedUrl": url}

    return response.error_json_response()