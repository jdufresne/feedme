import json
from django.http import HttpResponse


def json_response(obj):
    return HttpResponse(json.dumps(obj), mimetype="application/json")
