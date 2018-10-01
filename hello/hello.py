from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse

def sendhello(request, mynumber=1):
    print("Yes this is dog")
    #print(request)
    #print()
    return


def sendhellonumber(request, mynumber):
    print("yes yes, numbers")
    print(mynumber)
    message = "you sent a nice number, it is in the number field"
    jsonresponse = "{number: %s, msg: \"you sent a nice number, it is in the number field\"}" % mynumber
    return HttpResponse(jsonresponse)