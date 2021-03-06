from Cookie_Class import Cookie
import sys

#converts date string to integer representation without dashes
def convert_date_string_to_int(date_str):
    check_valid_date(date_str)
    return int(date_str.replace('-',''))

#analyzes a line from the csv file, finding the cookie name, date, and time from it
def analyze_line(cookie_str):
    try:
        index_of_comma = cookie_str.index(',')
    except:
        raise Exception('No comma in cookie string, it should signal end of cookie name and start of date')
    cookie_name = cookie_str[:index_of_comma]
    try:
        index_of_T = cookie_str[index_of_comma:].index('T') + index_of_comma
    except:
        raise Exception('No T in cookie string after comma, it should signal the end of date and start of time')
    time = cookie_str[index_of_T + 1:-1]
    date_string = cookie_str[index_of_comma + 1:index_of_comma + 11]
    return cookie_name,date_string,time


#binary search function to find a cookie with input date from the cookie list, since list is sorted
def find_cookie_given_date(cookie_list,input_date):
    start = 0
    input_date_int = convert_date_string_to_int(input_date)
    end = len(cookie_list) - 1
    while start <= end:
        current_index = (start + end) // 2
        current_date = cookie_list[current_index].date
        current_date_int = convert_date_string_to_int(current_date)
        if current_date_int == input_date_int:
            return current_index
        elif current_date_int < input_date_int:
            end = current_index - 1
        else:
            start = current_index + 1
    return -1

#finds the dictionary of all the cookies on a day given a file and input date
def find_cookie_dict_of_day(file, input_date):
    list_of_cookies = create_cookie_list(file)
    cookie_index = find_cookie_given_date(list_of_cookies,input_date)
    if cookie_index == -1:
        raise Exception('No cookies on this date were found')
    cookie_dict = {}
    index_after = cookie_index
    index_before = cookie_index - 1
    while(index_after) < len(list_of_cookies):
        cur_cookie_date = list_of_cookies[index_after].date
        cur_cookie_name = list_of_cookies[index_after].name
        if cur_cookie_date != input_date:
            break
        if cur_cookie_name not in cookie_dict:
            cookie_dict[cur_cookie_name] = 0
        cookie_dict[cur_cookie_name] += 1
        index_after += 1
    while(index_before) > -1:
        cur_cookie_date = list_of_cookies[index_before].date
        cur_cookie_name = list_of_cookies[index_before].name
        if cur_cookie_date != input_date:
            break
        if cur_cookie_name not in cookie_dict:
            cookie_dict[cur_cookie_name] = 0
        cookie_dict[cur_cookie_name] += 1
        index_before -= 1
    return cookie_dict

#creates the cookie list given the file
def create_cookie_list(file):
    found_date = False
    cookie_list = []
    check_for_first_line = True
    for line in file:
        if check_for_first_line:
            check_for_first_line = False
        else:
            cookie_name,date,time = analyze_line(line)
            cookie_list.append(Cookie(cookie_name,date,time))
    return cookie_list

#finds most active cookie given the file and input date, prints all of these cookies
def find_most_active_cookie(file, input_date):
    cookie_dict = find_cookie_dict_of_day(file, input_date)
    sorted_cookie_list = sorted(cookie_dict.items(), key = lambda x: x[1], reverse = True)
    last_max_ind = 1
    maximum = sorted_cookie_list[0][1]
    while last_max_ind < len(sorted_cookie_list) and sorted_cookie_list[last_max_ind][1] == maximum:
        last_max_ind += 1
    for i in range(last_max_ind):
        print(sorted_cookie_list[i][0])

#error checking function for the date input, to make sure its valid
def check_valid_date(date_str):
    if len(date_str) != 10:
        raise Exception('Date should be 10 characters')
    index_of_first_dash = date_str.find('-')
    if index_of_first_dash == -1:
        raise Exception('Date should have 2 dashes separating the year, month, and day values, has 0')
    year = date_str[:index_of_first_dash]
    if len(year) != 4:
        raise Exception('Year should be of length 4')
    try:
        int(year)
    except:
        raise Exception('Year must be an integer')
    substring_after_first_dash = date_str[index_of_first_dash + 1:]
    index_of_second_dash = substring_after_first_dash.find('-')
    if index_of_second_dash == -1:
        raise Exception('Date should have 2 dashes separating the year, month, and day values, has 1')
    month = substring_after_first_dash[:index_of_second_dash]
    if len(month) != 2:
        raise Exception('Month should be of length 2')
    try:
        month_int = int(month)
    except:
        raise Exception('Month must be an integer')
    if month_int < 1 or month_int > 12:
        raise Exception('Month must be between 1 and 12')
    day = substring_after_first_dash[index_of_second_dash + 1:]
    if len(day) != 2:
        raise Exception('Day should be of length 2')
    try:
        day_int = int(day)
    except:
        raise Exception('Day must be an integer')
    if day_int < 1 or day_int > 12:
        raise Exception('Day must be between 1 and 31')

if __name__ == "__main__":
    arg_list = []
    for arg in sys.argv:
        arg_list.append(arg)
    if len(arg_list) < 4:
        raise Exception('There should be 4 arguments, the python file, the cookie log file, -d, and the date in UTC form. There are instead ' + len(arg_list) + ' arguments.')
    filename = arg_list[1]
    try:
        file = open(filename,'r')
    except:
        raise Exception(filename + ' path cant be found')
    dash_d = arg_list[2]
    if dash_d != '-d':
        raise Exception('Third argument should be -d')
    date = arg_list[3]
    check_valid_date(date)
    find_most_active_cookie(file,date)
    file.close()
