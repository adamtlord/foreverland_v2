from common.uploads import staff_receipt_url
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail


def thumbnail(image_path):
    t = get_thumbnail(image_path, "60x60", quality=60)
    return u'<img src="%s" alt="%s" />' % (t.url, image_path)


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value:
            file_name = str(value)
            href = staff_receipt_url(value)
            file_type = value.name[-3:]
            if file_type != "pdf":
                try:
                    output.append(
                        '<a href="%s" class="thumb">%s</a>'
                        % (href, thumbnail(file_name))
                    )
                except Exception:
                    pass
            else:
                try:
                    display = file_name.split("/")[-1]
                    output.append(
                        '<a href="%s" class="file"><i class="fa fa-file-pdf-o"></i> %s</a>'
                        % (href, display)
                    )
                except Exception:
                    pass
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u"".join(output))
