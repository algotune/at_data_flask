from at_data_flask.db_operations import db_get_fund_nav_ts_by_id
import matplotlib.pyplot as plt


def plot_fund(fund_type, fund_id):
    """

    :param fund_type:
    :param fund_id:
    usage:
    >>> fund_type = 'hedge'
    >>> fund_id = '9650'
    """
    fund_df = db_get_fund_nav_ts_by_id(fund_type, fund_id, date_index=True)
    fund_df['cum_return'] = fund_df['return'].cumsum()
    fund_name = fund_df['fund_name'].values[0]
    fund_df[['cum_return', 'aum']].plot(subplots=True, title=fund_name)
