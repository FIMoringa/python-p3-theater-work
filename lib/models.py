from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Audition(Base):
    __tablename__ = "auditions"
    id = Column(Integer, primary_key=True)
    actor = Column(String(255))
    location = Column(String(255))
    phone = Column(Integer(255))
    hired = Column(Boolean)
    role_id = Column(Integer, ForeignKey("role.id"))
    role = relationship("Role", backref=backref("auditions", uselist=True))

    def __repr__(self):
        return f"{self.actor} auditioned for {self.role} at {self.location}."

    # return role
    def role(self):
        return self.role

    def audition_callback(self):
        self.hired = True


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    character_name = Column(String(255))
    audition_id = Column(Integer, ForeignKey("auditions.id"))
    audition = relationship("Audition", backref=backref("role", uselist=False))

    # Role.auditions returns all of the auditions associated with this role.
    def auditions(self):
        return self.auditions

    def actors(self):
        return self.actors

    # def  returns a list of locations from the auditions associated with this role.
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        #  returns the first instance of the audition that was hired for this role or returns a string 'no actor has been hired for this role'
        return self.auditions.filter_by(hired=True).first() or "no actor has been hired for this role"
    # Role.understudy() returns the second instance of the audition that was hired for this role or returns a string 'no actor has been hired for understudy for this role'.
    def understudy(self):
        return self.auditions.filter_by(hired=True).all()[1] or "no actor has been hired for understudy for this role"