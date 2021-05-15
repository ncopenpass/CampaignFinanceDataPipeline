#!/usr/bin/env python

from pathlib import Path
from pprint import pprint as pp
import cytoolz.curried as cc
import pandas as pd
import re
import numpy as np


pd.set_option('display.max_rows', 100)
pd.set_option('display.min_rows', 30)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 10000)



data_files = cc.pipe(
    Path('s3-data').rglob('*.csv')
    , cc.map(lambda p: (p.stem, pd.read_csv(p)))
    , dict
)


committee_names_df = (
    data_files['committees_export_20210410']['committee_name'].to_frame('committee_name')
    .assign(
        committee_name_clean=lambda df: (
            df.committee_name
            .str.replace(' {2,}', ' ')
            .str.replace('RE-? ?ELECT', 'ELECT')
            .str.strip())
        , committee_entity=pd.NA)
)



regex_dict = {
    'committee_elect_for'        : '(?:COMM(?:ITTEE)? TO ?ELECT (.*)) ?(?: FOR (?:.*))?'
    , 'committee_elect'          : '(?:COMM(?:ITTEE)? TO ?ELECT (.*))'
    , 'comm_suffix'              : '(.*) COMM$'
    , 'comm_to_elect_suffix'     : '^(.*) COMM TO ELECT'
    , 'comm_in_support_prefix'   : 'COMM IN SUPPORT OF (.*)'
    , 'vote_for'                 : '^VOTE (.*) FOR (?:.*)'
    , 'vote'                     : '^VOTE (.*)'
    , 'citizens_for_x'           : 'CITIZENS FOR (.*)'
    , 'x_for_x'                  : '^(.*) FOR (?:.*)'
    , 'x_committee'              : '(.*) COMMITTEE$'
    , 'committee_to_elect_2word' : '^(?:(?:JUDGE|SHERIFF) ?)(.*) COMM(?:ITTEE)? TO ELECT'
    , 'friends_of_x'             : 'FRIENDS OF (.*)'
    , 'elect'                    : 'ELECT (.*)'
    , 'campaign_suffix'          : '^(.*) CAMPAIGN'
    , 'keep'                     : 'KEEP (?:JUDGE|SHERIFF)? ?(.*)'
    , '4'                        : '(.*) 4 (?:.*)'
    , 'nc_house'                 : '(.*) NC ?HOUSE'
    , 'citizens_support'         : 'CITIZENS IN SUPPORT OF(?: JUDGE)? (.*)'
    , 'pac_suffix'               : '^(.*) PAC$'
    , 'year_suffix'              : '(.*) (?:20)?[0-9]{2}$'
}




for regex_name, regex_pat in regex_dict.items():
    committee_names_df[regex_name] = committee_names_df['committee_name_clean'].str.extract(re.compile(regex_pat), expand=False)


committee_names_df['committee_entity'] = (
    committee_names_df.loc[:, regex_dict.keys()].bfill(axis='columns').iloc[:, 0]
    .str.replace('^(ELECT )?(JUDGE|SHERIFF) ', '')
    .str.replace('( SHERIFF|JUDGE)$', '')
    .str.strip()
)



manual_override_path = Path('manual_override.csv')
if manual_override_path.exists():
    manual_override_df = pd.read_csv(manual_override_path).set_index('committee_name')

    committee_names_df = (
        committee_names_df.merge(
            manual_override_df
            , how='left'
            , on='committee_name'
            , suffixes=(None, None))
        .assign(committee_entity=lambda df: df.committee_entity.mask(pd.isnull, df.manual_entity))
        .drop(columns=['manual_entity'])
    )


# committee_names_df.iloc[:, :3].to_clipboard(index=False)
