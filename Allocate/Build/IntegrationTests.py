import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from Build.app import app
from datetime import date, time

class FlaskLoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_valid_login(self):
        response = self.client.post('/logIn', data={
            'email': 'joo20210042@std.psut.edu.jo',
            'password': 'bsbsbs'
        }, follow_redirects=True) 

        self.assertEqual(response.status_code, 200)
        self.assertIn('Home', response.data.decode('utf-8'))
    
    def test_invalid_login(self):
        response = self.client.post('/logIn', data={
            'email': 'joo20210042@std.psut.edu',
            'password': 'bsbsbs'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Invalid username', response.data.decode('utf-8'))

    def test_valid_reservation(self):
        response = self.client.post('/ReserveForm/1', data={
            'eventTitle': 'Test event',
            'eventType': 'Conference',
            'date': date(2025, 5, 28),
            'start_time': "12:00",
            'end_time': "14:00",
            'facility': 'IT203',
            'fundingSource': 'None',
            'fundingAmount': 0,
            'agenda': 'None',
            'guestCount': 0
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Reservation Requests', response.data.decode('utf-8'))
        self.assertIn('Test event', response.data.decode('utf-8'))

    def test_invalid_reservation(self):
        response = self.client.post('/ReserveForm/1', data={
            'eventTitle': 'Test event',
            'eventType': 'Conference',
            'date': date(2025, 5, 28),
            'start_time': "12:00",
            'end_time': "14:00",
            'facility': 'No facilities available for this time.',
            'fundingSource': 'None',
            'fundingAmount': 0,
            'agenda': 'None',
            'guestCount': 0
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Reservation Form', response.data.decode('utf-8'))

    def test_valid_report(self):
        response = self.client.post('/ReportIssue/1', data={
            'description': 'Monitor does not work',
            'equipment': 'Monitor'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Reservations', response.data.decode('utf-8'))

    def test_view_all_requests(self):
        response = self.client.get('/ViewAllRequests', data={}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Test event', response.data.decode('utf-8'))

    def test_view_all_reports(self):
        response = self.client.get('/ViewAllReports', data={}, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Monitor does not work', response.data.decode('utf-8'))

    def test_add_user(self):
        response = self.client.get('/AddUser', data={
            "uniId": 12345,
            "name": "Sara Ahmad",
            "userType": "0",
            "email": "sara@test.com"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

    def test_generate_schedule(self):
        response = self.client.get('/GenerateSchedule', data={
            "startDate": date(2026, 5, 28),
            "endDate": date(2026, 6, 12)
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)