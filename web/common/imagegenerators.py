from imagekit import processors, ImageSpec, register


class Thumbnail(ImageSpec):
    processors = [
        processors.SmartResize(100, 100),
        processors.Adjust(contrast=1.1, sharpness=1.1),
    ]

class Medium(ImageSpec):
    processors = [processors.ResizeToFit(400, 400)]


class Large(ImageSpec):
    processors = [processors.ResizeToFit(960, 960)]


register.generator('common:thumbnail', Thumbnail)
register.generator('common:medium', Medium)
register.generator('common:large', Large)
