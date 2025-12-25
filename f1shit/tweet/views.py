from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse

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
            tweet.save()

            if tweet.post_type == "POLL":
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

    return render(request, "tweet/tweet_form.html", {"form": form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)

    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")

    return render(request, "tweet/tweet_confirm_delete.html", {"tweet": tweet})


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
    tweet = get_object_or_404(Tweet, id=tweet_id)

    Reaction.objects.get_or_create(
        user=request.user,
        tweet=tweet,
        reaction_type=reaction_type
    )

    return redirect("tweet_list")


# ===========================
# AJAX
# ===========================

def get_drivers_by_team(request):
    team_id = request.GET.get("team_id")
    drivers = Driver.objects.filter(team_id=team_id).values("id", "name")
    return JsonResponse(list(drivers), safe=False)


# ===========================
# PROFILE
# ===========================

def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    tweets = Tweet.objects.filter(user=profile_user).order_by("-created_at")

    return render(request, "tweet/profile.html", {
        "profile_user": profile_user,
        "tweets": tweets,
    })