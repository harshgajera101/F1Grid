from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import models

from .models import (
    Tweet, Reaction, Team, Driver,
    RaceWeekend, Poll, PollOption, PollVote
)
from .forms import TweetForm, UserRegisterForm, PollOptionForm


# ===========================
# HOME / FEED
# ===========================

def tweet_list(request):
    tweets = Tweet.objects.all().order_by("-created_at")

    # Filters
    post_type = request.GET.get("type")
    team = request.GET.get("team")
    driver = request.GET.get("driver")

    if post_type:
        tweets = tweets.filter(post_type=post_type)
    if team:
        tweets = tweets.filter(team__id=team)
    if driver:
        tweets = tweets.filter(driver__id=driver)

    # Race weekend
    race_weekend = RaceWeekend.objects.first()

    # Poll voting state
    if request.user.is_authenticated:
        user_votes = PollVote.objects.filter(user=request.user)
        voted_poll_ids = {vote.option.poll_id for vote in user_votes}
    else:
        voted_poll_ids = set()

    for tweet in tweets:
        if hasattr(tweet, "poll"):
            tweet.poll.has_voted = tweet.poll.id in voted_poll_ids

    context = {
        "tweets": tweets,
        "post_types": Tweet.POST_TYPE_CHOICES,
        "teams": Team.objects.all(),
        "drivers": Driver.objects.all(),
        "race_weekend": race_weekend,
    }

    return render(request, "tweet_list.html", context)


# ===========================
# CREATE / EDIT / DELETE
# ===========================

@login_required
def tweet_create(request):
    poll_form = PollOptionForm()

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        poll_form = PollOptionForm(request.POST)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet. save()

            if tweet.post_type == "POLL":
                # VALIDATE POLL FORM BEFORE ACCESSING cleaned_data
                if poll_form.is_valid():
                    options = [
                        poll_form.cleaned_data.get("option_1"),
                        poll_form.cleaned_data.get("option_2"),
                        poll_form.cleaned_data.get("option_3"),
                        poll_form.cleaned_data.get("option_4"),
                    ]   
                    options = [o for o in options if o]

                    if len(options) < 2:
                        messages.error(request, "Poll must have at least 2 options.")
                        tweet.delete()
                        return redirect("tweet_create")

                    poll = Poll.objects.create(tweet=tweet)

                    for opt in options:
                        PollOption.objects.create(poll=poll, text=opt)
                else:
                    # If poll form is invalid, delete tweet and show error
                    messages.error(request, "Please fill in poll options correctly.")
                    tweet.delete()
                    return redirect("tweet_create")

            return redirect("tweet_list")

    else:
        form = TweetForm()

    return render(request, "tweet_form.html", {
        "form": form,
        "poll_form": poll_form,
    })


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweet_form.html", {"form": form})  # CHANGED THIS


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request. user)

    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")

    return render(request, "tweet_confirm_delete.html", {"tweet": tweet})  # CHANGED THIS


# ===========================
# AUTH
# ===========================

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserRegisterForm()

    return render(request, "registration/register.html", {"form": form})


# ===========================
# POLL VOTING (CORRECT)
# ===========================

@login_required
def poll_vote(request, option_id):
    if request.method != "POST":
        return redirect("tweet_list")

    option = get_object_or_404(PollOption, id=option_id)

    already_voted = PollVote.objects.filter(
        user=request.user,
        option__poll=option.poll
    ).exists()

    if not already_voted:
        PollVote.objects.create(
            user=request.user,
            option=option
        )

    return redirect("tweet_list")


# ===========================
# REACTIONS
# ===========================

@login_required
def react_to_tweet(request, tweet_id, reaction_type):
    if request.method != "POST":
        return redirect("tweet_list")
    
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    # Check if user already reacted to this tweet
    existing_reaction = Reaction.objects.filter(user=request.user, tweet=tweet).first()
    
    if existing_reaction:
        # If user clicked the same reaction, remove it (toggle off)
        if existing_reaction.reaction_type == reaction_type:
            existing_reaction.delete()
        else:
            # User clicked a different reaction, update it
            existing_reaction.reaction_type = reaction_type
            existing_reaction.save()
    else:
        # Create new reaction
        Reaction.objects.create(
            user=request.user,
            tweet=tweet,
            reaction_type=reaction_type
        )
    
    return redirect("tweet_list")


# ===========================
# AJAX
# ===========================


def get_drivers_by_team(request):
    team_id = request. GET.get("team_id")
    if team_id:
        drivers = Driver.objects.filter(team_id=team_id).values("id", "name")
    else:
        drivers = Driver. objects.all().values("id", "name")
    return JsonResponse(list(drivers), safe=False)


# ===========================
# PROFILE
# ===========================

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=profile_user).order_by("-created_at")
    
    # Calculate stats
    total_posts = tweets.count()
    total_polls = tweets.filter(post_type='POLL').count()
    total_reactions = Reaction.objects.filter(tweet__user=profile_user).count()
    
    # Get favorite team and driver (most posted about)
    favorite_team = tweets.exclude(team=None).values('team__name').annotate(
        count=models.Count('team')
    ).order_by('-count').first()
    
    favorite_driver = tweets.exclude(driver=None).values('driver__name').annotate(
        count=models.Count('driver')
    ).order_by('-count').first()
    
    # Post type breakdown
    post_breakdown = {}
    for code, label in Tweet.POST_TYPE_CHOICES:
        post_breakdown[label] = tweets.filter(post_type=code).count()
    
    # Recent activity (last 7 days)
    from datetime import timedelta
    from django.utils import timezone
    last_week = timezone.now() - timedelta(days=7)
    recent_activity = tweets.filter(created_at__gte=last_week).count()
    
    # Member since
    member_since = profile_user.date_joined
    
    context = {
        "profile_user": profile_user,
        "tweets": tweets,
        "total_posts": total_posts,
        "total_polls": total_polls,
        "total_reactions": total_reactions,
        "favorite_team": favorite_team['team__name'] if favorite_team else "None yet",
        "favorite_driver":  favorite_driver['driver__name'] if favorite_driver else "None yet",
        "post_breakdown":  post_breakdown,
        "recent_activity": recent_activity,
        "member_since": member_since,
    }
    
    return render(request, "tweet/profile.html", context)