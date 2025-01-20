from django.shortcuts import render


def update_data_sharing(user):
    if user.age >= 15:
        user.can_data_be_shared = True
        user.save()
