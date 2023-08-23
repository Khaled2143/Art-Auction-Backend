from MVC.models import Artist


def home():
    return Artist.query.all()