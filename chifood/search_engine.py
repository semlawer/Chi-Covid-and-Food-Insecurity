'''
search engine


Input format:
input = {zip_code: [zips], %var1:[direction cutoff], %var2:[dir cutoff] }
'''

from math import radians, cos, sin, asin, sqrt, ceil
import sqlite3
import os
import re

# UPDATE
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'search_engine.sqlite3')

connection = sqlite3.connect("search_engine.sqlite3")
c = connection.cursor()

# UPDATE
def args_needed(args):
    '''
    This takes the dictionary given and creates a matching dictionary
        that fills the values with "?". 
    Input: args - dictionary of arguments
    Output: args_replacement - dictionary of keys mapped to "?"
    '''
    args_replacement = {}
    for key, val in args.items():
        if key not in ("zip_code"):
            dir, cutoff = val
            args_replacement[key] = " ?"
        where_operator[key] = dir
        else:
                args_replacement[key] = ", ".join("?" * len(val))
                args_replacement[key] += ") "
    return args_replacement


# UPDATE
def select_conditions():
    '''
    This function explains which variables are in final product
    Input: 
    Output: selected_var_list - string of variables to be included in table
    '''
    selected_var_list = """acs.zip_code, acs.total_population, acs.unemployed
        acs.black, acs.perc_poverty, covid.cases, covid.deaths, food.ratio"""
  
    return selected_var_list


# UPDATE
def where_conditions(args, where_args):
    '''
    This function returns the "where" section of the SQL query and the
        parameterized argument list needed to fill the "?" in the query
    Inputs:
        args: dict of entered arguments
        where_args: dict of the arguments that will be included in the Where
            statement
    Outputs:
        args_value: list of parameterized variable values
            used this to help:
            https://stackoverflow.com/questions/2158395/flatten-an-irregular-list-of-lists
        where_var_string: string of the where statement
    '''
    where_operator = {"zip_code": "="}
    where_vars = { k: where_operators[k] +  where_args[k] for k in where_args }


    flatten = lambda *n: (e for a in n for e in (flatten(*a) if isinstance(a, \
        (tuple, list)) else (a,)))
    args_values = list(flatten(values))
    where_var_string = ' AND '.join("{}{}".format(key,val) for (key,val) in where_vars.items())
    if where_var_string != "":
        where_var_string = "WHERE " + where_var_string

    return args_values, where_var_string

# UPDATE - don't think I'll need
def terms_method(args):
    '''
    This creates the nested part of the query to search for courses with
        all the terms in the given dictionary, rather than at least one
    Input: args - dict of given arguments
    Output: terms_output - string of the nested part of this query
    '''
    if "terms" not in args:
        return ""
    length = len(args["terms"])
    terms = ", ".join("?" * length)
    terms_output = '''SELECT course_id, COUNT(*) as cnt FROM catalog_index \
        WHERE word in ({}) GROUP BY course_id HAVING cnt={}'''.format(terms, str(length))
    return terms_output


# UPDATE - switch to calculate regression
def walking_time():
    '''
    For a given building code, builds a nested query calculating the distance
        (using the compute_time_between function) between that and other buildings
    Input: building_code - string
    Output: dist - string of nested query
    '''
    connection.create_function("distance", 4, compute_time_between)
    dist = '''
       SELECT a.building_code, distance(a.lon,a.lat,b.lon,b.lat) as walking_time
       FROM gps as a JOIN (SELECT lon, lat, building_code FROM gps 
       WHERE building_code = ?) as b
       '''
    return dist


# UPDATE
def merge_conditions(selected_vars, terms_output, dist):
    '''
    This function combines the necessary SQL joins together as strings
        depending on the variables needed. Uses the 2 nested queries
    Inputs:
        selected_vars: integer showing test type
        terms_output: string of nested query for terms
        dist: string of nested query for distance from given building
    Output: merges - string of all merges necessary for the given test
    '''
    merges = ""
    merges += "LEFT JOIN covid ON acs.zipcode = covid.zipcode
    return merges

# STAYS THE SAME
def final_list(select_string, merge_string, where_string, arg_list):
    '''
    Combines all string elements of the SQL query together and executes
    Inputs:
        select_string - string of all selected variables to include in table
        merge_string - string of all joins needed to create table
        where_string - string of all the Where statements needed to specify table
        arg_list - list of variable values to fill the parameterized inputs with
    Output: output_sql - SQL table
    '''
    output = ''' SELECT {} FROM courses {}
        {} '''.format(select_string, merge_string, where_string)
    output_sql = c.execute(output, arg_list).fetchall()
    return output_sql


#SHOULD PRETTY MUCH BE CORRECT
def find_courses(args):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept a string
      - day is list of strings
           -> ["'MWF'", "'TR'", etc.]
      - time_start is an integer in the range 0-2359
      - time_end is an integer an integer in the range 0-2359
      - enrollment is a pair of integers
      - walking_time is an integer
      - building_code ia string
      - terms is a list of strings string: ["quantum", "plato"]

    Returns a pair: an ordered list of attribute names and a list the
     containing query results.  Returns ([], []) when the dictionary
     is empty.
    '''
    assert_valid_input(args)
    if args == {}:
        return ([], [])
    dist = ""
    question_args = args_needed(args)
    selected_vars = select_attr(args.keys())
    select_string = select_conditions(selected_vars)
    args_values, where_string = where_conditions(args, question_args)
    terms_output = terms_method(args)
    #dist = walking_time()
    merge_string = merge_conditions(selected_vars, terms_output, dist)
    final_courses =  final_list(select_string, merge_string, where_string, args_values)
    header = get_header(c)
    return (header, final_courses)