Web-server configuration examples
=================================

nGINX
-----

Django settings:

.. code-block:: python

    PRIVATE_MEDIA_ROOT = "/path/to/files/on/disk/private_media/"
    PRIVATE_MEDIA_URL = "/private-media/"
    SENDFILE_BACKEND = "django_sendfile.backends.nginx"
    SENDFILE_ROOT = PRIVATE_MEDIA_ROOT
    SENDFILE_URL = PRIVATE_MEDIA_URL

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
