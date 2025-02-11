from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

# Import Blueprints
from displayvendor import display_vendor_bp  # Corrected Blueprint name



from add_vendor import add_vendor_bp
from budget import budget_bp
from checklist_api import checklist_bp

from guest_list_api import guest_list_bp
from rsvp_api import rsvp_bp
from signin import signin_bp
from signup import signup_bp
from taskmanagement import task_bp
from update import update_bp
from vendor_categories import vendor_categories_bp
from vendor_details import vendor_details_bp
from vendor_review import vendor_review_bp
from vendorlist import vendorlist_bp
from reset import reset_bp, init_mongo as init_reset_mongo  

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/api"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Initialize MongoDB for reset module
init_reset_mongo(app)

# Register Blueprints
app.register_blueprint(add_vendor_bp, url_prefix='/add_vendor')
app.register_blueprint(budget_bp, url_prefix='/budget')
app.register_blueprint(checklist_bp, url_prefix='/checklist')
# Register the corrected Blueprint
app.register_blueprint(display_vendor_bp, url_prefix='/displayvendor')
app.register_blueprint(guest_list_bp, url_prefix='/guest_list')
app.register_blueprint(rsvp_bp, url_prefix='/rsvp')
app.register_blueprint(signin_bp, url_prefix='/signin')
app.register_blueprint(signup_bp, url_prefix='/signup')
app.register_blueprint(task_bp, url_prefix='/tasks')
app.register_blueprint(update_bp, url_prefix='/update')
app.register_blueprint(vendor_categories_bp, url_prefix='/vendor_categories')
app.register_blueprint(vendor_details_bp, url_prefix='/vendor_details')
app.register_blueprint(vendor_review_bp, url_prefix='/vendor_review')
app.register_blueprint(vendorlist_bp, url_prefix='/vendorlist')
app.register_blueprint(reset_bp, url_prefix='/reset')

if __name__ == "__main__":
    app.run(debug=True)
