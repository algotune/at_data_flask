"""Main module.
"""
from flask import Flask, jsonify, request
import logging
import pandas as pd
from at_data_flask.db_operations import db_get_fund_by_id, db_get_fund_nav_ts_by_id, db_get_fund_list
from flask_cors import cross_origin, CORS

app = Flask(__name__)
CORS(app)


@app.route('/fund/<fund_type>/<fund_id>', methods=['GET'])
def get_fund_by_id(fund_type: str, fund_id: str):
    logger = logging.getLogger(__name__)
    result_dict = {}
    try:
        result = db_get_fund_by_id(fund_type, fund_id)
        result = result.where(pd.notnull(result), None)
        if len(result) == 1:
            result_dict = result.iloc[0, :].to_dict()
    except Exception as e:
        logger.error(e)

    return jsonify(result_dict)


@app.route('/fund/ts/<fund_type>/<fund_id>', methods=['GET'])
def get_fund_nav_ts_by_id(fund_type: str, fund_id: str):
    ts_df = db_get_fund_nav_ts_by_id(fund_type, fund_id)
    ts_df = ts_df.where(pd.notnull(ts_df), None)

    # only return aum/return/date to reduce size of the json
    result_list = [x[1].to_dict() for x in ts_df[['aum', 'return', 'date']].iterrows()]

    return jsonify(result_list)


@app.route('/funds/<fund_type>')
def get_funds(fund_type: str):
    page_num = request.args.get('pageNumber', 0, int)
    page_size = request.args.get('pageSize', 100, int)

    sort_by = request.args.get('sortBy', 'inception_date')
    sort_order = request.args.get('sortOrder', 'asc')
    active_only = request.args.get('activeOnly', True, bool)

    filter_str = request.args.get('filterStr', None, str)
    if filter_str == 'null':
        filter_str = None

    result_df = db_get_fund_list(fund_type=fund_type,
                                 order_by=sort_by,
                                 order_type=sort_order,
                                 page_number=page_num,
                                 page_size=page_size,
                                 active_only=active_only,
                                 filter_str=filter_str)
    result_df = result_df.where(pd.notnull(result_df), None)
    result_list = [x[1].to_dict() for x in result_df.iterrows()]
    return jsonify(result_list)


# driver function
if __name__ == '__main__':
    app.run(debug=True)
