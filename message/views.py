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
from .models import Messages, Whatsapp_Message
from .serializer import ChatMessageSerializer
from twilio.twiml.messaging_response import MessagingResponse
from django.http import HttpResponse, HttpResponseForbidden
import os
from twilio.rest import Client

account_sid = os.getenv('TWILIO_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

def _save_message(*args, **kwargs):
       try:
            Whatsapp_Message.objects.create(**kwargs)
       except Exception as e:
           print("Error saving message: ", e)
#     print(kwargs)   

@api_view(["POST"])
def receive_whatsapp_message(request):
    response  = MessagingResponse()
    
    print(request.data)
    if request.data["AccountSid"] == account_sid:
       _save_message(
           message_id = request.data["MessageSid"],
           profile_name = request.data["ProfileName"],
           message_type = request.data["MessageType"],
           _from = request.data["From"],
           body = request.data["Body"],
           to = request.data["To"]
       )
       
       response.message("Message Received")
       return HttpResponse(str(response))
    
    return HttpResponseForbidden("Invalid Request")

@api_view(["POST"])
def send_whatsapp_message(request):
    try:
        
       client = Client(account_sid, auth_token)

       message = client.messages.create(
              from_='whatsapp:+14155238886',
              body=request.data["body"],
              to=f'whatsapp:+91{request.data["to"]}'
       )
       if message:
              _save_message(
              message_id = message.sid,
              _from = message.from_,
              body = message.body,
              to = message.to
              )
       return HttpResponse("Message sent")
    except Exception as e:
         print("Error sending message: ", e)

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
