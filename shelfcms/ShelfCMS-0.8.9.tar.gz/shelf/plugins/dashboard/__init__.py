from flask_admin.base import AdminIndexView, expose
from flask import Blueprint

config = {
    "name": "Dashboard",
    "description": "Dashboard-like view using tiles containing text and chart."
}

class DashboardView(AdminIndexView):
    widgets = []

    def add_widget(self, view):
        if not self.widgets:
            self.widgets = []
        self.widgets.append(view)

    @expose("/")
    def index(self):
        return self.render(self._template, user=current_user, widgets=[w.render() for w in self.widgets])

class Dashboard:
    def __init__(self):
        self.config = config

    def init_app(self, app):
        self.bp = Blueprint("dashboard", __name__, url_prefix="/dashboard",
            static_folder="static", template_folder="templates")
        app.register_blueprint(self.bp)