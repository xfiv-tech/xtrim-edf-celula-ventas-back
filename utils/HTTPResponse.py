import json
from flask import Response


MIMETYPEJSON: str = 'application/json'


def response_404(message=''):
    response = json.dumps({'status': 404, 'message': f'{message} NOT FOUND'})
    return Response(response, status=404, mimetype=MIMETYPEJSON)


def response_400(field='', message=''):
    response = json.dumps({'status': 400, 'field': field, 'message': message})
    return Response(response, status=400, mimetype=MIMETYPEJSON)


def response_data_200(message='', data=None):
    response = json.dumps({'status': 200, 'message': message, 'data': data})
    return Response(response, status=200, mimetype=MIMETYPEJSON)


def response_status_200():
    return Response(status=200, mimetype=MIMETYPEJSON)
