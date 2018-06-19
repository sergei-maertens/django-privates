from django.urls import reverse

import pytest


@pytest.mark.django_db
def test_admin_widget_url(admin_client, private_file):
    url = reverse('admin:testapp_file_change', args=(private_file.pk,))
    file_url = reverse('admin:testapp_file_file', args=(private_file.pk,))

    response = admin_client.get(url)
    assert file_url in response.rendered_content


@pytest.mark.django_db
def test_admin_view(admin_client, private_file):
    url = reverse('admin:testapp_file_file', args=(private_file.pk,))

    response = admin_client.get(url)

    assert 'X-Accel-Redirect' in response
    assert 'Content-Type' in response

    assert response['Content-Disposition'] == 'attachment; filename="dummy.txt"'
