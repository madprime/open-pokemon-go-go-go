import csv
import os

INITIAL_SURVEY_FILEPATH = os.path.join('raw_data',
                                       'Open Pokemon GO GO GO!.csv')
WEEKLY_SURVEY_PLAYERS = os.path.join('scratch', 'weekly_survey_players.txt')
WEEKLY_SURVEY_NONPLAYERS = os.path.join('scratch', 'weekly_survey_nonplayers.txt')
GRANULAR_DATA_MEMBERS = os.path.join('scratch', 'granular_data_list.txt')
DAILY_DATA_MEMBERS = os.path.join('scratch', 'daily_data_list.txt')


def get_user_info(initial_survey_filepath):
    """
    Parse surveys to get user info for managing data and communications.
    """
    user_info = {}
    # Get initial survey data header.
    with open(initial_survey_filepath) as inputfile:
        csv_in = csv.DictReader(inputfile)
        for row_data in csv_in:
            member_id = row_data['Open Humans Project Member ID']
            weekly_surveys = (row_data[
                'Want to contribute to short weekly surveys in the future?']
                == 'Yes')
            granular_data = (row_data[
                'What level of activity data do you want to share?'] ==
                'Minute-to-minute activity data (if available)')
            is_player = (row_data['Did you install and play Pokemon GO?'] ==
                         'Yes')
            user_info[member_id] = {
                'weekly_surveys': weekly_surveys,
                'granular_data': granular_data,
                'is_player': is_player,
            }

    # TODO: When we have weekly survey data, parse it here to update
    # 'weekly_surveys' and 'is_player' fields.

    return user_info


def create_weekly_survey_lists(user_data):
    """
    Use the user data to create lists of IDs to send weekly survey invites.

    Weekly surveys were conceived as only being relevant to players, but
    some non-player "controls" indicated "yes". As a result, there are two
    surveys and two lists created.

    For players: The weekly survey repeats some stats and usage questions
    to capture information about the past week.

    For non-players: Because they may have installed the game, their survey
    checks if this has occurred. If so, they can answer a copy of the
    "initial survey" questions regarding Pokemon GO usage.
    """
    with open(WEEKLY_SURVEY_PLAYERS, 'w') as weekly_file:
        for user_id in user_data:
            if (user_data[user_id]['weekly_surveys'] and
                    user_data[user_id]['is_player']):
                weekly_file.write('{}\n'.format(user_id))

    with open(WEEKLY_SURVEY_NONPLAYERS, 'w') as weekly_file:
        for user_id in user_data:
            if (user_data[user_id]['weekly_surveys'] and
                    not user_data[user_id]['is_player']):
                weekly_file.write('{}\n'.format(user_id))


if __name__ == "__main__":
    user_data = get_user_info(initial_survey_filepath=INITIAL_SURVEY_FILEPATH)

    # Lists needed to manage sending surveys.
    create_weekly_survey_lists(user_data)

    # Lists needed to manage data processing.
    with open(GRANULAR_DATA_MEMBERS, 'w') as granular_file:
        for user_id in user_data:
            if user_data[user_id]['granular_data']:
                granular_file.write('{}\n'.format(user_id))
    with open(DAILY_DATA_MEMBERS, 'w') as daily_file:
        for user_id in user_data:
            if not user_data[user_id]['granular_data']:
                daily_file.write('{}\n'.format(user_id))

    import json
    json.dumps(user_data, indent=2)
