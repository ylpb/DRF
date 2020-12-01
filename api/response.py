from rest_framework.response import Response

class APIResponse(Response):
    def __init__(self, status=0,
                 results=None, msg='ok',http_status=None,headers=None,
                 exception=False, content_type=None,**kwargs):
        data = {
            "status":status,
            'msg':msg,
        }
        if results is not None:
            data['results'] = results

        data.update(**kwargs)
        super().__init__(data=data,status=http_status,headers=headers,
                         exception=exception,content_type=content_type)

