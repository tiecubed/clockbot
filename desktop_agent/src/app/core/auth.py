"""OAuth Authentication for Desktop Agent"""
import asyncio
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import socket
from .config import config


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Discord"""
    
    def do_GET(self):
        """Handle GET request with auth code"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        
        if 'code' in params:
            self.server.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''
                <html>
                <body style="font-family: sans-serif; text-align: center; padding: 50px;">
                    <h1>Authentication Successful</h1>
                    <p>You can close this window and return to the Time Tracker Agent.</p>
                </body>
                </html>
            '''
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Error: No code received')
    
    def log_message(self, format, *args):
        """Suppress HTTP server logs"""
        pass


class OAuthHandler:
    """Handle Discord OAuth flow for agent authentication"""
    
    DISCORD_OAUTH_URL = "https://discord.com/oauth2/authorize"
    REDIRECT_URI = f"http://localhost:{config.OAUTH_REDIRECT_PORT}/oauth/callback"
    
    def __init__(self):
        self.client_id = config.DISCORD_CLIENT_ID
        self.auth_code = None
    
    def start_login(self) -> str:
        """
        Start OAuth login flow
        Returns: URL to open in browser
        """
        if not self.client_id:
            raise ValueError("DISCORD_CLIENT_ID not configured")
        
        auth_url = (
            f"{self.DISCORD_OAUTH_URL}?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.REDIRECT_URI}&"
            f"response_type=code&"
            f"scope=identify"
        )
        return auth_url
    
    async def wait_for_callback(self, timeout: int = 120):
        """
        Start local HTTP server and wait for OAuth callback
        Returns: auth_code or None if timeout/error
        """
        server = HTTPServer(('localhost', config.OAUTH_REDIRECT_PORT), OAuthCallbackHandler)
        server.auth_code = None
        
        # Run server in thread
        import threading
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        
        # Wait for callback
        start_time = asyncio.get_event_loop().time()
        while server.auth_code is None:
            await asyncio.sleep(0.1)
            if asyncio.get_event_loop().time() - start_time > timeout:
                server.shutdown()
                return None
        
        server.shutdown()
        return server.auth_code
    
    async def exchange_code_for_token(self, code: str):
        """
        Exchange OAuth code for API token via backend
        Returns: {token, user_id, username} or raises error
        """
        # This would call the backend to exchange code
        # For now, return structure
        return {
            'token': '',
            'user_id': '',
            'username': ''
        }
    
    async def complete_login(self):
        """
        Full login flow: open browser, wait for callback, exchange code
        Returns: auth data or None
        """
        # Open browser
        auth_url = self.start_login()
        webbrowser.open(auth_url)
        
        # Wait for callback
        code = await self.wait_for_callback()
        if not code:
            return None
        
        # Exchange for token
        return await self.exchange_code_for_token(code)
