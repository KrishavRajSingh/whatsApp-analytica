from rest_framework import serializers
from .models import Messages

# class DataSerializer(serializers.ModelSerializer):
#     class Meta:
#        model = Messages
#        fields = ['id', 'from', 'to', 'author', 'pushname', 'ack', 'type', 'body', 'media', 'fromMe', 'self', 'isForwarded', 'isMentioned', 'quotedMsg', 'mentionedIds', 'time']

#     def to_internal_value(self, data):
#         # Extract the 'data' part from the incoming JSON
#         data = data.get('data', {})
#         return super().to_internal_value(data)
    

# from rest_framework import serializers
# from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
   class Meta:
       model = Messages
       fields = ['id', 'from_field', 'to', 'author', 'pushname', 'ack', 'type', 'body', 'media', 'fromMe', 'self', 'isForwarded', 'isMentioned', 'quotedMsg', 'mentionedIds', 'time']

#    def to_internal_value(self, data):
#        print(data)
#        data = data.get('data', {})
#        return super().to_internal_value(data)

   def create(self, validated_data):
       print(validated_data)
       return Messages.objects.create(
           id=validated_data.get('id'),
           from_field=validated_data.get('from'),
           to=validated_data.get('to'),
           author=validated_data.get('author'),
           pushname=validated_data.get('pushname'),
           ack=validated_data.get('ack'),
           type=validated_data.get('type'),
           body=validated_data.get('body'),
           media=validated_data.get('media'),
           fromMe=validated_data.get('fromMe'),
           self=validated_data.get('self'),
           isForwarded=validated_data.get('isForwarded'),
           isMentioned=validated_data.get('isMentioned'),
           quotedMsg=validated_data.get('quotedMsg'),
           mentionedIds=validated_data.get('mentionedIds'),
           time=validated_data.get('time')
       )

   def update(self, instance, validated_data):
       instance.id = validated_data.get('id', instance.id)
       instance.from_field = validated_data.get('from', instance.from_field)
       instance.to = validated_data.get('to', instance.to)
       instance.author = validated_data.get('author', instance.author)
       instance.pushname = validated_data.get('pushname', instance.pushname)
       instance.ack = validated_data.get('ack', instance.ack)
       instance.type = validated_data.get('type', instance.type)
       instance.body = validated_data.get('body', instance.body)
       instance.media = validated_data.get('media', instance.media)
       instance.fromMe = validated_data.get('fromMe', instance.fromMe)
       instance.self = validated_data.get('self', instance.self)
       instance.isForwarded = validated_data.get('isForwarded', instance.isForwarded)
       instance.isMentioned = validated_data.get('isMentioned', instance.isMentioned)
       instance.quotedMsg = validated_data.get('quotedMsg', instance.quotedMsg)
       instance.mentionedIds = validated_data.get('mentionedIds', instance.mentionedIds)
       instance.time = validated_data.get('time', instance.time)
       instance.save()
       return instance