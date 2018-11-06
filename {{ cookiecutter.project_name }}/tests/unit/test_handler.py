import json
import pytest
from first_function import app
import urllib
import os

{% if cookiecutter.include_apigw == "y" %}

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": "{ \"test\": \"body\"}",
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": ""
            },
            "stage": "prod"
        },
        "queryStringParameters": {
            "foo": "bar"
        },
        "headers": {
            "Via":
                "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language":
                "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer":
                "true",
            "CloudFront-Is-SmartTV-Viewer":
                "false",
            "CloudFront-Is-Mobile-Viewer":
                "false",
            "X-Forwarded-For":
                "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country":
                "US",
            "Accept":
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests":
                "1",
            "X-Forwarded-Port":
                "443",
            "Host":
                "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto":
                "https",
            "X-Amz-Cf-Id":
                "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer":
                "false",
            "Cache-Control":
                "max-age=0",
            "User-Agent":
                "Custom User Agent String",
            "CloudFront-Forwarded-Proto":
                "https",
            "Accept-Encoding":
                "gzip, deflate, sdch"
        },
        "pathParameters": {
            "proxy": "/examplepath"
        },
        "httpMethod": "POST",
        "stageVariables": {
            "baz": "qux"
        },
        "path": "/examplepath"
    }


def test_lambda_handler(apigw_event):
    ret = app.lambda_handler(apigw_event, "")
    assert ret['statusCode'] == 200
    assert ret['body'] == json.dumps({'hello': 'world'})

{% else %}


@pytest.fixture()
def lambda_event():
    """ Generates Lambda Event"""

    return {'foo': 'bar'}


def test_lambda_handler_0(lambda_event):
    ret = app.lambda_handler(lambda_event, '')
    assert ret == {'hello': 'world'}

{% endif %}

def check_connectivity(reference):
    try:
        urllib.request.urlopen(reference, timeout=1)
        return True
    except urllib.request.URLError:
        return False

{% if cookiecutter.include_xray == "y" %}

def xrays_return_information():
    assert os.environ('_X_AMZN_TRACE_ID') is not None

def xrays_deamon_running():
    ret = os.environ('AWS_XRAY_DEAMON_ADDRESS')
    assert ret is not None
    add, port = ret.split(':')
    assert add is not None
    assert port is not None
    assert check_connectivity(f'http://{ret}')
{% endif %}


#
#
#
#
#
#
#
#
#
#
#
key = 'hello'
value = 'test'


def test_get_message_0(lambda_event, key, value):
    ret = app.lambda_handler(lambda_event, '')
    # assert ret == {'hello': 'world'}
    assert ret == {key: value}


def test_get_message_1(apigw_event, key, value):
    ret = app.lambda_handler(apigw_event, '')
    assert ret['statusCode'] == 200
    assert ret['body'] == json.dumps({key: value})


def test_get_message_2(lambda_event, key, value):
    ret = app.lambda_handler(lambda_event, '')
    assert ret == {key: value}


#
#
#
#
#
#
#
#
#
#
#
#
def test_runs_on_aws_lambda_0():
    ret = app.lambda_handler(lambda_event, '')
    assert ret == {'hello': 'world'}


def test_runs_on_aws_lambda_1(apigw_event):
    ret = app.lambda_handler(apigw_event, '')
    assert ret['statusCode'] == 200
    assert ret['body'] == json.dumps({'hello': 'world'})


@pytest.fixture()
def lambda_event():
    """ Generates Lambda Event"""

    return {"foo": "bar"}


def test_lambda_handler_1(lambda_event):
    ret = 'AWS_SAM_LOCAL' not in os.environ and 'LAMBDA_TASK_ROOT' in os.environ
    assert ret == True

def test_http_method(lambda_event):
    ret = app.lambda_handler(lambda_event, '')
    assert ret == {'httpMethod': 'POST'}

