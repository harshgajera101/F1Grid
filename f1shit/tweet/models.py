from django.db import models
from django.contrib.auth.models import User

# ---------------------------
# F1 DOMAIN MODELS
# ---------------------------

class Team(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, help_text="Hex color code, e.g. #FF0000")

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="drivers")

    def __str__(self):
        return self.name


# ---------------------------
# POST MODEL (EXTENDED TWEET)
# ---------------------------

class Tweet(models.Model):

    POST_TYPE_CHOICES = [
        ('RACE', 'Race Update'),
        ('NEWS', 'Breaking News'),
        ('OPINION', 'Opinion'),
        ('MEME', 'Meme'),
        ('POLL', 'Poll'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES,
        default='OPINION'
    )

    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def fast_lap_count(self):
        return self.reactions.filter(reaction_type='FAST_LAP').count()

    def push_count(self):
        return self.reactions.filter(reaction_type='PUSH').count()

    def team_order_count(self):
       return self.reactions.filter(reaction_type='TEAM').count()

    def champ_count(self):
        return self.reactions.filter(reaction_type='CHAMP').count()

    def __str__(self):
        return f"{self.user.username} | {self.post_type} | {self.text[:20]}"


# ---------------------------
# REACTIONS (NO COMMENTS)
# ---------------------------

class Reaction(models.Model):

    REACTION_CHOICES = [
        ('FAST_LAP', '🔥 Fastest Lap'),
        ('PUSH', '🏎️ Push Push'),
        ('TEAM', '😤 Team Orders'),
        ('CHAMP', '🏆 Champion Move'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="reactions")
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet', 'reaction_type')

    def __str__(self):
        return f"{self.user.username} → {self.reaction_type}"



# ---------------------------
# Race Weekend
# ---------------------------

class RaceWeekend(models.Model):
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Race Weekend Mode"



# ---------------------------
# POLL MODELS
# ---------------------------

class Poll(models.Model):
    tweet = models.OneToOneField(
        Tweet,
        on_delete=models.CASCADE,
        related_name="poll"
    )

    def __str__(self):
        return f"Poll for Tweet {self.tweet.id}"

    @property
    def total_votes(self):
        return PollVote.objects.filter(option__poll=self).count()


class PollOption(models.Model):
    poll = models.ForeignKey(
        Poll,
        related_name="options",
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

    @property
    def votes_count(self):
        return self.votes.count()

    @property
    def vote_percent(self):
        total = self.poll.total_votes
        return int((self.votes_count / total) * 100) if total > 0 else 0


class PollVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(
        PollOption,
        related_name="votes",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "option")

    def __str__(self):
        return f"{self.user.username} → {self.option.text}"