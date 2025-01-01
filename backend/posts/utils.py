from django.utils.timesince import timesince

def format_time(date_time):
    time = timesince(date_time)
    return time.split(',')[0]