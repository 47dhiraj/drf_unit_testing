from rest_framework.test import APIClient                      
from organization.tests import base_test
from organization.models import Organization


class OrganizationTestCreateCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()                                    
        self.client = APIClient() 
        self.login_response = self.client.post('/api/v1/user/login/',   
                                               {'username': self.username,             
                                                'password': self.password},
                                               format='json')
        self.access_token = self.login_response.json()['access']                        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)      

    def test_organization_create_api(self):                                             
        self.create_organization = self.client.post('/api/v1/organization/',
                                                    {
                                                        'name': 'Agent Company',
                                                        'established_on': '1996-01-01',
                                                        'registration_code': '471234'
                                                    }, format='json')
        self.assertEquals(self.create_organization.status_code, 201)
        self.assertTrue('Agent Company' in self.create_organization.json()['data']['name'])
        self.assertTrue('1996-01-01' in self.create_organization.json()['data']['established_on'])
        self.assertTrue('471234' in self.create_organization.json()['data']['registration_code'])

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()    
        super().tearDown()



class OrganizationTestListingCase(base_test.NewUserTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username,
                                                'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Agent Company',
                                                        established_on='1996-01-01',
                                                        registration_code='471234')

    def test_organization_listing_api(self):
        self.list_organizations = self.client.get('/api/v1/organization/', format='json')       
        self.assertEquals(self.list_organizations.status_code, 200)                             
        self.assertTrue('Agent Company' in self.list_organizations.json()['results'][0]['name'])   

    def tearDown(self) -> None:
        self.client.logout()
        Organization.objects.filter().delete()        
        super().tearDown()




class OrganizationTestAccessByIdCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')
        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Agent Company',
                                                        established_on='1996-01-01',
                                                        registration_code='471234')


    def test_organization_access_by_id_api(self):
        self.read_organization_by_id = self.client.get(f'/api/v1/organization/{self.organization.id}', format='json')
        self.assertEquals(self.read_organization_by_id.status_code, 200)         
        self.assertTrue('Agent Company' in self.read_organization_by_id.json()['name'])
        self.assertTrue('1996-01-01' in self.read_organization_by_id.json()['established_on'])
        self.assertTrue('471234' in self.read_organization_by_id.json()['registration_code'])


    def tearDown(self):
        self.client.logout()
        self.organization.delete()
        super().tearDown()



class OrganizationTestUpdateByIdCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')
        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Agent Company',
                                                        established_on='1996-01-01',
                                                        registration_code='471234')


    def test_organization_update_by_id_api(self):
        self.update_organization_by_id = self.client.put(f'/api/v1/organization/{self.organization.id}',
                                                         {
                                                             'name': '47 Company',
                                                             'established_on': '1994-01-01',
                                                             'registration_code': '12345846'
                                                         }, format='json')
        self.assertEquals(self.update_organization_by_id.status_code, 200)
        self.assertTrue(self.update_organization_by_id.json()['status'], True)
        self.assertEquals(self.update_organization_by_id.json()['message'], 'Organization Updated !')
        self.assertEquals(self.update_organization_by_id.json()['data']['name'], '47 Company')
        self.assertEquals(self.update_organization_by_id.json()['data']['established_on'], '1994-01-01')
        self.assertEquals(self.update_organization_by_id.json()['data']['registration_code'], '12345846')


    def tearDown(self):
        self.client.logout()
        self.organization.delete()
        super().tearDown()





class OrganizationTestDeleteByIdCase(base_test.NewUserTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_response = self.client.post('/api/v1/user/login/',
                                               {'username': self.username, 'password': self.password},
                                               format='json')

        self.access_token = self.login_response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.organization = Organization.objects.create(name='Agent Company',
                                                        established_on='1996-01-01',
                                                        registration_code='471234')


    def test_organization_delete_by_id_api(self):
        self.delete_organization_by_id = self.client.delete(f'/api/v1/organization/{self.organization.id}',
                                                            format='json')
        self.assertEquals(self.delete_organization_by_id.status_code, 204)


    def tearDown(self):
        self.client.logout()
        super().tearDown()


