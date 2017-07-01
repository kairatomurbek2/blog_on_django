import uuid


def blog_image_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/blogs/images/unicode<filename>
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return 'blogs/images/{0}'.format(filename)
