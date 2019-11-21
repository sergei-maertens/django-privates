from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_admin_widget_url(admin_client, private_file):
    url = reverse('admin:testapp_file_change', args=(private_file.pk,))
    file_url = reverse('admin:testapp_file_file', args=(private_file.pk,))
    image_url = reverse('admin:testapp_file_image', args=(private_file.pk,))

    response = admin_client.get(url)
    assert file_url in response.rendered_content
    assert image_url in response.rendered_content


@pytest.mark.django_db
def test_admin_view(admin_client, private_file):
    file_url = reverse('admin:testapp_file_file', args=(private_file.pk,))
    image_url = reverse('admin:testapp_file_image', args=(private_file.pk,))

    file_response = admin_client.get(file_url)
    image_response = admin_client.get(image_url)

    assert 'X-Accel-Redirect' in file_response
    assert 'Content-Type' in file_response
    assert 'X-Accel-Redirect' in image_response
    assert 'Content-Type' in image_response

    assert file_response['Content-Disposition'] == 'attachment; filename="dummy.txt"'
    assert image_response['Content-Disposition'] == 'attachment; filename="dummy.png"'
