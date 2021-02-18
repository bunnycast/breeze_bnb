from django.contrib import admin

from conversations.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """ Conversation Admin Definition """
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message Admin Definition """
    pass
