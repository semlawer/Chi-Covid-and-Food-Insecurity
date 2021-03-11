import json
import traceback
import sys
import csv
import os

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms

from obs import find_obs

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
    zipcode='ZIP Code',
    total_pop='Population (Total)',
    perc_black='Population (% Black)',
    perc_hisp='Population (% Hispanic)',
    perc_unempl='Population (% Unemployed)',
    median_income='Median Income',
    perc_poverty='Population (% Poverty)',
    fs_ratio='Food Swamp Ratio',
    pr_food_ins='Predicted Food Insecurity',
    death_rate_cumulative="COVID-19 Death Rate"
)


def _valid_result(res):
    """Validate results returned by find_obs"""
    (HEADER, RESULTS) = [0, 1]
    ok = (isinstance(res, (tuple, list)) and
          len(res) == 2 and
          isinstance(res[HEADER], (tuple, list)) and
          isinstance(res[RESULTS], (tuple, list)))
    if not ok:
        return False

    n = len(res[HEADER])

    def _valid_row(row):
        return isinstance(row, (tuple, list)) and len(row) == n
    return reduce(and_, (_valid_row(x) for x in res[RESULTS]), True)


def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)


def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]


ZIPS = _build_dropdown([None] + _load_res_column('zipcode_list.csv'))


class IntegerRange(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (forms.IntegerField(),
                  forms.IntegerField())
        super(IntegerRange, self).__init__(fields=fields,
                                           *args, **kwargs)

    def compress(self, data_list):
        if data_list and (data_list[0] is None or data_list[1] is None):
            raise forms.ValidationError('Must specify both lower and upper '
                                        'bound, or leave both blank.')

        return data_list


class Range(IntegerRange):
    def compress(self, data_list):
        super(Range, self).compress(data_list)
        for v in data_list:
            if not 0.0 <= v <= 1000:
                raise forms.ValidationError(
                    'Number bounds must be in the range 0 to 1000.')
        if data_list and (data_list[1] < data_list[0]):
            raise forms.ValidationError(
                'Lower bound must not exceed upper bound.')
        return data_list

RANGE_WIDGET = forms.widgets.MultiWidget(widgets=(forms.widgets.NumberInput,
                                                  forms.widgets.NumberInput))

class SearchForm(forms.Form):
    zipcode = forms.MultipleChoiceField(label='ZIP Code(s)',
                                        choices=ZIPS,
                                        required=False)
    death_rate_cumulative = Range(
        label='COVID-19 Death Rates (lower/upper)',
        help_text='between 0.0 and 308.5',
        widget=RANGE_WIDGET,
        required=False)
    fs_ratio = Range(
        label='Food Swamp Ratio (lower/upper)',
        help_text='between 0.0 and 61.0',
        widget=RANGE_WIDGET,
        required=False)
    show_args = forms.BooleanField(label='Show args_to_ui',
                                   required=False)


def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():

            # Convert form data to an args dictionary for find_obs
            args = {}
            if form.cleaned_data['zipcode'] and form.cleaned_data['zipcode'] != ['']:
                args['zipcode'] = form.cleaned_data['zipcode']
            if form.cleaned_data['death_rate_cumulative']:
                args['death_rate_cumulative'] = form.cleaned_data['death_rate_cumulative']
            if form.cleaned_data['fs_ratio']:
                args['fs_ratio'] = form.cleaned_data['fs_ratio']
            if form.cleaned_data['show_args']:
                context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

            try:
                res = find_obs(args)
            except Exception as e:
                print('Exception caught')
                bt = traceback.format_exception(*sys.exc_info()[:3])
                context['err'] = """
                An exception was thrown in find_obs:
                <pre>{}
{}</pre>
                """.format(e, '\n'.join(bt))

                res = None
    else:
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
    elif not _valid_result(res):
        context['result'] = None
        context['err'] = ('Return of find_obs has the wrong data type. '
                          'Should be a tuple of length 4 with one string and '
                          'three lists.')
    else:
        columns, result = res

        # Wrap in tuple if result is not already
        if result and isinstance(result[0], str):
            result = [(r,) for r in result]

        context['result'] = result
        context['num_results'] = len(result)
        context['columns'] = [COLUMN_NAMES.get(col, col) for col in columns]

    context['form'] = form
    return render(request, 'index.html', context)
