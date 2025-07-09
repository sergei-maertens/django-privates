from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _

import pytest
from PIL import Image
from pyquery import PyQuery as pq


@pytest.mark.django_db
def test_admin_widget_url(admin_client, private_file):
    url = reverse("admin:testapp_file_change", args=(private_file.pk,))
    file_url = reverse("admin:testapp_file_file", args=(private_file.pk,))
    image_url = reverse("admin:testapp_file_image", args=(private_file.pk,))

    response = admin_client.get(url)
    assert file_url in response.rendered_content
    assert image_url in response.rendered_content


@pytest.mark.django_db
def test_admin_view(admin_client, private_file):
    file_url = reverse("admin:testapp_file_file", args=(private_file.pk,))
    image_url = reverse("admin:testapp_file_image", args=(private_file.pk,))

    file_response = admin_client.get(file_url)
    image_response = admin_client.get(image_url)

    assert "X-Accel-Redirect" in file_response
    assert "Content-Type" in file_response
    assert "X-Accel-Redirect" in image_response
    assert "Content-Type" in image_response

    assert file_response["Content-Disposition"] == 'attachment; filename="dummy.txt"'
    assert image_response["Content-Disposition"] == 'attachment; filename="dummy.png"'


def test_admin_widget_url_empty_initial(admin_client):
    url = reverse("admin:testapp_file_add")
    response = admin_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_widget_url_inmemoryfile(admin_client):
    url = reverse("admin:testapp_file_add")
    response = admin_client.post(url, {"file": BytesIO(b"")}, follow=True)
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_no_download_field(admin_client, private_file):
    """Assert that there is no view for `private_media_no_download_fields`
    but the relevant filename is still visible in the response"""

    url = reverse("admin:testapp_file2_change", args=(private_file.pk,))

    response = admin_client.get(url)

    # OK: file field is not included in `private_media_no_download_fields`
    file_url = reverse("admin:testapp_file2_file", args=(private_file.pk,))
    assert file_url in response.rendered_content

    # Fail: image field is included in `private_media_no_download_fields`
    with pytest.raises(NoReverseMatch):
        reverse("admin:testapp_file2_image", args=(private_file.pk,))

    # display_value of img element is still visible
    html = response.content.decode("utf-8")
    doc = pq(html)
    uploads = doc(".file-upload")
    img = uploads[1]

    display_value = img.text.strip()

    assert display_value == _("Currently: %s") % private_file.image.name


@pytest.mark.django_db
def test_admin_readonly_field(admin_client, private_file):
    """
    Assert that readonly files have the correct download URL.
    """
    url = reverse("admin:testapp_file4_change", args=(private_file.pk,))
    change_page = admin_client.get(url)
    assert change_page.status_code == 200
    html = change_page.content.decode("utf-8")
    doc = pq(html)
    download_link = doc.find(".readonly a").eq(0)
    assert download_link.attr("href") == reverse(
        "admin:testapp_file4_file", args=(private_file.pk,)
    )


@pytest.mark.django_db
def test_admin_readonly_field_can_still_cache_object(
    admin_client, private_file, settings
):
    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    }
    # Regression test for #15 - the readonly field workaround introduced a regression
    # leading to the model instance no longer being able to be pickled.
    url = reverse("admin:testapp_file4_change", args=(private_file.pk,))
    png_image = Image.new("RGB", (1, 1), color=(255, 255, 255))
    png_file = BytesIO()
    png_image.save(png_file, format="PNG")
    png_file.seek(0)

    # submit the form to modify the object, which triggers the cache hook, which
    # triggers the pickling error
    response = admin_client.post(
        url,
        {
            "file": BytesIO(b""),
            "image": SimpleUploadedFile("pixel.png", png_file.read()),
        },
    )

    assert response.status_code == 302
