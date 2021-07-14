from django.contrib import admin
from songs.models import Setlist, SetlistSong, Song


class SongAdmin(admin.ModelAdmin):
    pass


class SetlistSongInline(admin.TabularInline):
    model = SetlistSong
    extra = 1


class SetlistAdmin(admin.ModelAdmin):
    inlines = (SetlistSongInline,)


admin.site.register(Song, SongAdmin)
admin.site.register(Setlist, SetlistAdmin)
