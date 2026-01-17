
from app import create_app
from extensions.ext_database import db
from models.model import Site
from controllers.console.app.site import app_site_model
from flask_restx import marshal

app = create_app()
with app.app_context():
    s = db.session.query(Site).filter(Site.code == 'I8He0TGq1royQLOl').first()
    if s:
        print(f"DB Icon Type: {s.chatbot_icon_type}")
        print("-" * 20)
        res = marshal(s, app_site_model)
        import json
        print(json.dumps(res, indent=2))
    else:
        print("Site not found")
