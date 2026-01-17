"""Public API endpoint for chatbot configuration (no auth required)."""
from flask import request
from flask_restx import Resource, fields, marshal_with

from controllers.web import web_ns
from extensions.ext_database import db
from libs.helper import ChatbotIconUrlField
from models.model import Site


chatbot_config_fields = {
    "chatbot_icon_type": fields.String,
    "chatbot_icon": fields.String,
    "chatbot_icon_background": fields.String,
    "chatbot_icon_url": ChatbotIconUrlField,
}


@web_ns.route("/public/chatbot-config")
class PublicChatbotConfigApi(Resource):
    """Public API to get chatbot icon configuration without authentication."""

    @web_ns.doc("get_public_chatbot_config")
    @web_ns.doc(description="Get chatbot icon configuration by app code (public, no auth required)")
    @web_ns.doc(
        params={
            "code": "The app access token/code"
        }
    )
    @web_ns.doc(
        responses={
            200: "Success",
            400: "Missing code parameter",
            404: "App not found",
        }
    )
    @marshal_with(chatbot_config_fields)
    def get(self):
        """Get chatbot config by app code."""
        code = request.args.get("code")
        if not code:
            return {"error": "Missing code parameter"}, 400

        site = db.session.query(Site).filter(Site.code == code).first()
        if not site:
            return {"error": "App not found"}, 404

        return site
