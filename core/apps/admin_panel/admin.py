from asgiref.sync import async_to_sync
from django.contrib import admin
from django.contrib.auth.models import Group
from nested_admin.nested import (
    NestedModelAdmin,
    NestedStackedInline,
)

from apps.admin_panel.permissons import AdminCanAddSitePermission
from apps.admin_panel.permissons.permissions import (
    AdminCanDeleteSitePermission,
)
from apps.landing.models import (
    About,
    AboutBlock,
    Advantage,
    ColorFont,
    Footer,
    MainScreen,
    OurResults,
    OurResultsPhoto,
    Service,
    ServiceDetail,
    Site,
)
from config.containers import get_container


admin.site.unregister(Group)


class AdvantageInline(NestedStackedInline):
    model = Advantage
    extra = 1


class ColorFontAdmin(admin.ModelAdmin):
    model = ColorFont
    list_display = [
        "color",
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ServiceDetailInline(NestedStackedInline):
    model = ServiceDetail
    extra = 1
    inlines = [
        AdvantageInline,
    ]


class ServiceInline(NestedStackedInline):
    model = Service
    extra = 1
    inlines = [
        ServiceDetailInline,
    ]
    list_display = ["name", "color_name", "discount_message"]


class MainScreenInline(NestedStackedInline):
    model = MainScreen
    can_delete = False
    max_num = 1


class AboutBlockInline(NestedStackedInline):
    model = AboutBlock
    extra = 1
    max_num = 3


class AboutInline(NestedStackedInline):
    model = About
    can_delete = False
    inlines = [
        AboutBlockInline,
    ]
    max_num = 1


class ResultProtoInline(NestedStackedInline):
    model = OurResultsPhoto
    extra = 1


class OurResultsInline(NestedStackedInline):
    model = OurResults
    inlines = [
        ResultProtoInline,
    ]
    max_num = 1
    can_delete = False


class FooterInline(NestedStackedInline):
    model = Footer
    max_num = 1
    can_delete = False


@admin.register(Site)
class SiteAdmin(NestedModelAdmin):
    inlines = [
        MainScreenInline,
        OurResultsInline,
        ServiceInline,
        AboutInline,
        FooterInline,
    ]

    def has_add_permission(self, request) -> bool:
        container = get_container()
        permission: AdminCanAddSitePermission = container.resolve(
            AdminCanAddSitePermission
        )
        return async_to_sync(permission.has_permission)()

    def has_delete_permission(self, request, obj=None) -> bool:
        container = get_container()
        permission: AdminCanDeleteSitePermission = container.resolve(
            AdminCanDeleteSitePermission
        )
        return async_to_sync(permission.has_permission)()


admin.site.register(ColorFont, ColorFontAdmin)
