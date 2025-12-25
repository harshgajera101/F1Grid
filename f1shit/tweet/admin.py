from django.contrib import admin
from .models import Tweet, Team, Driver, Reaction, RaceWeekend, Poll, PollOption, PollVote


admin.site.register(Tweet)
admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(Reaction)
admin.site.register(RaceWeekend)
admin.site.register(Poll)
admin.site.register(PollOption)
admin.site.register(PollVote)