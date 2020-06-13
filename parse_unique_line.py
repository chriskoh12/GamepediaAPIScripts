# Helper function to parse gamepedia's uniqueLine to extract the week and day of the game
# The way the uniqueLine is structured, the week will always be to the left of the first underscore,
# and the game # will always be to the right, so look at what characters are there and
# the week num and the day num can be determined from those
# args:
# unique_line - the uniqueLine to parse
#
# returns two variables: the week and the day (both as ints)
# example of week 1 UniqueLine: 'LCS/2019 Season/Spring Season/Scoreboards_7_1_2_2'
# example of non-week 1 UniqueLine: 'LCS/2019 Season/Spring Season/Scoreboards/Week 2_9_1_1_2'


def parse_unique_line(unique_line):
    week_ = unique_line.find('_') - 1  # find index of either the weeknum or a letter, which means the weeknum is 1
    week_ = unique_line[week_]
    game_num = unique_line.find('_') + 1  # find index of game num, which can be used to find the day num
    game_num = unique_line[game_num]
    week_num = int(week_) if week_.isdigit() else 1  # If it's a digit, it's the week num, if it's not, it's from week 1
    day_num = 1 if int(game_num) <= 5 else 2  # If game num is less than or equal to 5, it's game 1-5 which is first day, if > 5 then day 2
    return week_num, day_num
