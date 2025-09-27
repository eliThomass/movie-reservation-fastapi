from sqlalchemy import (Boolean, Column, ForeignKey, Integer, String, 
                        DateTime, Index, Computed, Text, UniqueConstraint, Enum
                        )
from sqlalchemy.sql import func, column
from sqlalchemy.dialects.postgresql import ExcludeConstraint
import enum
from sqlalchemy.orm import relationship
from database import Base

class ReservationStatusEnum(enum.Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    EXPIRED = 'EXPIRED'
    REFUNDED = 'REFUNDED'

class Account(Base):
    __tablename__ = "account"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    password = Column(String, nullable=False)
    start_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    points = Column(Integer, nullable=False, server_default='0')

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

    __table_args__ = (
        ExcludeConstraint(
            ('audit_id', '='),
            (func.tstzrange(column('start_at'), column('end_at'), '()'), '&&'),
            name='no_overlap_in_auditorium'
        ),
    )

    movie = relationship("Movie", back_populates="showtimes")
    auditorium = relationship("Auditorium", back_populates="showtimes")

class Auditorium(Base):
    __tablename__ = "auditorium"

    id = Column(Integer, primary_key=True, autoincrement=True)
    seat_rows = Column(Integer, nullable=False)
    seat_cols = Column(Integer, nullable=False)
    capacity = Column(Integer, Computed('seat_rows * seat_cols', persisted=True))

class Seat(Base):
    __tablename__ = "seat"

    id = Column(Integer, primary_key=True, autoincrement=True)
    audit_id = Column(Integer, ForeignKey("auditorium.id", ondelete="CASCADE"), nullable=False)
    row_number = Column(Integer, nullable=False)
    seat_number = Column(Integer, nullable=False)
    row_label = Column(String(1))

    __table_args__ = (
        UniqueConstraint('audit_id', 'row_number', 'seat_number', name='uq_audit_row_seat_num'),
        UniqueConstraint('audit_id', 'row_label', 'seat_number', name='uq_audit_row_seat_label')
    )

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    showtime_id = Column(Integer, ForeignKey('showtime.id', ondelete='RESTRICT'), nullable=False)
    total_price_cents = Column(Integer, nullable=False, server_default='0')
    status = Column(
        Enum(ReservationStatusEnum, name='reservation_status'), 
        nullable=False, 
        server_default='PENDING'
    )
    payment_provider = Column(Text)
    payment_ref = Column(Text)
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    cancelled_at = Column(DateTime(timezone=True))

class ReservationSeat(Base):
    __tablename__ = "reservation_seats"
    reservation_id = Column(Integer, ForeignKey('reservation.id', ondelete='CASCADE'), primary_key=True)
    seat_id = Column(Integer, ForeignKey('seat.id', ondelete='RESTRICT'), primary_key=True)
    showtime_id = Column(Integer, ForeignKey('showtime.id', ondelete='RESTRICT'), nullable=False)
    price_cents = Column(Integer, nullable=False, server_default='0')

    __table_args__ = (
        UniqueConstraint('showtime_id', 'seat_id', name='uq_res_seat_showtime'),
    )

Index("idx_showtime_movie_id", Showtime.movie_id)
Index("idx_showtime_audit_id", Showtime.audit_id)
Index("idx_seat_audit_id", Seat.audit_id)
Index("idx_reservation_account", Reservation.account_id)
Index("idx_reservation_showtime", Reservation.showtime_id)
Index("idx_reservation_seats_show", ReservationSeat.showtime_id)
Index("idx_reservation_seats_seat", ReservationSeat.seat_id)