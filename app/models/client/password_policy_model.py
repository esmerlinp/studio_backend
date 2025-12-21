from ...extensions import db
from flask import g

class PasswordPolicy(db.Model):
    __tablename__ = "politicascontrasenas"
    #__table_args__ = {"schema": "cliente"}


    id = db.Column(
        "idpoliticacontrasena",
        db.Integer,
        primary_key=True
    )

    require_uppercase = db.Column(
        "bmayuscula",
        db.Boolean,
        nullable=False,
        default=True
    )

    require_lowercase = db.Column(
        "bminuscula",
        db.Boolean,
        nullable=False,
        default=True
    )

    require_numbers = db.Column(
        "bnumeros",
        db.Boolean,
        nullable=False,
        default=True
    )

    require_special_chars = db.Column(
        "bcaracteresp",
        db.Boolean,
        nullable=False,
        default=True
    )

    min_length = db.Column(
        "ilongitudminima",
        db.SmallInteger,
        nullable=False,
        default=8
    )

    expire_months = db.Column(
        "imesesexpira",
        db.SmallInteger,
        nullable=False,
        default=3
    )

    password_history = db.Column(
        "ihistorialcontrasenas",
        db.SmallInteger,
        nullable=False,
        default=5
    )

    max_login_attempts = db.Column(
        "iintentosmaxlogin",
        db.SmallInteger,
        nullable=False,
        default=3
    )

    def __repr__(self):
        return f"<PasswordPolicy id={self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "require_uppercase": self.require_uppercase,
            "require_lowercase": self.require_lowercase,
            "require_numbers": self.require_numbers,
            "require_special_chars": self.require_special_chars,
            "min_length": self.min_length,
            "expire_months": self.expire_months,
            "password_history": self.password_history,
            "max_login_attempts": self.max_login_attempts
        }

        
