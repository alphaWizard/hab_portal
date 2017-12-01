from django.contrib import admin
from hab_app.models import *
from django.apps import apps
from import_export.admin import ImportExportModelAdmin
from import_export import resources

app = apps.get_app_config('hab_app')



for model_name, model in app.models.items():
    if model_name!="HostelRoom" and model_name!="HostelRoomOccupantRelation" and model_name!="HostelViewAccess" :

        if model_name !="siangroom":
            admin.site.register(model)
class SiangRoomResource(resources.ModelResource):
    class Meta:
        model = SiangRoom
        import_id_fields = ['roomNo',]
class SiangRoomAdmin(ImportExportModelAdmin):
    resource_class = SiangRoomResource
admin.site.register(SiangRoom,SiangRoomAdmin)
