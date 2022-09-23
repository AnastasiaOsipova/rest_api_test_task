import requests
import json


class InfoLogisticRequests:

    def __init__(self):
        self.site_url = 'https://im-api-df-backend-dev.dev.info-logistics.eu'
        self.orgid = 'a08fa69a-efe8-4679-a63a-5637f22860db'
        self.headers = {"Access-Token": None,
                        "Accept": "application/json",
                        "Content-Type": "application/json"}

    def auth(self, username, password):
        """
        Authtorisation
        :param username: Email
        :param password: password
        :return: None
        """
        data = {
            "email": username,
            "password": password
        }
        response = requests.post(f"{self.site_url}/signin", json=data)
        self.headers['Access-Token'] = response.json()['access']['value']
        return response

    def get_channels(self):
        """
        get channels content
        :return: list of channels with content
        """
        response = requests.get(f"{self.site_url}/orgs/{self.orgid}/channels", headers=self.headers)
        return response

    def create_channel(self, **kwargs):
        """

        :return: current channel id
        """
        request_body = json.load(open('create_channel.json', "r"))
        for kwarg, value in kwargs.items():
            if kwarg in ['filename', 'direction']:
                request_body['fields'][kwarg] = value
            elif kwarg == 'pop':
                if value in ['filename', 'direction']:
                    request_body['fields'].pop(value)
                else:
                    request_body.pop(value)
            else:
                request_body[kwarg] = value
        response = requests.post(f"{self.site_url}/orgs/{self.orgid}/channels", json=request_body, headers=self.headers)
        return response

    def get_channel_content(self, channel_id):
        """

        :param channel_id: channel id
        :return:current channel content
        """
        response = requests.get(f"{self.site_url}/orgs/{self.orgid}/channels/{channel_id}", headers=self.headers)
        return response

    def edit_channel(self, channel_id, **kwargs):
        """

        :param channel_id: channel id
        :return: edited channel content
        """
        request_body = json.load(open('edit_channel.json', "r"))
        for kwarg, value in kwargs.items():
            if kwarg in ['filename', 'direction']:
                request_body['fields'][kwarg] = value
            elif kwarg == 'pop':
                if value in ['filename', 'direction']:
                    request_body['fields'].pop(value)
                else:
                    request_body.pop(value)
            else:
                request_body[kwarg] = value
        response = requests.put(f"{self.site_url}/orgs/{self.orgid}/channels/{channel_id}", json=request_body,
                                headers=self.headers)
        return response

    def delete_channel(self, channel_id):
        """

        :param channel_id: channel id
        :return: None
        """
        response = requests.delete(f"{self.site_url}/orgs/{self.orgid}/channels/{channel_id}", headers=self.headers)
        return response

