from django.core.exceptions import ImproperlyConfigured
import requests
import json
from chattyhive_project import settings


def send_gcm_message(regs_id, data, collapse_key=None):

    api_key = getattr(settings, 'GCM_APIKEY', None)
    if not api_key:
        raise ImproperlyConfigured("You haven't set the 'GCM_APIKEY' setting yet.")

    values = dict(registration_ids=regs_id,
                  collapse_key=collapse_key,
                  data=data)
    print(values)

    values = json.dumps(values)

    headers = {
        'UserAgent': "GCM-Server",
        'Content-Type': 'application/json',
        'Authorization': 'key=' + api_key,
    }

    response = requests.post(url="https://android.googleapis.com/gcm/send",
                             data=values,
                             headers=headers)

    json_response = json.loads(response.text)
    return json_response