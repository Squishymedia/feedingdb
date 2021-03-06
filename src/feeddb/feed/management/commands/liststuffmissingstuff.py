from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from feeddb.feed.models import Trial, EmgSensor, SonoSensor

class Command(BaseCommand):
    args = ''
    help = 'help'

    def handle(self, *args, **options):
        print "Trials missing OWL behavior:"
        for t in trials_missing_behaviorowl():
            print "  %d: %s" % (t.id, t)
            try:
                pk = t.behavior_primary.pk
            except AttributeError:
                pk = 0
            print "      behavior_primary: '%s' pk=%d" % (t.behavior_primary, pk)
            print "  %s" % (t.get_absolute_url())

        print "Sensors missing muscle:"
        for typename, s in sensors_missing_muscle():
            print "  %d: %s (%s)" % (s.id, s, typename)
            try:
                pk = s.location_controlled.pk
            except:
                pk = 0
            print "      location_controlled: '%s' (pk=%d)" % (s.location_controlled, pk)
            print "  %s" % (s.get_absolute_url())

def trials_missing_behaviorowl():
    return Trial.objects.filter(behaviorowl_primary__isnull=True).select_related('behavior_primary')

def sensors_missing_muscle():
    for emgsensor in EmgSensor.objects.filter(muscle__isnull=True).select_related('location_controlled'):
        yield ('EMG', emgsensor)
    for sonosensor in SonoSensor.objects.filter(muscle__isnull=True).select_related('location_controlled'):
        yield ('Sono', sonosensor)
