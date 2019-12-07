import unittest

from room.models import Room


class TestStringMethods(unittest.TestCase):
    # # # # # # # # # # # # # # # # # # # # #
    def test_everything_ok_with_two_rooms(self):
        pass
        # MOCK OBJECTS #


test_room_1 = Room(126, 'B2', 125, 0, 'BRAK')
test_room_2 = Room(127, 'B2', 125, 0, 'BRAK')
test_room_3 = Room(128, 'B2', 125, 0, 'BRAK')
test_room_4 = Room(129, 'B2', 125, 0, 'BRAK')
test_room_5 = Room(130, 'B2', 125, 10, 'BRAK')

room_list = [test_room_1, test_room_2, test_room_3, test_room_4, test_room_5]

test_reservation_1 = Reservation(date(2019, 10, 3), time(8, 0), 1, test_room_1, True, 'ZIMOWY', True)
test_reservation_2 = Reservation(date(2019, 10, 4), time(8, 0), 1, test_room_2, True, 'ZIMOWY', True)
test_reservation_3 = Reservation(date(2019, 10, 5), time(8, 0), 1, test_room_3, True, 'ZIMOWY', True)
test_reservation_4 = Reservation(date(2019, 10, 6), time(8, 0), 1, test_room_4, True, 'ZIMOWY', True)
test_reservation_5 = Reservation(date(2019, 10, 7), time(8, 0), 1, test_room_5, True, 'ZIMOWY', True)
