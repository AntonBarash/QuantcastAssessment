import unittest
import most_active_cookie
from Cookie_Class import Cookie

class Converting_Date_Test(unittest.TestCase):
    def test(self):
        self.assertEqual(most_active_cookie.convert_date_string_to_int('2000-01-01'),20000101)
        self.assertEqual(most_active_cookie.convert_date_string_to_int('0000-01-01'),101)
        self.assertEqual(most_active_cookie.convert_date_string_to_int('1234-01-01'),12340101)


class Analyze_Line_Test(unittest.TestCase):
    def test(self):
        cookie1_values = ('AtY0laUfhglK3lC7','2018-12-09','14:19:00+00:00')
        self.assertEqual(most_active_cookie.analyze_line('AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00'),cookie1_values)
        cookie2_values = ('A','2000-01-01','1')
        self.assertEqual(most_active_cookie.analyze_line('A,2000-01-01T1'),cookie2_values)
        cookie3_values = ('','0000-01-01','')
        self.assertEqual(most_active_cookie.analyze_line(',0000-01-01T'),cookie3_values)

class Find_Cookie_Dict_Test(unittest.TestCase):
    def test(self):
        file = open('cookie_log.csv','r')
        self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-09'),{'AtY0laUfhglK3lC7':2,'SAZuXPGUrfbcn5UA':1,'5UAVanZf6UtGyKVS':1})
        file = open('cookie_log.csv','r')
        self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-08'),{'SAZuXPGUrfbcn5UA':1,'4sMM2LxV07bPJzwf':1,'fbcn5UAVanZf6UtG':1})
        file = open('cookie_log.csv','r')
        self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-07'),{'4sMM2LxV07bPJzwf':1})
        #self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-06'),{}) add error check

class Checking_Date_Format_Test(unittest.TestCase):
    def test(self):
        self.assertEqual(most_active_cookie.convert_date_string_to_int('2000-01-01'),20000101)
        self.assertEqual(most_active_cookie.convert_date_string_to_int('0000-01-01'),101)
        self.assertEqual(most_active_cookie.convert_date_string_to_int('1234-56-78'),12345678)
        with self.assertRaisesRegex(Exception, 'z*'):
            most_active_cookie.check_valid_date('1234-5678')

class Full_Program_Test(unittest.TestCase):
    def test(self):
        self.assertEqual(most_active_cookie.find_most_active_cookie('cookie_log.csv','2018-12-09'))
        self.assertEqual(most_active_cookie.find_most_active_cookie('cookie_log.csv','2018-12-08'))
        self.assertEqual(most_active_cookie.find_most_active_cookie('cookie_log.csv','2018-12-07'),'4sMM2LxV07bPJzwf')
        #add test for if cookie doesn't exist

Converting_Date_Test().test()
Analyze_Line_Test().test()
Find_Cookie_Dict_Test().test()
#Checking_Date_Format_Test().test()
#Full_Program_Test().test()
