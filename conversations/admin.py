from django.contrib import admin

from conversations.models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """ Conversation Admin Definition """

    list_display = ('__str__', 'count_messages', 'count_participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """ Message Admin Definition """

    list_display = ('__str__', 'created_at')
