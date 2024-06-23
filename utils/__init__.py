import uuid
import re


def hexid():
    return uuid.uuid4().hex


def is_valid_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


# This function determines the grade based on the score.
def get_grade(score):
    print(score, type(score))
    # The if statement checks the score and assigns the grade
    # if the score is greater than or equal to 80, the grade is A
    if score >= 80:
        return 'A'
    # if the score is greater than or equal to 65, the grade is B
    elif score >= 65:
        return 'B'
    # if the score is greater than or equal to 55, the grade is C
    elif score >= 55:
        return 'C'
    # if the score is greater than or equal to 40, the grade is D
    elif score >= 40:
        return 'D'
    # if the score is less than 40, the grade is F
    else:
        return 'F'


# This function calculates the GPA based on the scores and units.
def calculate_gpa(scores, units):
    # The total_grade_points variable holds the sum of the grade points
    total_grade_points = 0
    # The total_credits variable holds the sum of the units
    total_credits = 0

    # The for loop iterates through the scores and units list
    for i in range(len(scores)):
        # The if statement checks the score and assigns the grade points
        # if the score is greater than or equal to 80, the grade points is 4.0
        if scores[i] >= 80:
            grade_points = 5.0
        # if the score is greater than or equal to 65, the grade points is 3.0
        elif scores[i] >= 65:
            grade_points = 4.0
        # if the score is greater than or equal to 55, the grade points is 2.0
        elif scores[i] >= 55:
            grade_points = 3.0
        # if the score is greater than or equal to 40, the grade points is 1.0
        elif scores[i] >= 40:
            grade_points = 2.0
        # if the score is less than 40, the grade points is 0.0
        else:
            grade_points = 1.0

        # The total_grade_points is the sum of the grade points multiplied by the units
        total_grade_points += grade_points * units[i]
        # The total_credits is the sum of the units
        total_credits += units[i]

    # The gpa variable holds the total_grade_points divided by the total_credits
    # The round function rounds the gpa to 2 decimal places
    gpa = round(total_grade_points / total_credits, 2)
    # The gpa is returned
    return gpa
