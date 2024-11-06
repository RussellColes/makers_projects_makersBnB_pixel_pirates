from lib.booking import Booking
import datetime


class BookingRepository:
    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all bookings
    def all(self):
        rows = self._connection.execute('SELECT * FROM bookings')
        bookings = []
        for row in rows:
            start_date_str = row["start_date"].strftime('%Y-%m-%d') if isinstance(row["start_date"], datetime.date) else row["start_date"]
            end_date_str = row["end_date"].strftime('%Y-%m-%d') if isinstance(row["end_date"], datetime.date) else row["end_date"]
            item = Booking(row["id"], start_date_str, end_date_str, row["status"], row["total_price"], row["space_id"], row["user_id"])
            bookings.append(item)
        return bookings
    
    
    def find(self, id):
        rows = self._connection.execute(
            'SELECT * from bookings WHERE id = %s', [id])
        row = rows[0]
        start_date_str = row["start_date"].strftime('%Y-%m-%d') if isinstance(row["start_date"], datetime.date) else row["start_date"]
        end_date_str = row["end_date"].strftime('%Y-%m-%d') if isinstance(row["end_date"], datetime.date) else row["end_date"]
            
        return Booking(row["id"], start_date_str, end_date_str, row["status"], row["total_price"], row["space_id"], row["user_id"])
    
    def create(self, booking):
        rows = self._connection.execute(
            'INSERT INTO bookings (start_date, end_date, status, total_price, space_id, user_id) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id', 
            [booking.start_date, booking.end_date, booking.status, booking.total_price, booking.space_id, booking.user_id])
        row = rows[0]
        booking.id = row["id"]
        return booking

    
    def delete(self, id):
        self._connection.execute('DELETE FROM bookings WHERE id = %s', [id])
        return None