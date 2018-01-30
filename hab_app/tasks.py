# # Create your tasks here
# from __future__ import absolute_import, unicode_literals
# from celery import shared_task
# from celery.task.schedules import crontab
# from celery.decorators import periodic_task
# from django.shortcuts import redirect
# from django.http import HttpResponseRedirect,HttpResponse
# from django.shortcuts import render,redirect
# from hab_app.utils import opi_calculate
#
#
# @periodic_task(
#     run_every=(crontab(minute='*/1')),
#     name="task_opi_calculate",
#     ignore_result=True
# )
# def task_opi_calculate():
#     opi_calculate()
