from flask import Blueprint, request
from flask.json import jsonify
import pandas as pd
import SQL

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

#######################
# Dashboard Endpoints #
#######################


@dashboard.route('/site/dashboard/gettotaltrackedplayers', methods=['GET'])
def get_total_tracked_players():
    num_of_players = SQL.get_number_tracked_players()
    return_dict = {
        "players": num_of_players[0]
    }

    return jsonify(return_dict)


@dashboard.route('/site/dashboard/getreportsstats', methods=['GET'])
def get_total_reports():
    report_stats = SQL.get_report_stats()[0]

    return_dict = {
        "bans": int(report_stats[0]),
        "false_reports": int(report_stats[1]),
        "total_reports": int(report_stats[2]),
        "accuracy": float(report_stats[3])
    }

    return jsonify(return_dict)

@dashboard.route('/site/dashboard/getregionstats', methods=['GET'])
def get_region_reports():
    region_stats = SQL.get_region_report_stats()

    print(region_stats)
    print(type(region_stats))

    return jsonify({'success': 'good job'})

@dashboard.route('/labels/get_player_labels', methods=['GET'])
def get_player_labels():
    labels = SQL.get_player_labels()

    df = pd.DataFrame(labels)
    output = df.to_dict('records')

    return jsonify(output)

@dashboard.route('/leaderboard', methods=['GET'])
def leaderboard(board=None):
    params = request.args.to_dict()

    # Any query param will be treated as True
    params = dict.fromkeys(params, True)

    board_data = SQL.get_leaderboard_stats(**params)

    df = pd.DataFrame(board_data)

	# Post processing: rename, group by reporter and count, sort, and limit results
    df = df.rename(columns={"reported": "count"}).groupby(['reporter']).count().reset_index().sort_values(by='count', ascending=False).head(25)

    output = df.to_dict('records')

    return jsonify(output)


# CORS Policy: Allow Access to These Methods From Any Origin
@dashboard.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
