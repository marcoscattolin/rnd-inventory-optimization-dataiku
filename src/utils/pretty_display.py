from IPython.display import display_html
from itertools import chain,cycle
import pandas as pd

def display_side_by_side(*args,titles=cycle([''])):
    html_str=''
    for df,title in zip(args, chain(titles,cycle(['</br>'])) ):
        html_str+='<th style="text-align:left"><td style="vertical-align:top">'
        html_str+=f'<h2 style="text-align: left;">{title}</h2>'
        html_str+=df.to_html().replace('table','table style="display:inline"')
        html_str+='</td></th>'
    display_html(html_str,raw=True)


def _color_red_or_green(val):
    color = 'green' if val > 0 else ''
    return 'color: %s' % color


def numpy_to_pandas_pretty(np_matrix, indices, columns, index_name, columns_name):
    pd_df = pd.DataFrame(np_matrix, index=indices, columns=columns)
    pd_df.index.name = index_name
    pd_df.columns.name = columns_name
    pd_df = pd_df.astype(int)
    pd_df = pd_df.style.applymap(_color_red_or_green)
    return pd_df