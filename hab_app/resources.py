from import_export import resources
from student_portal.models import *
from hab_app.models import *
class MessFeedbackResource(resources.ModelResource):
    class Meta:
        model = MessFeedback

class PreferenceResource(resources.ModelResource):
    class Meta:
        model = Preference

class FinalPreferenceResource(resources.ModelResource):
    class Meta:
        model = FinalPreference
        import_id_fields = ['hostelName','username','month','year','final_hostel']
class FreshersBulkAllotResource(resources.ModelResource):
    class Meta:
        model = UpcomingOccupant
