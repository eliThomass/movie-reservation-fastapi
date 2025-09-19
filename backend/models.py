from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Index, Computed, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class Account(Base):
    __tablename__ = "account"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    password = Column(String, nullable=False)
    start_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    maturity = Column(String(5), nullable=False, default="NR")
    runtime = Column(Integer, nullable=False)
    genre = Column(String(30))
    poster_url = Column(Text)

class Showtime(Base):
    __tablename__ = "showtime"

    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movie.id", ondelete="RESTRICT"), nullable=False)
    audit_id = Column(Integer, ForeignKey("auditorium.id", ondelete="RESTRICT"), nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)
    runtime_min = Column(Integer, nullable=False)
    base_price_cents = Column(Integer, nullable=False)
    end_at = Column(
        DateTime(timezone=True),
        Computed("start_at + (runtime_min * INTERVAL '1 minute')", persisted=True)
    )

    movie = relationship("Movie", back_populates="showtimes")
    auditorium = relationship("Auditorium", back_populates="showtimes")

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