import datetime
import uuid
import jwt
import requests
import logging
import traceback
import time

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TableauEmbeddingService:
    def __init__(self, server_url, site_id,secret_id,  secret_value, client_id):
        self.server_url = server_url.rstrip('/')
        self.site_id = site_id
        self.secret_id = secret_id
        self.secret_value = secret_value
        self.client_id = client_id
        logger.info(f"Initializing TableauEmbeddingService with server URL: {server_url}")
        
    def _get_server_connection(self):
        """Use the generated JWT to create an authenticated session."""
        try:
            jwt_token = self._generate_jwt()
            headers = {
                "Authorization": f"Bearer {jwt_token}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            return headers
        except Exception as e:
            logger.error(f"Error creating server connection: {str(e)}")
            raise Exception(f"Failed to create server connection: {str(e)}")
        
    def _generate_jwt(self):
        """Generate a JWT token for Connected App authentication."""
        try:
            now = int(time.time())
            exp = now + (5 * 60)  # Token expiration in 5 minutes
            
            # JWT Payload
            payload = {
                "iss": self.client_id,
                "exp": exp,
                "iat": now,
                "jti": str(uuid.uuid4()),
                "aud": "tableau",
                "sub": "samuel.fabrizio@gmail.com",
                "scp": ["tableau:views:embed"],
                "https://tableau.com/oda": "true",
                "site": {"id": self.site_id}  # Include site ID
            }
            
            # JWT Headers
            headers = {
                "typ": "JWT",
                "kid": self.secret_id,  # Correctly set secret ID here
                "alg": "HS256"  
            }

            # Generate the token
            token = jwt.encode(
                payload,
                self.secret_value,
                algorithm="HS256",
                headers=headers
            )

            logger.debug(f"Generated JWT headers: {headers}")
            logger.debug(f"Generated JWT payload: {payload}")

            # Optional: Validate token structure without expiration
            try:
                decoded = jwt.decode(
                    token, 
                    self.secret_value, 
                    algorithms=["HS256"],
                    audience="tableau",
                    options={"verify_exp": False}  
                )
                logger.debug(f"Token structure valid (ignoring expiration): {decoded}")
            except Exception as e:
                logger.error(f"Token structure verification failed: {str(e)}")
                raise
                
            return token

        except Exception as e:
            logger.error(f"Error generating JWT: {str(e)}")
            logger.error(traceback.format_exc())
            raise Exception(f"Failed to generate JWT: {str(e)}")


    def _validate_response(self, response, operation):
        """Validate the API response and provide detailed error logging."""
        if response.status_code != 200:
            logger.error(f"Error in {operation} - Status Code: {response.status_code}")
            logger.error(f"Response Headers: {response.headers}")
            logger.error(f"Response Content: {response.text}")
            try:
                error_json = response.json()
                logger.error(f"Error JSON: {error_json}")
            except Exception:
                logger.error(f"Raw response content: {response.content}")
            response.raise_for_status()

    def list_workbooks_and_views(self):
        """List all workbooks and their views."""
        try:
            headers = self._get_server_connection()
            url = f"{self.server_url}/api/3.15/sites/{self.site_id}/workbooks"
            
            response = requests.get(url, headers=headers)
            self._validate_response(response, "list_workbooks_and_views")
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error in list_workbooks_and_views: {str(e)}")
            raise Exception(f"Failed to list workbooks: {str(e)}")

    def get_embed_url(self, workbook_id, view_id):
        """Get embed URL for a specific view"""
        try:
            headers = self._get_server_connection()
            url = f"{self.server_url}/api/3.15/sites/{self.site_id}/views/{view_id}"
            
            response = requests.get(url, headers=headers)
            self._validate_response(response, "get_embed_url")
            
            view_data = response.json()
            embed_url = f"{self.server_url}/t/{self.site_id}/views/{view_id}"
            return embed_url
            
        except Exception as e:
            logger.error(f"Error in get_embed_url: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise Exception(f"Failed to generate embed URL: {str(e)}")