"""
Keycloak Setup Script
Automates the creation of the Agricultural Realm and Clients.
Requires: python-keycloak
"""
import logging
import sys

logging.basicConfig(level=logging.INFO)

try:
    from keycloak import KeycloakAdmin
    HAS_KEYCLOAK = True
except ImportError:
    HAS_KEYCLOAK = False
    logging.warning("python-keycloak module not found. Running in MOCK mode.")

def setup_realm():
    if not HAS_KEYCLOAK:
        logging.info("[MOCK] Connecting to Keycloak at http://localhost:8080...")
        logging.info("[MOCK] Creating realm 'agric_realm'...")
        logging.info("[MOCK] Creating client 'agric_app'...")
        logging.info("[MOCK] Creating roles 'farmer', 'buyer', 'admin'...")
        logging.info("[MOCK] Realm setup complete.")
        return

    try:
        keycloak_admin = KeycloakAdmin(server_url="http://localhost:8080/auth/",
                                       username='admin',
                                       password='admin',
                                       realm_name="master",
                                       verify=True)
        
        # Create Realm
        new_realm = {
            "realm": "agric_realm",
            "enabled": True,
            "displayName": "Agricultural Supply Chain"
        }
        keycloak_admin.create_realm(payload=new_realm)
        logging.info("Realm 'agric_realm' created.")
        
        # Switch to new realm
        keycloak_admin.realm_name = "agric_realm"
        
        # Create Client
        new_client = {
            "clientId": "agric_app",
            "enabled": True,
            "publicClient": True,
            "directAccessGrantsEnabled": True,
            "redirectUris": ["http://localhost:3000/*"]
        }
        keycloak_admin.create_client(payload=new_client)
        logging.info("Client 'agric_app' created.")
        
    except Exception as e:
        logging.error(f"Failed to setup Keycloak: {e}")

if __name__ == "__main__":
    setup_realm()
