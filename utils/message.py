def error_required(field='field'):
    return {
        'type': 'error',
        'field': field,
        'message': 'field is required or is invalid'
    }


def success_required():
    return {
        'type': 'success'
    }


def success_response(data):
    return {
        'type': 'success',
        'message': 'success',
        'data': data
    }
