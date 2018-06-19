from io import BytesIO

from django.core.files import File

import pytest


@pytest.fixture
def private_file(request):
    from testapp.models import File as FileModel
    file = FileModel()
    file.file.save('dummy.txt', File(BytesIO(b'dummy')))

    def fin():
        file.file.storage.delete('dummy.txt')

    request.addfinalizer(fin)
    return file
