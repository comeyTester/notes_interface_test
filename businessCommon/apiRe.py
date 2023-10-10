import requests
from common.caseLogsMethod import info
import json


class ApiRe:
    @staticmethod
    def note_post(url, user_id, sid, body, new_headers=None):
        if new_headers is not None:
            headers = new_headers
        else:
            headers = {
                'Content-Type': 'application/json',
                'X-user-key': user_id,
                'Cookie': f'wps_sid={sid}'
            }

        info(f'url:{url}')
        info(f'headers:{json.dumps(headers)}')
        info(f'body:{json.dumps(body)}')
        res = requests.post(url=url, headers=headers, json=body)
        info(f'res code:{res.status_code}')
        info(f'res body:{res.json()}')
        return res

    @staticmethod
    def note_get(url, sid):
        cookie = {
            'wps_sid': sid
        }
        info(f'url:{url}')
        info(f'cookie:{json.dumps(cookie)}')
        res = requests.get(url=url, cookies=cookie)
        info(f'res code:{res.status_code}')
        info(f'res body:{res.json()}')
        return res
