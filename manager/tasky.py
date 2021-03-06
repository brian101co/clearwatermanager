from datetime import date, timedelta
from django.conf import settings
from twilio.rest import Client
from models import Customer


today = date.today()
tomorrow = today + timedelta(days = 2)
notifications = Customer.objects.filter(end__range=[today, tomorrow]).all().values('title', 'end', 'site')
notification_list = list(notifications)

if len(notification_list) != 0:
    for notification in notification_list:
        message_to_broadcast = f"{ notification['title'] } is checking out on { notification['end'].strftime('%m/%d/%Y') }. Site No: { notification['site'] }"
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        for recipient in settings.SMS_BROADCAST_TO_NUMBERS:
            if recipient:
                client.messages.create(to=recipient,
                                    from_=settings.TWILIO_NUMBER,
                                    body=message_to_broadcast)