from django.test import TestCase, Client
from django.contrib.auth.models import User
from analytics.models import RequestLog
from analytics.middleware import RequestLoggingMiddleware
from django.http import HttpResponse
from django.test import RequestFactory
import json


class RequestLoggingMiddlewareTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def get_response_mock(self, request):
        """Mock response function for middleware testing"""
        return HttpResponse('OK')

    def test_get_request_logging(self):
        """Test that GET requests are logged properly"""
        initial_count = RequestLog.objects.count()

        # Make a GET request
        response = self.client.get('/admin/', {'param1': 'value1'})
        self.assertEqual(response.status_code, 302)

        # Check that a log entry was created
        self.assertEqual(RequestLog.objects.count(), initial_count + 1)

        log_entry = RequestLog.objects.latest('timestamp')
        self.assertEqual(log_entry.method, 'GET')
        self.assertEqual(log_entry.path, '/admin/')
        self.assertEqual(log_entry.query_string, 'param1=value1')
        self.assertEqual(log_entry.post_params, '')
        self.assertIsNotNone(log_entry.ip_address)

    def test_post_request_logging(self):
        """Test that POST requests with data are logged properly"""
        initial_count = RequestLog.objects.count()

        # Make a POST request with data
        post_data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post('/admin/login/', post_data)
        self.assertEqual(response.status_code, 200)

        # Check that a log entry was created
        self.assertEqual(RequestLog.objects.count(), initial_count + 1)

        log_entry = RequestLog.objects.latest('timestamp')
        self.assertEqual(log_entry.method, 'POST')
        self.assertEqual(log_entry.path, '/admin/login/')
        print(f'POST request: {log_entry.post_params}')
        """
        POST request: --BoUnDaRyStRiNg
        Content-Disposition: form-data; name="username"

        testuser
        --BoUnDaRyStRiNg
        Content-Disposition: form-data; name="password"

        testpass
        --BoUnDaRyStRiNg--

        OR
        csrfmiddlewaretoken=udrQsBavCYAqpAXpMbyJ7aX7gMCNCcfWZWWJXs5bVgV79UAo72DoQ0CWIRsIYPL0&username=victor&password=Zuliani2*&next=%2Fadmin%2F
        """
        self.assertIn('testuser', log_entry.post_params)
        self.assertIn('testpass', log_entry.post_params)

    def test_authenticated_user_logging(self):
        """Test that authenticated user requests are logged with user info"""
        self.client.login(username='testuser', password='testpass123')
        initial_count = RequestLog.objects.count()

        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

        log_entry = RequestLog.objects.latest('timestamp')
        self.assertEqual(log_entry.user, self.user)
        self.assertEqual(log_entry.user_display, 'testuser')
        final_count = RequestLog.objects.count()
        self.assertEqual(final_count, initial_count + 1)

    def test_anonymous_user_logging(self):
        """Test that anonymous user requests are logged without user info"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

        log_entry = RequestLog.objects.latest('timestamp')
        self.assertIsNone(log_entry.user)
        self.assertEqual(log_entry.user_display, 'Anonymous')

    def test_skip_static_files(self):
        """Test that static files are not logged"""
        middleware = RequestLoggingMiddleware(self.get_response_mock)

        # Test static file request
        request = self.factory.get('/static/css/style.css')
        self.assertTrue(middleware.should_skip_logging(request))

        # Test media file request
        request = self.factory.get('/media/images/logo.png')
        self.assertTrue(middleware.should_skip_logging(request))

        # Test favicon request
        request = self.factory.get('/favicon.ico')
        self.assertTrue(middleware.should_skip_logging(request))

        # Test normal request should not be skipped
        request = self.factory.get('/admin/')
        self.assertFalse(middleware.should_skip_logging(request))

    def test_json_post_data_logging(self):
        """Test that JSON POST data is logged properly"""
        middleware = RequestLoggingMiddleware(self.get_response_mock)

        json_data = {'key': 'value', 'number': 42}
        request = self.factory.post(
            '/api/endpoint/',
            data=json.dumps(json_data),
            content_type='application/json'
        )
        # Add user authentication state to the request
        request.user = self.user

        response = middleware(request)
        self.assertEqual(response.status_code, 200)

        log_entry = RequestLog.objects.latest('timestamp')
        self.assertEqual(log_entry.method, 'POST')
        self.assertIn('key', log_entry.post_params)
        self.assertIn('value', log_entry.post_params)

    def test_response_time_logging(self):
        """Test that response time is logged"""

        response = self.client.get('/admin/')
        # we expect a redirection to login
        self.assertEqual(response.status_code, 302)

        log_entry = RequestLog.objects.latest('timestamp')
        self.assertIsNotNone(log_entry.response_time_ms)
        self.assertGreater(log_entry.response_time_ms, 0)

    def test_ip_address_extraction(self):
        """Test IP address extraction from headers"""
        middleware = RequestLoggingMiddleware(self.get_response_mock)

        # Test with X-Forwarded-For header
        request = self.factory.get('/')
        request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'
        ip = middleware.get_client_ip(request)
        self.assertEqual(ip, '192.168.1.1')

        # Test without X-Forwarded-For header
        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        ip = middleware.get_client_ip(request)
        self.assertEqual(ip, '127.0.0.1')
