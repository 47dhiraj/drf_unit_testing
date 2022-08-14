from rest_framework.test import APIClient       
from organization.tests import base_test


class RefreshTokenTestCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_user_refresh_token(self):
        client = APIClient()
        login_response = client.post('/api/v1/user/login/', 
                                    {'username': self.username, 'password': self.password},
                                    format='json')

        token_refresh_response = client.post('/api/v1/user/refresh-token/',
                                            {'refresh': login_response.json()['refresh']},
                                            format='json')

        self.assertEquals(token_refresh_response.status_code, 200)
        self.assertTrue('access' in token_refresh_response.json())

    def tearDown(self) -> None:
        self.client.logout()                                    
        super().tearDown()
