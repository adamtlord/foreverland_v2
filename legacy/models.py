# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AhmFiles(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255L)
    description = models.TextField()
    file = models.CharField(max_length=255L)
    password = models.CharField(max_length=40L)
    download_count = models.IntegerField()
    access = models.CharField(max_length=6L)
    show_counter = models.IntegerField()
    link_label = models.CharField(max_length=255L)
    class Meta:
        db_table = 'ahm_files'

class WpBwbpsCategories(models.Model):
    id = models.BigIntegerField(primary_key=True)
    image_id = models.BigIntegerField()
    category_id = models.BigIntegerField(null=True, blank=True)
    tag_name = models.CharField(max_length=250L, blank=True)
    updated_date = models.DateTimeField()
    class Meta:
        db_table = 'wp_bwbps_categories'

class WpBwbpsCustomdata(models.Model):
    id = models.IntegerField(primary_key=True)
    image_id = models.IntegerField()
    updated_date = models.DateTimeField()
    bwbps_status = models.IntegerField()
    class Meta:
        db_table = 'wp_bwbps_customdata'

class WpBwbpsFavorites(models.Model):
    favorite_id = models.BigIntegerField(primary_key=True)
    image_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    updated_date = models.DateTimeField()
    class Meta:
        db_table = 'wp_bwbps_favorites'

class WpBwbpsFields(models.Model):
    field_id = models.IntegerField(primary_key=True)
    form_id = models.IntegerField()
    field_name = models.CharField(max_length=50L, blank=True)
    label = models.CharField(max_length=255L, blank=True)
    type = models.IntegerField(null=True, blank=True)
    numeric_field = models.IntegerField()
    multi_val = models.IntegerField()
    default_val = models.CharField(max_length=255L, blank=True)
    auto_capitalize = models.IntegerField(null=True, blank=True)
    keyboard_type = models.IntegerField(null=True, blank=True)
    html_filter = models.IntegerField(null=True, blank=True)
    date_format = models.IntegerField(null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    class Meta:
        db_table = 'wp_bwbps_fields'

class WpBwbpsForms(models.Model):
    form_id = models.IntegerField(primary_key=True)
    form_name = models.CharField(max_length=30L, blank=True)
    form = models.TextField(blank=True)
    css = models.TextField(blank=True)
    fields_used = models.TextField(blank=True)
    category = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'wp_bwbps_forms'

class WpBwbpsGalleries(models.Model):
    gallery_id = models.BigIntegerField(primary_key=True)
    post_id = models.BigIntegerField(null=True, blank=True)
    gallery_name = models.CharField(max_length=255L, blank=True)
    gallery_description = models.TextField(blank=True)
    gallery_type = models.IntegerField()
    caption = models.TextField(blank=True)
    add_text = models.CharField(max_length=255L, blank=True)
    upload_form_caption = models.CharField(max_length=255L, blank=True)
    contrib_role = models.IntegerField()
    anchor_class = models.CharField(max_length=255L, blank=True)
    img_count = models.BigIntegerField(null=True, blank=True)
    img_rel = models.CharField(max_length=255L, blank=True)
    img_class = models.CharField(max_length=255L, blank=True)
    img_perrow = models.IntegerField(null=True, blank=True)
    img_perpage = models.IntegerField(null=True, blank=True)
    mini_aspect = models.IntegerField(null=True, blank=True)
    mini_width = models.IntegerField(null=True, blank=True)
    mini_height = models.IntegerField(null=True, blank=True)
    thumb_aspect = models.IntegerField(null=True, blank=True)
    thumb_width = models.IntegerField(null=True, blank=True)
    thumb_height = models.IntegerField(null=True, blank=True)
    medium_aspect = models.IntegerField(null=True, blank=True)
    medium_width = models.IntegerField(null=True, blank=True)
    medium_height = models.IntegerField(null=True, blank=True)
    image_aspect = models.IntegerField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    image_height = models.IntegerField(null=True, blank=True)
    show_caption = models.IntegerField(null=True, blank=True)
    nofollow_caption = models.IntegerField(null=True, blank=True)
    caption_template = models.CharField(max_length=255L, blank=True)
    show_imgcaption = models.IntegerField(null=True, blank=True)
    img_status = models.IntegerField(null=True, blank=True)
    allow_no_image = models.IntegerField(null=True, blank=True)
    suppress_no_image = models.IntegerField(null=True, blank=True)
    default_image = models.CharField(max_length=255L, blank=True)
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField()
    layout_id = models.IntegerField(null=True, blank=True)
    use_customform = models.IntegerField(null=True, blank=True)
    custom_formid = models.IntegerField(null=True, blank=True)
    use_customfields = models.IntegerField(null=True, blank=True)
    cover_imageid = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    sort_field = models.IntegerField(null=True, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    poll_id = models.IntegerField(null=True, blank=True)
    rating_position = models.IntegerField(null=True, blank=True)
    hide_toggle_ratings = models.IntegerField(null=True, blank=True)
    pext_insert_setid = models.IntegerField(null=True, blank=True)
    max_user_uploads = models.IntegerField(null=True, blank=True)
    uploads_period = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'wp_bwbps_galleries'

class WpBwbpsImageratings(models.Model):
    rating_id = models.BigIntegerField(primary_key=True)
    image_id = models.BigIntegerField()
    gallery_id = models.BigIntegerField(null=True, blank=True)
    poll_id = models.BigIntegerField(null=True, blank=True)
    user_id = models.BigIntegerField(null=True, blank=True)
    user_ip = models.CharField(max_length=30L, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=250L, blank=True)
    updated_date = models.DateTimeField()
    status = models.IntegerField()
    class Meta:
        db_table = 'wp_bwbps_imageratings'

class WpBwbpsImages(models.Model):
    image_id = models.BigIntegerField(primary_key=True)
    gallery_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    post_id = models.BigIntegerField(null=True, blank=True)
    comment_id = models.BigIntegerField(null=True, blank=True)
    image_name = models.CharField(max_length=250L, blank=True)
    image_caption = models.TextField(blank=True)
    file_type = models.IntegerField(null=True, blank=True)
    file_name = models.TextField(blank=True)
    file_url = models.TextField(blank=True)
    mini_url = models.TextField(blank=True)
    thumb_url = models.TextField(blank=True)
    medium_url = models.TextField(blank=True)
    image_url = models.TextField(blank=True)
    wp_attach_id = models.BigIntegerField(null=True, blank=True)
    url = models.CharField(max_length=250L, blank=True)
    custom_fields = models.TextField(blank=True)
    meta_data = models.TextField(blank=True)
    geolong = models.FloatField(null=True, blank=True)
    geolat = models.FloatField(null=True, blank=True)
    img_attribution = models.TextField(blank=True)
    img_license = models.IntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField()
    created_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField()
    status = models.IntegerField()
    alerted = models.IntegerField()
    seq = models.BigIntegerField()
    favorites_cnt = models.BigIntegerField(null=True, blank=True)
    avg_rating = models.FloatField()
    rating_cnt = models.BigIntegerField()
    votes_sum = models.BigIntegerField()
    votes_cnt = models.BigIntegerField()
    class Meta:
        db_table = 'wp_bwbps_images'

class WpBwbpsLayouts(models.Model):
    layout_id = models.IntegerField(primary_key=True)
    layout_name = models.CharField(max_length=30L, blank=True)
    layout_type = models.IntegerField()
    layout = models.TextField(blank=True)
    alt_layout = models.TextField(blank=True)
    wrapper = models.TextField(blank=True)
    cells_perrow = models.IntegerField()
    css = models.TextField(blank=True)
    pagination_class = models.CharField(max_length=255L, blank=True)
    lists = models.CharField(max_length=255L, blank=True)
    post_type = models.CharField(max_length=20L, blank=True)
    fields_used = models.TextField(blank=True)
    footer_layout = models.TextField(blank=True)
    class Meta:
        db_table = 'wp_bwbps_layouts'

class WpBwbpsLookup(models.Model):
    id = models.IntegerField(primary_key=True)
    field_id = models.IntegerField(null=True, blank=True)
    value = models.CharField(max_length=255L, blank=True)
    label = models.CharField(max_length=255L, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'wp_bwbps_lookup'

class WpBwbpsParams(models.Model):
    id = models.BigIntegerField(primary_key=True)
    param_group = models.CharField(max_length=20L, blank=True)
    param = models.CharField(max_length=100L, blank=True)
    num_value = models.FloatField(null=True, blank=True)
    text_value = models.CharField(max_length=255L, blank=True)
    user_ip = models.CharField(max_length=30L, blank=True)
    updated_date = models.DateTimeField()
    class Meta:
        db_table = 'wp_bwbps_params'

class WpBwbpsRatingssummary(models.Model):
    rating_id = models.BigIntegerField(primary_key=True)
    image_id = models.BigIntegerField()
    gallery_id = models.BigIntegerField(null=True, blank=True)
    poll_id = models.BigIntegerField(null=True, blank=True)
    avg_rating = models.FloatField()
    rating_cnt = models.BigIntegerField()
    updated_date = models.DateTimeField()
    class Meta:
        db_table = 'wp_bwbps_ratingssummary'

class WpCommentmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    comment_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255L, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = 'wp_commentmeta'

class WpComments(models.Model):
    comment_id = models.BigIntegerField(primary_key=True, db_column='comment_ID') # Field name made lowercase.
    comment_post_id = models.BigIntegerField(db_column='comment_post_ID') # Field name made lowercase.
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=100L)
    comment_author_url = models.CharField(max_length=200L)
    comment_author_ip = models.CharField(max_length=100L, db_column='comment_author_IP') # Field name made lowercase.
    comment_date = models.DateTimeField()
    comment_date_gmt = models.DateTimeField()
    comment_content = models.TextField()
    comment_karma = models.IntegerField()
    comment_approved = models.CharField(max_length=20L)
    comment_agent = models.CharField(max_length=255L)
    comment_type = models.CharField(max_length=20L)
    comment_parent = models.BigIntegerField()
    user_id = models.BigIntegerField()
    class Meta:
        db_table = 'wp_comments'

class WpGigpressArtists(models.Model):
    artist_id = models.IntegerField(primary_key=True)
    artist_name = models.CharField(max_length=255L)
    artist_order = models.IntegerField(null=True, blank=True)
    artist_alpha = models.CharField(max_length=255L)
    artist_url = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'wp_gigpress_artists'

class WpGigpressShows(models.Model):
    show_id = models.IntegerField(primary_key=True)
    show_artist_id = models.IntegerField()
    show_venue_id = models.IntegerField()
    show_tour_id = models.IntegerField(null=True, blank=True)
    show_date = models.DateField()
    show_multi = models.IntegerField(null=True, blank=True)
    show_time = models.TextField() # This field type is a guess.
    show_expire = models.DateField()
    show_price = models.CharField(max_length=255L, blank=True)
    show_tix_url = models.CharField(max_length=255L, blank=True)
    show_tix_phone = models.CharField(max_length=255L, blank=True)
    show_ages = models.CharField(max_length=255L, blank=True)
    show_notes = models.TextField(blank=True)
    show_related = models.BigIntegerField(null=True, blank=True)
    show_status = models.CharField(max_length=32L, blank=True)
    show_tour_restore = models.IntegerField(null=True, blank=True)
    show_address = models.CharField(max_length=255L, blank=True)
    show_locale = models.CharField(max_length=255L, blank=True)
    show_country = models.CharField(max_length=2L, blank=True)
    show_venue = models.CharField(max_length=255L, blank=True)
    show_venue_url = models.CharField(max_length=255L, blank=True)
    show_venue_phone = models.CharField(max_length=255L, blank=True)
    show_external_url = models.CharField(max_length=255L, blank=True)
    class Meta:
        db_table = 'wp_gigpress_shows'

class WpGigpressTours(models.Model):
    tour_id = models.IntegerField(primary_key=True)
    tour_name = models.CharField(max_length=255L)
    tour_status = models.CharField(max_length=32L, blank=True)
    class Meta:
        db_table = 'wp_gigpress_tours'

class WpGigpressVenues(models.Model):
    venue_id = models.IntegerField(primary_key=True)
    venue_name = models.CharField(max_length=255L)
    venue_address = models.CharField(max_length=255L, blank=True)
    venue_city = models.CharField(max_length=255L)
    venue_country = models.CharField(max_length=2L)
    venue_url = models.CharField(max_length=255L, blank=True)
    venue_phone = models.CharField(max_length=255L, blank=True)
    venue_state = models.CharField(max_length=255L, blank=True)
    venue_postal_code = models.CharField(max_length=32L, blank=True)
    class Meta:
        db_table = 'wp_gigpress_venues'

class WpLinks(models.Model):
    link_id = models.BigIntegerField(primary_key=True)
    link_url = models.CharField(max_length=255L)
    link_name = models.CharField(max_length=255L)
    link_image = models.CharField(max_length=255L)
    link_target = models.CharField(max_length=25L)
    link_description = models.CharField(max_length=255L)
    link_visible = models.CharField(max_length=20L)
    link_owner = models.BigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=255L)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=255L)
    class Meta:
        db_table = 'wp_links'

class WpNggAlbum(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255L)
    slug = models.CharField(max_length=255L)
    previewpic = models.BigIntegerField()
    albumdesc = models.TextField(blank=True)
    sortorder = models.TextField()
    pageid = models.BigIntegerField()
    class Meta:
        db_table = 'wp_ngg_album'

class WpNggGallery(models.Model):
    gid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255L)
    slug = models.CharField(max_length=255L)
    path = models.TextField(blank=True)
    title = models.TextField(blank=True)
    galdesc = models.TextField(blank=True)
    pageid = models.BigIntegerField()
    previewpic = models.BigIntegerField()
    author = models.BigIntegerField()
    class Meta:
        db_table = 'wp_ngg_gallery'

class WpNggPictures(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    image_slug = models.CharField(max_length=255L)
    post_id = models.BigIntegerField()
    galleryid = models.BigIntegerField()
    filename = models.CharField(max_length=255L)
    description = models.TextField(blank=True)
    alttext = models.TextField(blank=True)
    imagedate = models.DateTimeField()
    exclude = models.IntegerField(null=True, blank=True)
    sortorder = models.BigIntegerField()
    meta_data = models.TextField(blank=True)
    class Meta:
        db_table = 'wp_ngg_pictures'

class WpOptions(models.Model):
    option_id = models.BigIntegerField(primary_key=True)
    option_name = models.CharField(max_length=64L, unique=True)
    option_value = models.TextField()
    autoload = models.CharField(max_length=20L)
    class Meta:
        db_table = 'wp_options'

class WpPostmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    post_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255L, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = 'wp_postmeta'

class WpPosts(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    post_author = models.BigIntegerField()
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(max_length=20L)
    comment_status = models.CharField(max_length=20L)
    ping_status = models.CharField(max_length=20L)
    post_password = models.CharField(max_length=20L)
    post_name = models.CharField(max_length=200L)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=255L)
    menu_order = models.IntegerField()
    post_type = models.CharField(max_length=20L)
    post_mime_type = models.CharField(max_length=100L)
    comment_count = models.BigIntegerField()
    class Meta:
        db_table = 'wp_posts'

class WpRandomtext(models.Model):
    randomtext_id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=32L)
    text = models.TextField()
    visible = models.CharField(max_length=3L)
    user_id = models.IntegerField()
    timestamp = models.DateTimeField()
    class Meta:
        db_table = 'wp_randomtext'

class WpTermRelationships(models.Model):
    object_id = models.BigIntegerField()
    term_taxonomy_id = models.BigIntegerField()
    term_order = models.IntegerField()
    class Meta:
        db_table = 'wp_term_relationships'

class WpTermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key=True)
    term_id = models.BigIntegerField()
    taxonomy = models.CharField(max_length=32L)
    description = models.TextField()
    parent = models.BigIntegerField()
    count = models.BigIntegerField()
    class Meta:
        db_table = 'wp_term_taxonomy'

class WpTerms(models.Model):
    term_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200L)
    slug = models.CharField(max_length=200L, unique=True)
    term_group = models.BigIntegerField()
    class Meta:
        db_table = 'wp_terms'

class WpUsermeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255L, blank=True)
    meta_value = models.TextField(blank=True)
    class Meta:
        db_table = 'wp_usermeta'

class WpUsers(models.Model):
    id = models.BigIntegerField(primary_key=True, db_column='ID') # Field name made lowercase.
    user_login = models.CharField(max_length=60L)
    user_pass = models.CharField(max_length=64L)
    user_nicename = models.CharField(max_length=50L)
    user_email = models.CharField(max_length=100L)
    user_url = models.CharField(max_length=100L)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=60L)
    user_status = models.IntegerField()
    display_name = models.CharField(max_length=250L)
    class Meta:
        db_table = 'wp_users'

class WpWpb2DExcludedFiles(models.Model):
    file = models.CharField(max_length=255L, unique=True)
    isdir = models.IntegerField()
    class Meta:
        db_table = 'wp_wpb2d_excluded_files'

class WpWpb2DOptions(models.Model):
    name = models.CharField(max_length=50L, unique=True)
    value = models.CharField(max_length=255L)
    class Meta:
        db_table = 'wp_wpb2d_options'

class WpWpb2DPremiumExtensions(models.Model):
    name = models.CharField(max_length=50L, unique=True)
    file = models.CharField(max_length=255L)
    class Meta:
        db_table = 'wp_wpb2d_premium_extensions'

class WpWpb2DProcessedFiles(models.Model):
    file = models.CharField(max_length=255L, unique=True)
    offset = models.IntegerField()
    uploadid = models.CharField(max_length=50L, blank=True)
    class Meta:
        db_table = 'wp_wpb2d_processed_files'

