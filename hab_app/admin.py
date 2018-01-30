from django.contrib import admin
from hab_app.models import *
from student_portal.models import *
from django.apps import apps
from import_export.admin import ImportExportModelAdmin
from import_export import resources

app = apps.get_app_config('hab_app')

for model_name, model in app.models.items():
    if model_name!="HostelRoom" and model_name!="HostelRoomOccupantRelation" and model_name!="HostelViewAccess" :

        if model_name[-4:] =="view":
            admin.site.register(model)


class SiangRoomResource(resources.ModelResource):
    class Meta:
        model = SiangRoom
        import_id_fields = ['roomNo',]
class SiangRoomAdmin(ImportExportModelAdmin):
    resource_class = SiangRoomResource
admin.site.register(SiangRoom,SiangRoomAdmin)

class BramhaputraRoomResource(resources.ModelResource):
    class Meta:
        model = BramhaputraRoom
        import_id_fields = ['roomNo',]
class BramhaputraRoomAdmin(ImportExportModelAdmin):
    resource_class = BramhaputraRoomResource
admin.site.register(BramhaputraRoom,BramhaputraRoomAdmin)

class DibangRoomResource(resources.ModelResource):
    class Meta:
        model = DibangRoom
        import_id_fields = ['roomNo',]
class DibangRoomAdmin(ImportExportModelAdmin):
    resource_class = DibangRoomResource
admin.site.register(DibangRoom,DibangRoomAdmin)

class DihingRoomResource(resources.ModelResource):
    class Meta:
        model = DihingRoom
        import_id_fields = ['roomNo',]
class DihingRoomAdmin(ImportExportModelAdmin):
    resource_class = DihingRoomResource
admin.site.register(DihingRoom,DihingRoomAdmin)

class KapiliRoomResource(resources.ModelResource):
    class Meta:
        model = KapiliRoom
        import_id_fields = ['roomNo',]
class KapiliRoomAdmin(ImportExportModelAdmin):
    resource_class = KapiliRoomResource
admin.site.register(KapiliRoom,KapiliRoomAdmin)

class UmiamRoomResource(resources.ModelResource):
    class Meta:
        model = UmiamRoom
        import_id_fields = ['roomNo',]
class UmiamRoomAdmin(ImportExportModelAdmin):
    resource_class = UmiamRoomResource
admin.site.register(UmiamRoom,UmiamRoomAdmin)


class LohitRoomResource(resources.ModelResource):
    class Meta:
        model = LohitRoom
        import_id_fields = ['roomNo',]
class LohitRoomAdmin(ImportExportModelAdmin):
    resource_class = LohitRoomResource
admin.site.register(LohitRoom,LohitRoomAdmin)

class BarakRoomResource(resources.ModelResource):
    class Meta:
        model = BarakRoom
        import_id_fields = ['roomNo',]
class BarakRoomAdmin(ImportExportModelAdmin):
    resource_class = BarakRoomResource
admin.site.register(BarakRoom,BarakRoomAdmin)

class KamengRoomResource(resources.ModelResource):
    class Meta:
        model = KamengRoom
        import_id_fields = ['roomNo',]
class KamengRoomAdmin(ImportExportModelAdmin):
    resource_class = KamengRoomResource
admin.site.register(KamengRoom,KamengRoomAdmin)

class ManasRoomResource(resources.ModelResource):
    class Meta:
        model = ManasRoom
        import_id_fields = ['roomNo',]
class ManasRoomAdmin(ImportExportModelAdmin):
    resource_class = ManasRoomResource
admin.site.register(ManasRoom,ManasRoomAdmin)

class DhansiriRoomResource(resources.ModelResource):
    class Meta:
        model = DhansiriRoom
        import_id_fields = ['roomNo',]
class DhansiriRoomAdmin(ImportExportModelAdmin):
    resource_class = DhansiriRoomResource
admin.site.register(DhansiriRoom,DhansiriRoomAdmin)

class SubansiriRoomResource(resources.ModelResource):
    class Meta:
        model = SubansiriRoom
        import_id_fields = ['roomNo',]
class SubansiriRoomAdmin(ImportExportModelAdmin):
    resource_class = SubansiriRoomResource
admin.site.register(SubansiriRoom,SubansiriRoomAdmin)







class OccupantDetailsResource(resources.ModelResource):
    class Meta:
        model = OccupantDetails
        import_id_fields = ['name',]
class OccupantDetailsAdmin(ImportExportModelAdmin):
    resource_class = OccupantDetailsResource
admin.site.register(OccupantDetails,OccupantDetailsAdmin)







class SiangRORelationResource(resources.ModelResource):
    class Meta:
        model = SiangRORelation
        import_id_fields = ['occupantId',]
class SiangRORelationAdmin(ImportExportModelAdmin):
    resource_class = SiangRORelationResource
admin.site.register(SiangRORelation,SiangRORelationAdmin)

class BramhaputraRORelationResource(resources.ModelResource):
    class Meta:
        model = BramhaputraRORelation
        import_id_fields = ['occupantId',]
class BramhaputraRORelationAdmin(ImportExportModelAdmin):
    resource_class = BramhaputraRORelationResource
admin.site.register(BramhaputraRORelation,BramhaputraRORelationAdmin)

class DibangRORelationResource(resources.ModelResource):
    class Meta:
        model = DibangRORelation
        import_id_fields = ['occupantId',]
class DibangRORelationAdmin(ImportExportModelAdmin):
    resource_class = DibangRORelationResource
admin.site.register(DibangRORelation,DibangRORelationAdmin)

class DihingRORelationResource(resources.ModelResource):
    class Meta:
        model = DihingRORelation
        import_id_fields = ['occupantId',]
class DihingRORelationAdmin(ImportExportModelAdmin):
    resource_class = DihingRORelationResource
admin.site.register(DihingRORelation,DihingRORelationAdmin)

class KapiliRORelationResource(resources.ModelResource):
    class Meta:
        model = KapiliRORelation
        import_id_fields = ['occupantId',]
class KapiliRORelationAdmin(ImportExportModelAdmin):
    resource_class = KapiliRORelationResource
admin.site.register(KapiliRORelation,KapiliRORelationAdmin)

class UmiamRORelationResource(resources.ModelResource):
    class Meta:
        model = UmiamRORelation
        import_id_fields = ['occupantId',]
class UmiamRORelationAdmin(ImportExportModelAdmin):
    resource_class = UmiamRORelationResource
admin.site.register(UmiamRORelation,UmiamRORelationAdmin)


class LohitRORelationResource(resources.ModelResource):
    class Meta:
        model = LohitRORelation
        import_id_fields = ['occupantId',]
class LohitRORelationAdmin(ImportExportModelAdmin):
    resource_class = LohitRORelationResource
admin.site.register(LohitRORelation,LohitRORelationAdmin)

class BarakRORelationResource(resources.ModelResource):
    class Meta:
        model = BarakRORelation
        import_id_fields = ['occupantId',]
class BarakRORelationAdmin(ImportExportModelAdmin):
    resource_class = BarakRORelationResource
admin.site.register(BarakRORelation,BarakRORelationAdmin)

class KamengRORelationResource(resources.ModelResource):
    class Meta:
        model = KamengRORelation
        import_id_fields = ['occupantId',]
class KamengRORelationAdmin(ImportExportModelAdmin):
    resource_class = KamengRORelationResource
admin.site.register(KamengRORelation,KamengRORelationAdmin)

class ManasRORelationResource(resources.ModelResource):
    class Meta:
        model = ManasRORelation
        import_id_fields = ['occupantId',]
class ManasRORelationAdmin(ImportExportModelAdmin):
    resource_class = ManasRORelationResource
admin.site.register(ManasRORelation,ManasRORelationAdmin)

class DhansiriRORelationResource(resources.ModelResource):
    class Meta:
        model = DhansiriRORelation
        import_id_fields = ['occupantId',]
class DhansiriRORelationAdmin(ImportExportModelAdmin):
    resource_class = DhansiriRORelationResource
admin.site.register(DhansiriRORelation,DhansiriRORelationAdmin)

class SubansiriRORelationResource(resources.ModelResource):
    class Meta:
        model = SubansiriRORelation
        import_id_fields = ['occupantId',]

class SubansiriRORelationAdmin(ImportExportModelAdmin):
    resource_class = SubansiriRORelationResource
admin.site.register(SubansiriRORelation,SubansiriRORelationAdmin)


#Automation
@admin.register(FinalPreference)
class FinalPreferenceAdmin(ImportExportModelAdmin):
    pass


admin.site.register(AllHostelMetaData)
admin.site.register(RoomCategory)
admin.site.register(OccupantCategory)
admin.site.register(UpcomingOccupantRequest)
admin.site.register(UpcomingOccupant)
admin.site.register(Log_Table)
admin.site.register(Log_Table2)
admin.site.register(Login)
admin.site.register(ChrViewAccess)
admin.site.register(Automation)
admin.site.register(TemporaryDetails)
