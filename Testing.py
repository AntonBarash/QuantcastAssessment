import unittest
import io
import sys
import most_active_cookie
from Cookie_Class import Cookie

class Converting_Date_Test(unittest.TestCase):
    def test1(self):
        self.assertEqual(most_active_cookie.convert_date_string_to_int('2000-01-01'),20000101)

    def test2(self):
        self.assertEqual(most_active_cookie.convert_date_string_to_int('0000-01-01'),101)

    def test3(self):
        self.assertEqual(most_active_cookie.convert_date_string_to_int('1234-01-01'),12340101)

class Analyze_Line_Test(unittest.TestCase):
    def test1(self):
        cookie1_values = ('AtY0laUfhglK3lC7','2018-12-09','14:19:00+00:00')
        self.assertEqual(most_active_cookie.analyze_line('AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00'),cookie1_values)

    def test2(self):
        cookie2_values = ('A','2000-01-01','1')
        self.assertEqual(most_active_cookie.analyze_line('A,2000-01-01T1'),cookie2_values)

    def test3(self):
        cookie3_values = ('','0000-01-01','')
        self.assertEqual(most_active_cookie.analyze_line(',0000-01-01T'),cookie3_values)

class Find_Cookie_Dict_Test(unittest.TestCase):
    def test1(self):
        file = open('cookie_log.csv','r')
        self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-09'),{'AtY0laUfhglK3lC7':2,'SAZuXPGUrfbcn5UA':1,'5UAVanZf6UtGyKVS':1})

    def test2(self):
        file = open('cookie_log.csv','r')
        self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-08'),{'SAZuXPGUrfbcn5UA':1,'4sMM2LxV07bPJzwf':1,'fbcn5UAVanZf6UtG':1})

    def test3(self):
        file = open('cookie_log.csv','r')
        self.assertEqual(most_active_cookie.find_cookie_dict_of_day(file, '2018-12-07'),{'4sMM2LxV07bPJzwf':1})

    def test4(self):
        file = open('cookie_log.csv','r')
        try:
            most_active_cookie.find_cookie_dict_of_day(file, '2018-12-06')
        except Exception as e:
            self.assertEqual(str(e),'No cookies on this date were found')
            return
        raise Exception('Find cookie dict test #4 didnt produce error when it should have')

class Checking_Date_Format_Test(unittest.TestCase):
    def test1(self):
        try:
            most_active_cookie.check_valid_date('notten')
        except Exception as e:
            self.assertEqual(str(e),'Date should be 10 characters')
            return
        raise Exception('Checking date format test #1 didnt produce error when it should have')

    def test2(self):
        try:
            most_active_cookie.check_valid_date('tennodash1')
        except Exception as e:
            self.assertEqual(str(e),'Date should have 2 dashes separating the year, month, and day values, has 0')
            return
        raise Exception('Checking date format test #2 didnt produce error when it should have')

    def test3(self):
        try:
            most_active_cookie.check_valid_date('100-000000')
        except Exception as e:
            self.assertEqual(str(e),'Year should be of length 4')
            return
        raise Exception('Checking date format test #3 didnt produce error when it should have')

    def test4(self):
        try:
            most_active_cookie.check_valid_date('10a0-00000')
        except Exception as e:
            self.assertEqual(str(e),'Year must be an integer')
            return
        raise Exception('Checking date format test #4 didnt produce error when it should have')

    def test5(self):
        try:
            most_active_cookie.check_valid_date('1000-55000')
        except Exception as e:
            self.assertEqual(str(e),'Date should have 2 dashes separating the year, month, and day values, has 1')
            return
        raise Exception('Checking date format test #5 didnt produce error when it should have')

    def test6(self):
        try:
            most_active_cookie.check_valid_date('1000-100-0')
        except Exception as e:
            self.assertEqual(str(e),'Month should be of length 2')
            return
        raise Exception('Checking date format test #6 didnt produce error when it should have')

    def test7(self):
        try:
            most_active_cookie.check_valid_date('1000-5a-00')
        except Exception as e:
            self.assertEqual(str(e),'Month must be an integer')
            return
        raise Exception('Checking date format test #7 didnt produce error when it should have')

    def test8(self):
        try:
            most_active_cookie.check_valid_date('1000-13-00')
        except Exception as e:
            self.assertEqual(str(e),'Month must be between 1 and 12')
            return
        raise Exception('Checking date format test #8 didnt produce error when it should have')

    def test9(self):
        try:
            most_active_cookie.check_valid_date('1000-10-0a')
        except Exception as e:
            self.assertEqual(str(e),'Day must be an integer')
            return
        raise Exception('Checking date format test #9 didnt produce error when it should have')

    def test10(self):
        try:
            most_active_cookie.check_valid_date('1000-10-32')
        except Exception as e:
            self.assertEqual(str(e),'Day must be between 1 and 31')
            return
        raise Exception('Checking date format test #10 didnt produce error when it should have')

class Find_Most_Active_Cookie_Test(unittest.TestCase):
    def test1(self):
        output = io.StringIO()
        sys.stdout = output
        file = open('cookie_log.csv','r')
        most_active_cookie.find_most_active_cookie(file,'2018-12-09')
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue(),'AtY0laUfhglK3lC7\n')

    def test2(self):
        output = io.StringIO()
        sys.stdout = output
        file = open('cookie_log.csv','r')
        most_active_cookie.find_most_active_cookie(file,'2018-12-08')
        sys.stdout = sys.__stdout__
        list_of_cookies = output.getvalue().split('\n')
        list_of_cookies.sort()
        list_of_cookies.remove('')
        self.assertEqual(list_of_cookies,['4sMM2LxV07bPJzwf','SAZuXPGUrfbcn5UA','fbcn5UAVanZf6UtG'])

    def test3(self):
        output = io.StringIO()
        sys.stdout = output
        file = open('cookie_log.csv','r')
        most_active_cookie.find_most_active_cookie(file,'2018-12-07')
        sys.stdout = sys.__stdout__
        self.assertEqual(output.getvalue(),'4sMM2LxV07bPJzwf\n')

    def test4(self):
        output = io.StringIO()
        sys.stdout = output
        file = open('cookie_log.csv','r')
        try:
            most_active_cookie.find_most_active_cookie(file,'2018-12-06')
        except Exception as e:
            self.assertEqual(str(e),'No cookies on this date were found')
            return
        raise Exception('Find most active cookie test #4 didnt produce error when it should have')


Converting_Date_Test().test1()
Converting_Date_Test().test2()
Converting_Date_Test().test3()

Analyze_Line_Test().test1()
Analyze_Line_Test().test2()
Analyze_Line_Test().test3()

Find_Cookie_Dict_Test().test1()
Find_Cookie_Dict_Test().test2()
Find_Cookie_Dict_Test().test3()
Find_Cookie_Dict_Test().test4()

Checking_Date_Format_Test().test1()
Checking_Date_Format_Test().test2()
Checking_Date_Format_Test().test3()
Checking_Date_Format_Test().test4()
Checking_Date_Format_Test().test5()
Checking_Date_Format_Test().test6()
Checking_Date_Format_Test().test7()
Checking_Date_Format_Test().test8()
Checking_Date_Format_Test().test9()
Checking_Date_Format_Test().test10()

Find_Most_Active_Cookie_Test().test1()
Find_Most_Active_Cookie_Test().test2()
Find_Most_Active_Cookie_Test().test3()
Find_Most_Active_Cookie_Test().test4()
