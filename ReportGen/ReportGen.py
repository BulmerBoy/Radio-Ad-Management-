from datetime import datetime
from datetime import date
import math
import os
"""
used_ad_space is the list that that manages how much
ad space has been used for each of the days in a given
week. It will be compared to the TOTAL_AD_SPACE
at the end of the program, to calculate how
much space is available.

For all lists, the semantic order for which number represents
which day is the same.
[MON, TUE, WED, THU, FRI, SAT, SUN]
"""
used_cita_space = [0, 0, 0, 0, 0, 0, 0]
TOTAL_CITA_SPACE = (72, 72, 72, 72, 72, 65, 45)
used_ciog_space = [0, 0, 0, 0, 0, 0, 0]
TOTAL_CIOG_SPACE = (66, 66, 66, 66, 66, 50, 40)
used_cjlu_space = [0, 0, 0, 0, 0, 0, 0]
TOTAL_CJLU_SPACE = (78, 78, 78, 78, 78, 60, 65)
today = datetime.today().strftime('%Y-%m-%d')
filename = 'Report - ' + str(today)

"""
the print_data method splices the necessary information for given contracts and writes them into
the report file in a presentable format. It also calls the station_writer method to aid in this, 
which in turn does important list calculations with the passed info.
"""
def print_data(current_data, today, Report_List):
    data = [p.strip() for p in current_data.split("|")]
    adrunlist = list(data[3])
    contract_length = days_between(data[1], data[2])
    remaining_length = days_between(today, data[2])
    contract_length_weeks = math.floor(contract_length / 7)
    contract_length_days = contract_length % 7
    remaining_weeks = math.floor(remaining_length / 7)
    remaining_days = remaining_length % 7
    future_date = days_between(today, data[1])
    future_date_weeks = math.floor(future_date / 7)
    future_date_days = future_date % 7
    #Does past date info even matter?
    past_date = days_between(today, data[2])
    #past_date_weeks = math.floor(future_date / 7)
    #past_date_days = future_date % 7
    # First check if the current date is before
    # the contract start date.
    if future_date > 0:
        print('\n--------------------')
        print('Sponsor Name: ' + data[0])
        print('this contract has not started yet.\n'
        '(starts in ' + str(future_date_weeks) + ' weeks and ' + str(future_date_days) + ' days).')
        print('--------------------')
    # Then check if the current date is after
    # the contract end date.    
    elif past_date < 0:
        print('\n--------------------')
        print('Sponsor Name: ' + data[0])
        print('This contract expired.')
        # print('this contract expired.\n'
        # '(ended ' + str(abs(past_date_weeks)) + ' weeks and ' + str(past_date_days) + ' days ago).')
        print('--------------------')
    # Current date is within the contract
    # period, therefore record its info.
    else:
        with open(Report_List, "a") as f: 
            f.write('\n--------------------\n')
            f.write('Sponsor Name: ' + data[0] + '\n')
            f.write('Contract Start/End Date: ' + data[1] + ' / ' + data[2] + '\n')
            f.write('Contract length: ' + str(contract_length_weeks) +' weeks and ' + str(contract_length_days) + ' days.\n')
            if remaining_days == 0 and remaining_weeks == 0:
                f.write('Remaining: Contract ends today.\n')
            else:    
                f.write('Remaining: ' + str(remaining_weeks) +' weeks and ' + str(remaining_days) + ' days.\n')
            f.write('Ad space requested:\n'
                '(Mon: ' + adrunlist[0] + ') '
                '(Tue: ' + adrunlist[1] + ') '
                '(Wed: ' + adrunlist[2] + ') '
                '(Thu: ' + adrunlist[3] + ') '
                '(Fri: ' + adrunlist[4] + ') '
                '(Sat: ' + adrunlist[5] + ') '
                '(Sun: ' + adrunlist[6] + ')\n')
        if (remaining_weeks == 0):   
            station_writer(data[4], adrunlist, remaining_days)  
        else:
            station_writer(data[4], adrunlist, 7)

"""
station_writer is the method that finds out which stations the given contract is playing
on. Based on that information, it'll print the correct stations, and also add the adrunlist of 
times the given contract plays on the station into the corresponding station list.
"""
def station_writer(station, adrunlist, day_count):
    if(day_count == 7):
        days = day_count
    else:
        days = day_count + 1    
    day_value = date.today().weekday()
    data = [p.strip() for p in station.split("&")]
    cita_flag = False
    ciog_flag = False
    cjlu_flag = False
    all_flag = False
    for x in data:
        match x:
            case "ALL":
                all_flag = True
                break
            case "CITA":
                cita_flag = True
            case "CIOG":
                ciog_flag = True
            case "CJLU":
                cjlu_flag = True
            case _:
                pass  
    with open(Report_List, "a") as f:
        counter = day_value 
        if all_flag or (cita_flag and ciog_flag and cjlu_flag):
            f.write('Airing on all stations.\n') 
            for x in range(days):
                used_cita_space[counter] = used_cita_space[counter] + int(adrunlist[counter])
                used_ciog_space[counter] = used_ciog_space[counter] + int(adrunlist[counter])
                used_cjlu_space[counter] = used_cjlu_space[counter] + int(adrunlist[counter])
                counter += 1
                counter = counter % 7
        else:        
            if cita_flag:
                f.write('Airing in CITA.\n')
                counter = day_value 
                for x in range(days):
                    used_cita_space[counter] = used_cita_space[counter] + int(adrunlist[counter])
                    counter += 1
                    counter = counter % 7
            if ciog_flag:
                f.write('Airing in CIOG.\n')
                counter = day_value 
                for x in range(days):
                    used_ciog_space[counter] = used_ciog_space[counter] + int(adrunlist[counter])
                    counter += 1
                    counter = counter % 7
            if cjlu_flag:
                f.write('Airing in CJLU.\n')
                counter = day_value 
                for x in range(days):
                    used_cjlu_space[counter] = used_cjlu_space[counter] + int(adrunlist[counter])
                    counter += 1
                    counter = counter % 7
        f.write('--------------------\n')
"""
ad_space_test is the method that calculates the 
available ad space for each station based on what
is currently being used by the existing contracts.
"""
def ad_space_test(Report_List):
    avail_ad_space = [0,0,0,0,0,0,0]
    with open(Report_List, "a") as f:
        f.write('\n********************\n')
        f.write('NOW CALCULATING AD SPACE...\n')
        for x in range(7):
            avail_ad_space[x] = TOTAL_CITA_SPACE[x] - used_cita_space[x]
        f.write('Total CITA space: ' + str(TOTAL_CITA_SPACE) + '\n')
        f.write('Used CITA space: ' + str(used_cita_space) + '\n')
        f.write('Available CITA space: ' + str(avail_ad_space) + '\n\n') 
        avail_ad_space = [0,0,0,0,0,0,0]
        for x in range(7):
            avail_ad_space[x] = TOTAL_CIOG_SPACE[x] - used_ciog_space[x]
        f.write('Total CIOG space: ' + str(TOTAL_CIOG_SPACE) + '\n')
        f.write('Used CIOG space: ' + str(used_ciog_space) + '\n')
        f.write('Available CIOG space: ' + str(avail_ad_space) + '\n\n') 
        avail_ad_space = [0,0,0,0,0,0,0]
        for x in range(7):
            avail_ad_space[x] = TOTAL_CJLU_SPACE[x] - used_cjlu_space[x]
        f.write('Total CJLU space: ' + str(TOTAL_CJLU_SPACE) + '\n')
        f.write('Used CJLU space: ' + str(used_cjlu_space) + '\n')
        f.write('Available CJLU space: ' + str(avail_ad_space) + '\n') 
        avail_ad_space = [0,0,0,0,0,0,0]
        f.write('********************\n')  



# the second parameter should always be the later date / end date.
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return (d2 - d1).days
            

# ----------MAIN PROGRAM----------
print(os.getcwd())
script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
Master_List = os.path.join(script_dir, "Master_List.txt")
Report_List = os.path.join(script_dir, filename)
Record_List = os.path.join(script_dir, "Record.txt")
with open(Report_List, 'w') as f:
    f.write('Welcome to the ad island information report.\n'
            'This report was created on ' + datetime.now().strftime('%A') + ', ' + str(today) + '.\n'
            'Now showing current commercials and ads playing...\n')
with open(Master_List, 'r') as f: 
    print('Welcome to the ad island information system.\nToday\'s date is ' + str(today) + '.\n')
    current_data = f.readline()
    for current_data in f:
        if current_data[0] == '#':
            pass
        else:
            print_data(current_data, today, Report_List)
    ad_space_test(Report_List)  
with open(Record_List, 'a') as f:
    f.write('A report for ' + str(today) + ' has been created.\n')     
#test comment.