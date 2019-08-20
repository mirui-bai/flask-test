# import unittest
# import re
# from flask import url_for
# from app import create_app, db
# from app.models import User, Role
#
#
# class FlaskClientTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('testing')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()
#         Role.insert_roles()
#         self.client = self.app.test_client(use_cookies=True)
#
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
#
#     def test_home_page(self):
#         response = self.client.get(url_for('main.index'))
#         self.assertTrue('Stranger' in response.get_data(as_text=True))
#
#     def test_register_and_login(self):
#         # register a new account
#         response = self.client.post(url_for('auth.register'), data={
#             'email': 'john@example.com',
#             'username': 'john',
#             'password': 'cat',
#             'password2': 'cat'
#         }, follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(re.search('You\s+can\s+now\s+login\s+!', response.get_data(as_text=True)))
#
#         # login with the new account
#         response = self.client.post('/auth/login', data={
#             'email': 'john@example.com',
#             'password': 'cat'
#         }, follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue(re.search('You\s+Account\s+Unconfirmed', response.get_data(as_text=True)))
#
#         # send a confirmation token
#         user = User.query.filter_by(email='john@example.com').first()
#         token = user.generate_confirmation_token()
#         user.confirm(token)
#         response = self.client.get('/auth/confirm/{}'.format(token),
#                                    follow_redirects=True)
#         print(response.get_data(as_text=True))
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('Happy to see you again!' in response.get_data(as_text=True))
#
#         # log out
#         response = self.client.get('/auth/logout', follow_redirects=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertTrue('You have been logged out.' in response.get_data(
#             as_text=True))
