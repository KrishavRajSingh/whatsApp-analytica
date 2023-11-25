# from django.shortcuts import render

# # Create your views here.
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from .models import Messages
# from .serializer import DataSerializer
# # Create your views here.


# @api_view(['POST'])
# def postData(request):
#     serializer = DataSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)


# @api_view(['GET'])
# def getData(request):
#     app = Messages.objects.all()
#     serializer = DataSerializer(app, many=True)
#     return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Messages
from .serializer import ChatMessageSerializer


@api_view(["POST"])
def postData(request):
    # Extract the 'data' part from the incoming JSON
    data = request.data.get("data", {})
    #    change from in data to from_field
    # data["from_field"] = data['from']
    print(data)
    # Use the serializer to validate and save the data
    # serializer = ChatMessageSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.create(data)

    Messages.objects.create(
           id=data['id'],
           from_field=data['from'],
           to=data['to'],
           author=data['author'],
           pushname=data['pushname'],
           ack=data['ack'],
           type=data['type'],
           body=data['body'],
           media=data['media'],
           isSelf=data['self'],
           fromMe=data['fromMe'],
           isForwarded=data['isForwarded'],
           isMentioned=data['isMentioned'],
           quotedMsg=data['quotedMsg'],
           mentionedIds=data['mentionedIds'],
           time=data['time']
    )
    return Response(data)
    # else:
    #     return Response(serializer.errors, status=400)
