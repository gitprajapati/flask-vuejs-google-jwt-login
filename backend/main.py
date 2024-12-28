from flask import Flask, jsonify, redirect, request, url_for
from flask_cors import CORS
from flask_jwt_extended import create_access_token, JWTManager
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import os
from google.auth.transport.requests import Request
from flask_jwt_extended import decode_token
from flask_jwt_extended import jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
CORS(app)
JWTManager(app)

# Google OAuth2 Configuration
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # For development purposes
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://127.0.0.1:5000/auth/callback"
flow = Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri=REDIRECT_URI,
)

super_admin_email = ["abhishek.abhi.prasad6@gmail.com"]

@app.route("/auth/google", methods=["GET"])
def google_login():
    authorization_url, _ = flow.authorization_url()
    return redirect(authorization_url)


@app.route("/auth/callback", methods=["GET"])
def google_callback():
    try:
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
        
        # Verify Google ID Token
        id_info = id_token.verify_oauth2_token(
            credentials.id_token, 
            Request(), 
            CLIENT_ID,
            clock_skew_in_seconds=10
        )
        
        print("Google ID Token Info:", id_info)  # Log ID token info
        
        # Generate JWT token
        if id_info["email"] in super_admin_email:
            token = create_access_token(identity={"email": id_info["email"], "role": "admin"}, additional_claims={"sub": {"email": id_info["email"], "role": "admin"}})

        else:
            token = create_access_token(identity={"email": id_info["email"], "role": "user"}, additional_claims={"sub": {"email": id_info["email"], "role": "user"}})

        
        print("Generated JWT Token:", token)  # Log JWT token
        
        # Redirect with token in the query parameter
        return redirect(f"http://localhost:8080/?token={token}")
    
    except ValueError as e:
        print("Callback Error:", str(e))
        return jsonify({"message": "Invalid token", "error": str(e)}), 400
    except Exception as e:
        print("Callback Unexpected Error:", str(e))
        return jsonify({"message": "Authentication failed", "error": str(e)}), 500


@app.route("/auth/verify", methods=["POST"])
def verify_token():
    token = request.json.get("token")

    print("Received Token for Verification:", token)
    if not token:
        print("Token Missing")
        return jsonify({"message": "Token is missing"}), 400
    
    try:
        decoded = decode_token(token)
        print("Decoded Token:", str(decoded))
        return jsonify({"message": "Token is valid"}), 200
    except Exception as e:
        print("Token Verification Failed:", str(e))
        return jsonify({"message": "Invalid token", "error": str(e)}), 401

@app.route("/admin/protected", methods=["GET"])
@jwt_required()
def admin_protected():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"message": "Admins only!"}), 403
    return jsonify({"message": "Welcome, Admin!"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
