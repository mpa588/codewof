"""Utility functions for codeWOF system. Involves points, badges, and backdating points and badges per user."""

import datetime
import json
import logging
from dateutil.relativedelta import relativedelta

from programming.models import (
    Profile,
    Question,
    Attempt,
    Badge,
    Earned,
)
from django.http import JsonResponse
from django.conf import settings

time_zone = settings.TIME_ZONE

logger = logging.getLogger(__name__)
del logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'incremental': True,
    'root': {
        'level': 'DEBUG',
    },
}


def add_points(question, profile, attempt):
    """
    Add appropriate number of points (if any) to user's profile after a question is answered.

    Adds 10 points to a user's profile for when the user answers a question correctly for the first time. If the user
    answers the question correctly the first time they answer, the user gains two bonus points, as checked with the
    variable "is_first_correct".
    """
    num_attempts = Attempt.objects.filter(question=question, profile=profile)
    is_first_correct = len(Attempt.objects.filter(question=question, profile=profile, passed_tests=True)) == 1
    logger.warning(num_attempts)
    logger.warning(is_first_correct)
    points_to_add = 0

    # check if first passed
    if attempt.passed_tests and is_first_correct:
        points_to_add += 10
        if len(num_attempts) == 1:
            # correct first try
            points_to_add += 2

    profile.points += points_to_add
    profile.full_clean()
    profile.save()
    return profile.points


def save_goal_choice(request):
    """Update user's goal choice in database."""
    request_json = json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        user = request.user
        profile = user.profile

        goal_choice = request_json['goal_choice']
        profile.goal = int(goal_choice)
        profile.full_clean()
        profile.save()

    return JsonResponse({})


def get_days_consecutively_answered(user):
    """
    Get the number of consecutive days with questions attempted.

    Gets all datetimes of attempts for the given user's profile, and checks for the longest continuous "streak" of
    days where attempts were made. Returns an integer of the longest attempt "streak".
    """
    # get datetimes from attempts in date form)
    attempts = Attempt.objects.filter(profile=user.profile).datetimes('datetime', 'day', 'DESC')
    # get current day as date
    i = 0
    today = datetime.datetime.now().replace(tzinfo=None).date()

    while i < len(attempts):
        attempt = attempts[i]
        expected_date = today - datetime.timedelta(days=i)
        if attempt.date() != expected_date:
            break
        i += 1

    return i


def get_questions_answered_in_past_month(user):
    """Get the number questions successfully answered in the past month."""
    today = datetime.datetime.now().replace(tzinfo=None) + relativedelta(days=1)
    last_month = today - relativedelta(months=1)
    solved = Attempt.objects.filter(profile=user.profile, datetime__gte=last_month.date(), passed_tests=True)
    return len(solved)


def check_badge_conditions(user):
    """
    Check if the user has earned new badges for their profile.

    Checks if the user has received each available badge. If not, check if the user has earned these badges. Badges
    available to be checked for are profile creation, numebr of attempts made, number of questions answered, and
    number of days with consecutive attempts.
    """
    earned_badges = user.profile.earned_badges.all()
    new_badge_names = ""
    new_badge_objects = []
    # account creation badge
    try:
        creation_badge = Badge.objects.get(id_name="create-account")
        if creation_badge not in earned_badges:
            # create a new account creation
            new_achievement = Earned(profile=user.profile, badge=creation_badge)
            new_achievement.full_clean()
            new_achievement.save()
            new_badge_names = new_badge_names + "- " + creation_badge.display_name + "\n"
            new_badge_objects.append(creation_badge)
    except Badge.DoesNotExist:
        logger.warning("No such badge: create-account")
        pass

    # check questions solved badges
    try:
        question_badges = Badge.objects.filter(id_name__contains="questions-solved")
        solved = Attempt.objects.filter(profile=user.profile, passed_tests=True)
        for question_badge in question_badges:
            if question_badge not in earned_badges:
                num_questions = int(question_badge.id_name.split("-")[2])
                if len(solved) >= num_questions:
                    new_achievement = Earned(profile=user.profile, badge=question_badge)
                    new_achievement.full_clean()
                    new_achievement.save()
                    new_badge_names = new_badge_names + "- " + question_badge.display_name + "\n"
                    new_badge_objects.append(question_badge)
    except Badge.DoesNotExist:
        logger.warning("No such badges: questions-solved")
        pass

    # checked questions attempted badges
    try:
        attempt_badges = Badge.objects.filter(id_name__contains="attempts-made")
        attempted = Attempt.objects.filter(profile=user.profile)
        for attempt_badge in attempt_badges:
            if attempt_badge not in earned_badges:
                num_questions = int(attempt_badge.id_name.split("-")[2])
                if len(attempted) >= num_questions:
                    new_achievement = Earned(profile=user.profile, badge=attempt_badge)
                    new_achievement.full_clean()
                    new_achievement.save()
                    new_badge_names = new_badge_names + "- " + attempt_badge.display_name + "\n"
                    new_badge_objects.append(attempt_badge)
    except Badge.DoesNotExist:
        logger.warning("No such badges: attempts-made")
        pass

    # consecutive days logged in badges
    num_consec_days = -1
    consec_badges = Badge.objects.filter(id_name__contains="consecutive-days")
    for consec_badge in consec_badges:
        if consec_badge not in earned_badges:
            if num_consec_days == -1:
                num_consec_days = get_days_consecutively_answered(user)
            n_days = int(consec_badge.id_name.split("-")[2])
            if n_days == num_consec_days:
                new_achievement = Earned(profile=user.profile, badge=consec_badge)
                new_achievement.full_clean()
                new_achievement.save()
                new_badge_names = new_badge_names + "- " + consec_badge.display_name + "\n"
                new_badge_objects.append(consec_badge)

    calculate_badge_points(user, new_badge_objects)
    return new_badge_names


def calculate_badge_points(user, badges):
    """Calculate points earned by the user for new badges earned by multiplying the badge tier by 10."""
    for badge in badges:
        points = badge.badge_tier * 10
        user.profile.points += points
    user.full_clean()
    user.save()


def backdate_points_and_badges():
    """Perform backdate of all points and badges for each profile in the system."""
    profiles = Profile.objects.all()
    for profile in profiles:
        profile = backdate_badges(profile)
        profile = backdate_points(profile)
        # save profile when update is completed
        profile.full_clean()
        profile.save()


def backdate_points(profile):
    """Re-calculate points for the user profile."""
    questions = Question.objects.all()
    profile.points = 0
    for question in questions:
        has_passed = len(Attempt.objects.filter(profile=profile, question=question, passed_tests=True)) > 0
        user_attempts = Attempt.objects.filter(profile=profile, question=question)
        first_passed = False
        if len(user_attempts) > 0:
            first_passed = user_attempts[0].passed_tests
        if has_passed:
            profile.points += 10
        if first_passed:
            profile.points += 1
    return profile


def backdate_badges(profile):
    """Re-check the profile for badges earned."""
    check_badge_conditions(profile.user)
    return profile
