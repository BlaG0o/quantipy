import unittest
import os.path
import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal
import test_helper
import copy

from operator import lt, le, eq, ne, ge, gt

from pandas.core.index import Index
__index_symbol__ = {
    Index.union: ',',
    Index.intersection: '&',
    Index.difference: '~',
    Index.sym_diff: '^'
}

from collections import defaultdict, OrderedDict
from quantipy.core.stack import Stack
from quantipy.core.chain import Chain
from quantipy.core.link import Link
from quantipy.core.cluster import Cluster
from quantipy.core.view_generators.view_mapper import ViewMapper
from quantipy.core.view_generators.view_maps import QuantipyViews
from quantipy.core.view import View
from quantipy.core.helpers import functions
from quantipy.core.helpers.functions import load_json
from quantipy.core.tools.dp.prep import (
    frange,
    frequency,
    crosstab
)
from quantipy.core.tools.dp.query import request_views
from quantipy.core.tools.view.query import get_dataframe

class TestBankedChains(unittest.TestCase):

    def setUp(self):
        self.path = './tests/'
#         self.path = ''
        project_name = 'Example Data (A)'

        # Load Example Data (A) data and meta into self
        name_data = '%s.csv' % (project_name)
        path_data = '%s%s' % (self.path, name_data)
        self.data = pd.DataFrame.from_csv(path_data)
        
        name_meta = '%s.json' % (project_name)
        path_meta = '%s%s' % (self.path, name_meta)
        self.meta = load_json(path_meta)

        # Variables by type for Example Data A
        self.dk = 'Example Data (A)'
        self.fk = 'no_filter'
        self.single = ['gender', 'locality', 'ethnicity', 'religion', 'q1']
        self.delimited_set = ['q2', 'q3', 'q8', 'q9']
        self.x_vars = ['q5_1', 'q5_2', 'q5_3', 'q5_4', 'q5_5', 'q5_6']
        self.y_vars = ['@', 'gender', 'locality', 'q2', 'q3']        
        self.views = ['cbase', 'counts']
        self.weights = [None, 'weight_a']
        self.text_key = 'en-GB'
        
        self.stack = get_stack(
            self, self.meta, self.data,
            self.x_vars, self.y_vars, 
            self.views, self.weights)
    
#         self.path = ''
                    
    def test_means_summary(self):
   
        ################## Unweighted
        
        views_ref = request_views(
            self.stack, 
            weight=None, 
            nets=False,
            descriptives=['mean', 'stddev', 'median'],
            coltests=False, 
            mimic="askia", 
            sig_levels=['low', 'mid', 'high']
        )
        
        chains = {
            xk: self.stack.get_chain(
                x=xk, y=self.y_vars, 
                views=views_ref['get_chain']['c'])
            for xk in self.x_vars
        }
        
        chain_q5_1 = chains['q5_1']
        chain_q5_2 = chains['q5_2']
        chain_q5_3 = chains['q5_3']
        chain_q5_4 = chains['q5_4']
        chain_q5_5 = chains['q5_5']
        chain_q5_6 = chains['q5_6']
        
        ## Unweighted, mean only        
        spec = {
            'name': 'q5_means',
            'type': 'banked-chain',
            'text': {'en-GB': 'Mean summary q5_1 to q5_6'},
            'bases': True,
            'view': 'x|mean|x:y|||descriptives',
            'items': [
                {'chain': chain_q5_1, 'text': {'en-GB': 'q5_1: Mean'}},
                {'chain': chain_q5_2, 'text': {'en-GB': 'q5_2: Mean'}},
                {'chain': chain_q5_3, 'text': {'en-GB': 'q5_3: Mean'}},
                {'chain': chain_q5_4, 'text': {'en-GB': 'q5_4: Mean'}},
                {'chain': chain_q5_5, 'text': {'en-GB': 'q5_5: Mean'}},
                {'chain': chain_q5_6, 'text': {'en-GB': 'q5_6: Mean'}}
            ]
        }
 
        means_summary_chain = Cluster().bank_chains(
            spec, text_key=self.text_key)
         
#         df = means_summary_chain.concat()
#         df.to_csv('{}{}.csv'.format(self.path, spec['name']))
        
        ## Unweighted, mean + stddev
        mean = 'x|mean|x:y|||descriptives'
        stddev = 'x|stddev|x:y|||descriptives'
        spec = {
            'name': 'q5_means_stddev',
            'type': 'banked-chain',
            'text': {'en-GB': 'Mean/stddev summary q5_1 to q5_6'},
            'bases': True,
            'view': mean,
            'items': [
                {'chain': chain_q5_1, 'text': {'en-GB': 'q5_1: Mean'}},
                {'chain': chain_q5_1, 'view': stddev, 'text': {'en-GB': 'q5_1: Stddev'}},
                {'chain': chain_q5_2, 'text': {'en-GB': 'q5_2: Mean'}},
                {'chain': chain_q5_2, 'view': stddev, 'text': {'en-GB': 'q5_2: Stddev'}},
                {'chain': chain_q5_3, 'text': {'en-GB': 'q5_3: Mean'}},
                {'chain': chain_q5_3, 'view': stddev, 'text': {'en-GB': 'q5_3: Stddev'}},
                {'chain': chain_q5_4, 'text': {'en-GB': 'q5_4: Mean'}},
                {'chain': chain_q5_4, 'view': stddev, 'text': {'en-GB': 'q5_4: Stddev'}},
                {'chain': chain_q5_5, 'text': {'en-GB': 'q5_5: Mean'}},
                {'chain': chain_q5_5, 'view': stddev, 'text': {'en-GB': 'q5_5: Stddev'}},
                {'chain': chain_q5_6, 'text': {'en-GB': 'q5_6: Mean'}},
                {'chain': chain_q5_6, 'view': stddev, 'text': {'en-GB': 'q5_6: Stddev'}},
            ]
        }

        means_stddev_summary_chain = Cluster().bank_chains(
            spec, text_key=self.text_key)
        
#         df = means_stddev_summary_chain.concat()
#         df.to_csv('{}{}.csv'.format(self.path, spec['name']))
        
        
        
#         cluster = Cluster('test')
#         cluster.add_chain([
#             
#         ])
        
# ##################### Helper functions #####################

def index_items(col, values, all=False):
    """
    Return a correctly formed list of tuples to matching an index.
    """
     
    items = [
        (col, str(i))
        for i in values
    ]
     
    if all: items = [(col, 'All')] + items
     
    return items

def str_index_values(index):
    """
    Make sure level 1 of the multiindex are all strings
    """
    values = index.values.tolist()
    values = zip(*[zip(*values)[0], [str(i) for i in zip(*values)[1]]])
    return values
        
def confirm_index_columns(self, df, expected_x, expected_y):
    """
    Confirms index and columns are as expected.
    """    
#     global COUNTER
    
    actual_x = str_index_values(df.index)
    actual_y = str_index_values(df.columns)
    
    self.assertEqual(actual_x, expected_x)
    self.assertEqual(actual_y, expected_y)
    
#     COUNTER = COUNTER + 2
#     print COUNTER
       
def get_stack(self, meta, data, xks, yks, views, weights):
  
    stack = Stack('test')
    stack.add_data('test', data, meta)
    stack.add_link(x=xks, y=yks, views=views, weights=weights)

    # Add two basic net
    net_views = ViewMapper(
        template={
            'method': QuantipyViews().frequency,
            'kwargs': {'iterators': {'rel_to': [None, 'y']}}})    
    net_views.add_method(
        name='Net 1-3',
        kwargs={'logic': [1, 2, 3], 'text': {'en-GB': '1-3'}})    
    net_views.add_method(
        name='Net 4-6',
        kwargs={'logic': [4, 5, 6], 'text': {'en-GB': '4-6'}})         
    stack.add_link(x=xks, y=yks, views=net_views, weights=weights)
    
    # Add block net  
    net_views.add_method(
        name='Block net',
        kwargs={
            'logic': [
                {'bn1': [1, 2]},
                {'bn2': [2, 3]},
                {'bn3': [1, 3]}]})
    stack.add_link(x=xks, y=yks, views=net_views.subset(['Block net']), weights=weights)
    
    # Add NPS
    ## TO DO
    
    # Add standard deviation
    desc_views = ViewMapper(
        template = {
            'method': QuantipyViews().descriptives,
            'kwargs': {'iterators': {'stats': ['mean', 'median', 'stddev']}}})
            
    desc_views.add_method(name='descriptives')        
    stack.add_link(x=xks, y=yks, views=desc_views, weights=weights)

    # Add tests
    test_views = ViewMapper(
        template={
            'method': QuantipyViews().coltests,
            'kwargs': {
                'mimic': 'askia',
                'iterators': {
                    'metric': ['props', 'means'],
                    'level': ['low', 'mid', 'high']
                }
            }
        }
    )        
    test_views.add_method('askia tests')
    stack.add_link(x=xks, y=yks, views=test_views)        

    return stack
       