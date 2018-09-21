from flask_login import UserMixin
from . import db


excursions_users = db.Table(
    "excursions_users",
    db.Column("excursion_id", db.Integer, db.ForeignKey("excursions.id"),
              primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"),
              primary_key=True)
)


class Permission:
    JOIN = 1
    LEAD = 2
    CREATE = 4
    ASSIGN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.JOIN],
            'Guide': [Permission.LEAD],
            'Organization': [Permission.CREATE, Permission.ASSIGN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    navi_token = db.Column(db.String(36), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    own_excursions = db.relationship("Excursion", backref="owner",
                                     lazy="dynamic")
    guided_excursions = db.relationship("Excursion", backref="guide",
                                        lazy="dynamic")
    excursions = db.relationship("Excursion", secondary=excursions_users,
                                 lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()


class Excursion(db.Model):
    __tablename__ = "excursions"
    id = db.Column(db.Integer, primary_key=True)
    container = db.Column(db.String(10), nullable=False)
    naviaddress = db.Column(db.String(20), nullable=False, unique=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    guide_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    members = db.relationship("Users", secondary=excursions_users,
                              lazy="dynamic")
