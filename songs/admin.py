from django.contrib import admin
import nested_admin
from songs.models import Song, Setlist, Set, SetSong


class SongAdmin(admin.ModelAdmin):
    pass


class SetSongInline(nested_admin.NestedStackedInline):
    model = SetSong
    sortable_field_name = "order"
    extra = 0


class SetlistSetInline(nested_admin.NestedTabularInline):
    model = Set
    sortable_field_name = "order"
    extra = 0
    inlines = (SetSongInline,)


class SetlistAdmin(nested_admin.NestedModelAdmin):
    inlines = (SetlistSetInline,)


admin.site.register(Setlist, SetlistAdmin)
