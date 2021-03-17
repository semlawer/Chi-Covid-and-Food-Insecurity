'''
Data search engine
'''

import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'chifood.sqlite3')
SELECT_CLAUSE = '''SELECT data.zipcode, data.death_rate_cumulative,
                   data.fs_ratio, data.pr_fs_ratio, data.total_population,
                   data.perc_black, data.perc_hispanic, data.perc_minority, 
                   data.perc_unemployed, data.median_income, data.perc_poverty'''
FROM_CLAUSE = '''FROM data'''


def build_where(args_from_ui):
    '''
    Builds WHERE clause of SQL query
    '''

    conds = []
    args = []

    for col, values in args_from_ui.items():
        args.extend(values)
        if col == 'zipcode':
            q_marks = ', '.join(['?']*len(values))
            conds.extend(['data.zipcode IN (' + q_marks + ')'])
        else:
            conds.extend(['data.'+ col + ' BETWEEN ? AND ?'])

    where_clause = 'WHERE ' + ' AND '.join(conds)

    return where_clause, args


def build_query(args_from_ui):
    '''
    Builds SQL query
    '''

    where_clause, arguments = build_where(args_from_ui)
    query = ' '.join([SELECT_CLAUSE, FROM_CLAUSE, where_clause])

    return query, arguments


def find_obs(args_from_ui):
    '''
    Returns tuple with a list of column headers
    and a list of observations
    '''

    assert_valid_input(args_from_ui)
    if not args_from_ui:
        return ([], [])

    connection = sqlite3.connect("CS_covid_food/chifood.sqlite3")
    cursor = connection.cursor()

    query, arguments = build_query(args_from_ui)
    table = cursor.execute(query, arguments).fetchall()
    col_header = get_header(cursor)
    connection.close()

    return (col_header, table)


def assert_valid_input(args_from_ui):
    '''
    Verify that the input conforms to the standards set in the
    assignment.
    '''

    assert isinstance(args_from_ui, dict)

    acceptable_keys = set(['zipcode', 'death_rate_cumulative', 'fs_ratio'])
    assert set(args_from_ui.keys()).issubset(acceptable_keys)

    # zipcode is a list of strings, if it exists
    assert isinstance(args_from_ui.get("zipcode", []), (list, tuple))
    assert all([isinstance(s, str) for s in args_from_ui.get("zipcode", [])])

    # death_rate_cumulative is a pair of floats, if it exists
    death_rate_val = args_from_ui.get("death_rate_cumulative", [0, 0])
    assert isinstance(death_rate_val, (list, tuple))
    assert len(death_rate_val) == 2
    assert all([isinstance(i, float) or isinstance(i, int) for i in death_rate_val])
    assert death_rate_val[0] <= death_rate_val[1]


def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    header = []

    for i in cursor.description:
        s = i[0]
        if "." in s:
            s = s[s.find(".")+1:]
        header.append(s)

    return header


