
import unittest
from unittest.mock import patch, MagicMock
from app import app  # Assuming your Flask app is in app.py

class LogInTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch("app.session")
    def test_not_found_email(self, mock_session):
        mock_session.query().all.return_value = [("test@example.com",)]
        response = self.client.post("/logIn", data={"email": "notfound@example.com", "password": "Pass1234"})
        self.assertIn(b"Invalid username", response.data)

    @patch("app.session")
    def test_incorrect_password(self, mock_session):
        mock_session.query().all.return_value = [("test@example.com",)]
        mock_session.query().filter_by().first.side_effect = [
            ("correct_password",)
        ]
        response = self.client.post("/logIn", data={"email": "test@example.com", "password": "wrong_password"})
        self.assertIn(b"Incorrect password", response.data)

    @patch("app.session")
    def test_student_login_success(self, mock_session):
        mock_session.query().all.return_value = [("student@example.com",)]
        mock_session.query().filter_by().first.side_effect = [
            ("student_pass",),        # Password
            ("Student Name",),        # userName
            (1,),                     # userId
            ("Student",)              # role
        ]
        response = self.client.post("/logIn", data={"email": "student@example.com", "password": "student_pass"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/Homepage/1", response.location)

    @patch("app.session")
    def test_instructor_login_success(self, mock_session):
        mock_session.query().all.return_value = [("inst@example.com",)]
        mock_session.query().filter_by().first.side_effect = [
            ("inst_pass",),          # Password
            ("Instructor",),         # userName
            (2,),                    # userId
            ("Instructor",)          # role
        ]
        response = self.client.post("/logIn", data={"email": "inst@example.com", "password": "inst_pass"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/Homepage/2", response.location)

    @patch("app.session")
    def test_student_affairs_login_success(self, mock_session):
        mock_session.query().all.return_value = [("sa@example.com",)]
        mock_session.query().filter_by().first.side_effect = [
            ("sapass",), ("SA",), (3,), ("Student Affairs",)
        ]
        response = self.client.post("/logIn", data={"email": "sa@example.com", "password": "sapass"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/ViewPendingRequests", response.location)

    @patch("app.session")
    def test_technician_login_success(self, mock_session):
        mock_session.query().all.return_value = [("tech@example.com",)]
        mock_session.query().filter_by().first.side_effect = [
            ("techpass",), ("Tech",), (4,), ("Technician",)
        ]
        response = self.client.post("/logIn", data={"email": "tech@example.com", "password": "techpass"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/ViewPendingReports", response.location)

    @patch("app.session")
    def test_registration_login_success(self, mock_session):
        mock_session.query().all.return_value = [("reg@example.com",)]
        mock_session.query().filter_by().first.side_effect = [
            ("regpass",), ("Reg",), (5,), ("Registration",)
        ]
        response = self.client.post("/logIn", data={"email": "reg@example.com", "password": "regpass"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("/GenerateSchedule", response.location)

class ViewReservationsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch("app.session")
    def test_view_reservations_with_valid_data(self, mock_session):
        mock_reservation_1 = MagicMock()
        mock_reservation_1.reservationId = 101
        mock_reservation_1.title = "Reservation 1"
        mock_reservation_1.date.isoformat.return_value = "2025-05-20"
        mock_reservation_1.start.strftime.return_value = "14:00"
        mock_reservation_1.facilityId = 201
        mock_reservation_1.status = 1
        mock_reservation_1.reportId = 301
        mock_reservation_1.reservedBy = 1

        mock_reservation_2 = MagicMock()
        mock_reservation_2.status = 0  

        mock_session.query().filter_by().order_by().all.return_value = [mock_reservation_1, mock_reservation_2]

        mock_facility = MagicMock()
        mock_facility.buildingId = 401
        mock_session.query().filter_by().first.side_effect = [
            mock_facility,                        # Facility for reservation 1
            ("Luai Shammout",),                      # Facility.facilityName query
            ("ENG",)                      # Buildings.buildingName query
        ]

        response = self.client.get("/ViewReservations/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Reservation 1", response.data)
        self.assertIn(b"Luai Shammout", response.data)
        self.assertIn(b"ENG", response.data)

    @patch("app.session")
    def test_view_reservations_with_no_active_reservations(self, mock_session):
        mock_reservation = MagicMock()
        mock_reservation.status = 0

        mock_session.query().filter_by().order_by().all.return_value = [mock_reservation]

        response = self.client.get("/ViewReservations/2")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"reservationId", response.data)
   
# class AcademicHomePageTestCase(unittest.TestCase):
#     def setUp(self):
#         self.client = app.test_client()
#         self.client.testing = True

#     @patch("app.session")
#     def test_homepage_with_pending_reservation(self, mock_session):
#         mock_session.query().filter_by().first.side_effect = [
#             ("Sara Ahmad",),
#             None           
#         ]

#         mock_last_request = MagicMock()
#         mock_last_request.status = 0 
#         mock_last_request.facilityName = "IT101"
#         mock_last_request.start.strftime.return_value = "10:00"

#         # Patch lastRequest query separately (we patch .first() on the Reservations query)
#         def filter_by_side_effect(**kwargs):
#             # When filter_by is called on Reservations, return a query whose .order_by().first() returns mock_last_request
#             mock_query = MagicMock()
#             mock_query.order_by.return_value.first.return_value = mock_last_request
#             return mock_query

#         # We patch session.query to differentiate calls:
#         # The first query for userName, the second for lastRequest
#         def query_side_effect(model):
#             if model.__name__ == "Users":
#                 # Returns a query where .filter_by().first() returns userName tuple
#                 mock_user_query = MagicMock()
#                 mock_user_query.filter_by.return_value.first.return_value = ("Sara Ahmad",)
#                 return mock_user_query
#             elif model.__name__ == "Reservations":
#                 mock_res_query = MagicMock()
#                 mock_res_query.filter_by.return_value.order_by.return_value.first.return_value = mock_last_request
#                 return mock_res_query
#             elif model.__name__ == "Facility":
#                 mock_facility_query = MagicMock()
#                 mock_facility_query.filter_by.return_value.first.return_value = ("Room",)
#                 return mock_facility_query
#             else:
#                 return MagicMock()

#         mock_session.query.side_effect = query_side_effect

#         response = self.client.get("/Homepage/1")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Sara Ahmad", response.data)
#         self.assertIn(b"Room", response.data)
#         self.assertIn(b"10:00", response.data)
#         self.assertIn(b"Pending", response.data)

#     @patch("app.session")
#     def test_homepage_with_approved_reservation(self, mock_session):
#         mock_last_request = MagicMock()
#         mock_last_request.status = 1  # Approved
#         mock_last_request.facilityId = 101
#         mock_last_request.start.strftime.return_value = "12:00"

#         def query_side_effect(model):
#             if model.__name__ == "Users":
#                 mock_user_query = MagicMock()
#                 mock_user_query.filter_by.return_value.first.return_value = ("Jane Smith",)
#                 return mock_user_query
#             elif model.__name__ == "Reservations":
#                 mock_res_query = MagicMock()
#                 mock_res_query.filter_by.return_value.order_by.return_value.first.return_value = mock_last_request
#                 return mock_res_query
#             elif model.__name__ == "Facility":
#                 mock_facility_query = MagicMock()
#                 mock_facility_query.filter_by.return_value.first.return_value = ("Library",)
#                 return mock_facility_query
#             else:
#                 return MagicMock()

#         mock_session.query.side_effect = query_side_effect

#         response = self.client.get("/Homepage/2")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Jane Smith", response.data)
#         self.assertIn(b"Library", response.data)
#         self.assertIn(b"12:00", response.data)
#         self.assertIn(b"Approved", response.data)

#     @patch("app.session")
#     def test_homepage_with_rejected_reservation(self, mock_session):
#         mock_last_request = MagicMock()
#         mock_last_request.status = 2  # Rejected
#         mock_last_request.facilityId = 101
#         mock_last_request.start.strftime.return_value = "15:00"

#         def query_side_effect(model):
#             if model.__name__ == "Users":
#                 mock_user_query = MagicMock()
#                 mock_user_query.filter_by.return_value.first.return_value = ("Alice",)
#                 return mock_user_query
#             elif model.__name__ == "Reservations":
#                 mock_res_query = MagicMock()
#                 mock_res_query.filter_by.return_value.order_by.return_value.first.return_value = mock_last_request
#                 return mock_res_query
#             elif model.__name__ == "Facility":
#                 mock_facility_query = MagicMock()
#                 mock_facility_query.filter_by.return_value.first.return_value = ("Auditorium",)
#                 return mock_facility_query
#             else:
#                 return MagicMock()

#         mock_session.query.side_effect = query_side_effect

#         response = self.client.get("/Homepage/3")
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b"Alice", response.data)
#         self.assertIn(b"Auditorium", response.data)
#         self.assertIn(b"15:00", response.data)
#         self.assertIn(b"Rejected", response.data)

#     @patch("app.session")
#     def test_homepage_with_no_reservation(self, mock_session):
#         # User with no lastRequest
#         def query_side_effect(model):
#             if model.__name__ == "Users":
#                 mock_user_query = MagicMock()
#                 mock_user_query.filter_by.return_value.first.return_value = ("Bob",)
#                 return mock_user_query
#             elif model.__name__ == "Reservations":
#                 mock_res_query = MagicMock()
#                 # Return None for lastRequest
#                 mock_res_query.filter_by.return_value.order_by.return_value.first.return_value = None
#                 return mock_res_query
        #     else:
        #         return MagicMock()

        # mock_session.query.side_effect = query_side_effect

        # response = self.client.get("/Homepage/4")
        # self.assertEqual(response.status_code, 200)
        # self.assertIn(b"Bob", response.data)
        # # Since no reservation, there should be no status text in the page
        # self.assertNotIn(b"Pending", response.data)
        # self.assertNotIn(b"Approved", response.data)
        # self.assertNotIn(b"Rejected", response.data)


class ReportIssueTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("app.session")
    def test_get_report_issue_with_equipment(self, mock_session):
        mock_reservation = MagicMock()
        mock_reservation.facilityId = 4
        mock_reservation.reservedBy = 1

        mock_session.query().filter_by().first.side_effect = [mock_reservation, ("IT202",)]
        mock_session.query().filter_by().all.return_value = [("E-Share",)]

        response = self.client.get("/ReportIssue/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"E-Share", response.data)
        self.assertIn(b"IT202", response.data)



class ViewAllRequestsTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @patch("app.session")
    def test_view_all_requests(self, mock_session):
        mock_reservation = MagicMock()
        mock_reservation.reservationId = 1
        mock_reservation.title = "DS Session"
        mock_reservation.date.isoformat.return_value = "2025-05-26"
        mock_reservation.start.strftime.return_value = "09:00"
        mock_reservation.facilityId = 1
        mock_reservation.reportId = None
        mock_reservation.reservedBy = 1
        mock_reservation.status = 1

        mock_session.query().order_by().all.return_value = [mock_reservation]

        mock_facility = MagicMock()
        mock_facility.buildingId = 1
        mock_session.query().filter_by().first.side_effect = [
            mock_facility,                          
            ("IT202",),                  
            ("IT",),                  
            ("Jood Wafa",),                          
        ]

        response = self.client.get("/ViewAllRequests")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DS Session", response.data)
        self.assertIn(b"2025-05-26", response.data)
        self.assertIn(b"IT", response.data)
        self.assertIn(b"Jood Wafa", response.data)
    
if __name__ == "__main__":
    unittest.main()
