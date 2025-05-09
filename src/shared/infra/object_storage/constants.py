ALLOWED_IMAGE_MIME_TYPES = [ 'image/png', 'image/jpg', 'image/jpeg', 'image/webp', 'image/gif' ]
ALLOWED_VIDEO_MIME_TYPES = [ 'video/mp4', 'video/webm', 'video/ogg' ]

ALLOWED_IMAGE_TYPES = [ x.replace('image/', '') for x in ALLOWED_IMAGE_MIME_TYPES ]
ALLOWED_VIDEO_TYPES = [ x.replace('image/', '') for x in ALLOWED_VIDEO_MIME_TYPES ]