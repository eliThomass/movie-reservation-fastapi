from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from database import Base


class Account(Base):
    __tablename__ = "account"
    
    user_id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

class Movie(Base):
    __tablename__ = "movie"

class Showtime(Base):
    __tablename__ = "showtime"

class Auditorium(Base):
    __tablename__ = "auditorium"

class Seat(Base):
    __tablename__ = "seat"

class Reservation(Base):
    __tablename__ = "reservation"

class ReservationSeat(Base):
    __tablename__ = "reservation_seats"

Index("idx_showtime_movie_id", Showtime.movie_id)
Index("idx_showtime_audit_id", Showtime.audit_id)
Index("idx_seat_audit_id", Seat.audit_id)
Index("idx_reservation_account", Reservation.account_id)
Index("idx_reservation_showtime", Reservation.showtime_id)
Index("idx_reservation_seats_show", ReservationSeat.showtime_id)
Index("idx_reservation_seats_seat", ReservationSeat.seat_id)