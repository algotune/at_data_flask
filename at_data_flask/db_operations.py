from at_util.util_mysql import get_session_from_env, db_select
import pandas as pd

VALID_FUND_TYPE_TABLE = {
    'hedge': 'ghf',
    'fof': 'fof',
    'pe': 'gpe'
}

db_session = get_session_from_env(
    env_host='FUND_HOST',
    env_user='FUND_USER',
    env_pass='FUND_PASS',
    env_db_name='FUND_DB'
)


def db_get_fund_list(fund_type,
                     order_by='inception_date',
                     order_type='asc',
                     page_number=0,
                     page_size=100,
                     active_only=True):
    """

    :param fund_type:
    :param order_by:
    :param order_type:
    :param page_number:
    :param page_size:
    :param active_only:
    :return:
    usage:
    >>> db_get_fund_list('hedge', page_number=1)
    """
    assert fund_type in VALID_FUND_TYPE_TABLE.keys(), 'fund_type [{}] not supported'.format(fund_type)
    table_name = VALID_FUND_TYPE_TABLE[fund_type]
    if active_only:
        sql = 'select * from eureka.{}_funddetails where dead = \'No\' ' \
              'order by {} {} limit {} offset {}'.format(table_name, order_by, order_type,
                                                         page_size, page_number * page_size)
    else:
        sql = 'select * from eureka.{}_funddetails ' \
              'order by {} {} limit {} offset {}'.format(table_name, order_by, order_type,
                                                         page_size, page_number * page_size)
    result = db_select(db_session, sql)
    return result


def db_get_fund_by_id(fund_type: str, fund_id: str) -> pd.DataFrame:
    """

    :param fund_id:
    :param fund_type:
    :return:
    usage:
    >>> fund_id = '5000'
    >>> fund_type = 'hedge'
    >>> db_get_fund_by_id(fund_id, fund_type)
    """
    assert fund_type in VALID_FUND_TYPE_TABLE.keys(), 'fund_type [{}] not supported'.format(fund_type)
    table_name = VALID_FUND_TYPE_TABLE[fund_type]
    sql = 'select * from eureka.{}_funddetails where fund_id = {}'.format(table_name, fund_id)
    result = db_select(db_session, sql)

    return result


def db_get_fund_nav_ts_by_id(fund_type: str, fund_id: str, date_index=False):
    """

    :param date_index:
    :param fund_type:
    :param fund_id:
    :return:
    usage:
    >>> fund_type = 'hedge'
    >>> fund_id = '32431'
    >>> date_index = True
    >>> db_get_fund_nav_ts_by_id('hedge', '29474', date_index=True)
    """
    assert fund_type in VALID_FUND_TYPE_TABLE.keys(), 'fund_type [{}] not supported'.format(fund_type)
    table_name = VALID_FUND_TYPE_TABLE[fund_type]
    sql = 'select * from eureka.{}_navdetails where fund_id = {}'.format(table_name, fund_id)
    result = db_select(db_session, sql)
    # if return is null, do not return data
    result = result[~result['return'].isnull()].sort_values('date')
    if date_index:
        result['date'] = pd.to_datetime(result['date'])
        result = result.set_index('date')
    else:
        # convert date to %Y%m%d
        result['date'] = pd.to_datetime(result['date']).dt.strftime('%Y%m%d')

    return result
