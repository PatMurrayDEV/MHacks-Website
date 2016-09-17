from MHacks.models import ScanEvent as ScanEventModel
from MHacks.v1.serializers import ScanEventSerializer
from MHacks.v1.util import GenericListCreateModel, GenericUpdateDestroyModel


class ScanEvents(GenericListCreateModel):
    """
    Announcements are what send push notifications and are useful for pushing updates to MHacks participants.
    Anybody who is logged in can make a GET request where as only authorized users can create, update and delete them.
    """
    serializer_class = ScanEventSerializer
    query_set = ScanEventModel.objects.none()

    def get_queryset(self):
        date_last_updated = super(ScanEvents, self).get_queryset()
        if date_last_updated:
            query_set = ScanEventModel.objects.all().filter(last_updated__gte=date_last_updated)
        else:
            query_set = ScanEventModel.objects.all().filter(deleted=False)

        return query_set


class ScanEvent(GenericUpdateDestroyModel):
    serializer_class = ScanEventSerializer
    queryset = ScanEventModel.objects.all()
