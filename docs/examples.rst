Web-server configuration examples
=================================

nGINX
-----

Django settings:

.. code-block:: python

    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
        "privates": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": "/path/to/files/on/disk/private_media/",
                "base_url": "/private-media/",
            },
        },
    }

    SENDFILE_BACKEND = "django_sendfile.backends.nginx"
    SENDFILE_ROOT = "/path/to/files/on/disk/private_media/"
    SENDFILE_URL = "/private-media/"

Nginx configuration:

.. code-block:: nginx

    server {
        listen app.example.com 443 http2 ssl;

        location / {
          # usual proxy directives
        }

        location /private-media/ {
            internal;  # crucial to prevent direct access!
            alias /path/to/files/on/disk/private_media/;
        }
    }
