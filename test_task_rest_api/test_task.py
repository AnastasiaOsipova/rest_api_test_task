import pytest
from rest_api_methods import InfoLogisticRequests


class TestTask:

    def setup(self):
        self.channels_ids = []
        self.go_teardown = True
        self.api = InfoLogisticRequests()
        auth_result = self.api.auth('adm1noff.t@yandex.ru', 'SinglePassword7')
        assert auth_result.status_code == 200, 'auth error'
        assert auth_result.json()
        self.result_tests = []

    def test_end_to_end(self):

        # create new channel
        new_channel = self.api.create_channel()
        assert new_channel.status_code == 201
        new_channel_id = new_channel.json()
        self.channels_ids.append(new_channel_id)

        # get channel content
        response = self.api.get_channel_content(new_channel_id)
        assert response.status_code == 200
        channel_content = response.json()

        # check we take right channel content
        assert new_channel_id == channel_content['oguid']

        # edit channel
        changed_channel = self.api.edit_channel(new_channel_id)
        assert changed_channel.status_code == 201
        changed_channel_content = changed_channel.json()

        # get edited channel
        edited_channel = self.api.get_channel_content(new_channel_id)
        assert edited_channel.status_code == 200
        edited_channel_content = edited_channel.json()

        # check changed_channel_content == edited_channel_content
        assert changed_channel_content == edited_channel_content

        # # get all channels
        # channels = self.api.get_channels()
        # assert channels.status_code == 200


    def test_required(self):

        # create channel withno dispensable fields
        for field in ['subOrgOguid', 'constraintViolationOguid', 'initiatorOguid', 'direction']:
            channel = self.api.create_channel(pop=field)
            assert channel.status_code == 201
            self.channels_ids.append(channel.json())

        # create channel withno name or status
        for field in ['name', 'status']:
            channel = self.api.create_channel(pop=field)
            assert channel.status_code == 400

        # create channel withno filename
        channel = self.api.create_channel(pop='filename')
        assert channel.status_code == 403

        # create channel withno documentType
        channel = self.api.create_channel(pop='documentType')
        assert channel.status_code == 500

    def test_nullable(self):

        for i in [None, '']:
            # create channel with nullable subOrgOguid
            channel = self.api.create_channel(subOrgOguid=i)
            assert channel.status_code == 201
            self.channels_ids.append(channel.json())

            # create channel with nullable constraintViolationOguid
            channel = self.api.create_channel(constraintViolationOguid=i)
            assert channel.status_code == 201
            self.channels_ids.append(channel.json())

            # create channel with nullable initiatorOguid
            channel = self.api.create_channel(initiatorOguid=i)
            assert channel.status_code == 201
            self.channels_ids.append(channel.json())

            # create channel with nullable name
            channel = self.api.create_channel(name=i)
            assert channel.status_code == 400

            # create channel with nullable status
            channel = self.api.create_channel(status=i)
            assert channel.status_code == 400

        # create channel with direction = None
        channel = self.api.create_channel(direction=None)
        assert channel.status_code == 201
        self.channels_ids.append(channel.json())

        # create channel with direction = ''
        channel = self.api.create_channel(direction='')
        assert channel.status_code == 400

        # create channel with filename = None
        channel = self.api.create_channel(filename=None)
        assert channel.status_code == 403

        # create channel with filename = ''
        channel = self.api.create_channel(filename='')
        assert channel.status_code == 400

        # create channel with documentType=None
        channel = self.api.create_channel(documentType=None)
        assert channel.status_code == 500

        # create channel with documentType=''
        channel = self.api.create_channel(documentType='')
        assert channel.status_code == 400

    def test_get_deleted_channel_content(self):
        deleted_channel_id = ['8a13ebb6-5428-45b5-89ad-1ae041556127',
                              '6550b35c-2b98-4cc8-93b8-18f545c021f0',
                              '3a7add5f-157e-4d35-b5ce-04d74fd937f1']
        for channel_id in deleted_channel_id:
            channel = self.api.get_channel_content(channel_id)
            assert channel.status_code == 404
            assert channel.json()['error'] == 'Not Found'

    def test_pattern(self):
        for i in [-6.63, 5, True, False]:
            # create channel with nullable name
            channel = self.api.create_channel(name=i)
            self.result_tests.append(channel.status_code)

            # create channel with filename = None
            channel = self.api.create_channel(filename=i)
            self.result_tests.append(channel.status_code)

            # create channel with nullable status
            channel = self.api.create_channel(status=i)
            self.result_tests.append(channel.status_code)

            # create channel with documentType=''
            channel = self.api.create_channel(documentType=i)
            self.result_tests.append(channel.status_code)

            # create channel with nullable subOrgOguid
            channel = self.api.create_channel(subOrgOguid=i)
            self.result_tests.append(channel.status_code)

            # create channel with nullable constraintViolationOguid
            channel = self.api.create_channel(constraintViolationOguid=i)
            self.result_tests.append(channel.status_code)

            # create channel with nullable initiatorOguid
            channel = self.api.create_channel(initiatorOguid=i)
            self.result_tests.append(channel.status_code)

            # create channel with direction = ''
            channel = self.api.create_channel(direction=i)
            self.result_tests.append(channel.status_code)

            print(self.result_tests)
            self.result_tests.clear()

    def teardown(self):
        if self.go_teardown:
            # delete all channels
            for channel_id in self.channels_ids:
                delete_channel = self.api.delete_channel(channel_id)
                assert delete_channel.status_code == 204
