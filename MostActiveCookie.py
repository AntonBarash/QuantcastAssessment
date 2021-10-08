from Cookie_Class import Cookie

def convert_date_string_to_int(date_str):
    if len(date_str) != 10:
        raise Exception('Date should be 10 characters')
    index_of_first_dash = date_str.find('-')
    if index_of_first_dash == -1:
        raise Exception('Date should have 2 dashes separating the year, month, and day values, has 0')
    substring_after_first_dash = date_str[index_of_first_dash + 1:]
    index_of_second_dash = substring_after_first_dash.find('-')
    if index_of_second_dash == -1:
        raise Exception('Date should have 2 dashes separating the year, month, and day values, has 1')
    return int(date_str.replace('-',''))


def analyze_line(cookie_str):
    index_of_comma = cookie_str.index(',') #finds index of comma in cookie string
    cookie = cookie_str[:index_of_comma]
    index_of_T = cookie_str[index_of_comma:].index(',') #finds index of T which starts time in cookie string
    time = cookie_str[index_of_T + 1:]
    date_string = cookie_str[index_of_comma + 1:index_of_comma + 11] #finds substring of 10 charactesr after comma, which is date
    return cookie,date_string,time


#binary search function to find a cookie with input date
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
            start = current_index - 1
    return -1

def find_cookie_dict_of_day(filename, input_date):
    list_of_cookies = create_cookie_list(filename)
    cookie_index = find_cookie_given_date(list_of_cookies,input_date)
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

def create_cookie_list(filename):
    file = open(filename,'r')
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

def find_most_active_cookie(filename, input_date):
    cookie_dict = find_cookie_dict_of_day(filename, input_date)
    sorted_cookie_list = sorted(cookie_dict.items(), key = lambda x: x[1], reverse = True)
    last_max_ind = 1
    maximum = sorted_cookie_list[0][1]
    while last_max_ind < len(sorted_cookie_list) and sorted_cookie_list[last_max_ind][1] == maximum:
        last_max_ind += 1
    for i in range(last_max_ind):
        print(sorted_cookie_list[i][0])

find_most_active_cookie('test.csv','2018-12-08')
