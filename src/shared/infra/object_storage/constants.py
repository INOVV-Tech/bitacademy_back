ALLOWED_IMAGE_MIME_TYPES = [ 'image/png', 'image/jpg', 'image/jpeg', 'image/webp', 'image/gif' ]
ALLOWED_VIDEO_MIME_TYPES = [ 'video/mp4', 'video/webm', 'video/ogg' ]

ALLOWED_DOCUMENT_MIME_TYPES = [
    'text/plain',
    'text/csv',
    'text/tab-separated-values',
    'text/html',
    'application/xml',
    'application/json',
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/rtf',
    'application/zip',
    'application/vnd.rar',
    'application/x-7z-compressed',
    'application/x-tar',
    'application/gzip'
]

ALLOWED_IMAGE_TYPES = [ x.replace('image/', '') for x in ALLOWED_IMAGE_MIME_TYPES ]
ALLOWED_VIDEO_TYPES = [ x.replace('image/', '') for x in ALLOWED_VIDEO_MIME_TYPES ]