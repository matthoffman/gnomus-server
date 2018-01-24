from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from garden.models import User, Sensor, Bed, db
from garden.extensions import login_manager, admin





# Create customized model view class. Because it sounded like a good idea...
# not sure if this is necessary w/ the AdminIndexView above?
class AuthModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


# Customized User model admin
class UserAdmin(AuthModelView):
    column_display_pk = True


# Add views
admin.add_view(UserAdmin(User, db))
admin.add_view(AuthModelView(Sensor, db))
admin.add_view(AuthModelView(Bed, db))

