from bokeh.plotting import *
from bokeh.models import (LinearAxis, SingleIntervalTicker,
        HoverTool, ColumnDataSource)

def heatmap_T_range(df, temps, title=None):
    data = df[['pos', 'seq', 'Temp', 'Diff']]
    row_range = [str(x) for x in sorted(temps)]
    col_range = [str(x) for x in set(df['pos'])]
    source = ColumnDataSource(
        data=dict(
            row=[str(x) for x in data['Temp']],
            col=[str(x) for x in data['pos']],
            base=data['seq'],
            alphas=data['Diff'],
        )
    )

    p = figure(title=title,
               tools='resize,save,box_zoom,reset,pan',
               x_range=col_range, 
               y_range=row_range,
               x_axis_type=None,
               plot_width=800)

    p.rect('col', 'row', 0.9, 0.9, source=source, alpha='alphas', color='#FF7F00', line_color=None)
    p.grid.grid_line_color = None
    ticker = SingleIntervalTicker(interval=100, num_minor_ticks=10)
    xaxis = LinearAxis(ticker=ticker)
    p.add_layout(xaxis, 'below')
    show(p)

    
def sequence_heatmap(df, temp, num_cols=60):
    data = df[df['Temp'] == temp]
    num_rows = data.shape[0] // num_cols
    if data.shape[0] % num_cols:
        num_rows += 1

    rows = [(x // num_cols) + 1 for x in range(data.shape[0])]
    cols = [(x - x // num_cols * num_cols) + 1 for x in range(data.shape[0])]
    

    row_range = [str(x) for x in reversed(range(1,num_rows+1))]
    col_range = [str(x) for x in range(1, num_cols)]
    
    source = ColumnDataSource(
        data=dict(
            row=[str(x) for x in rows],
            col=[str(x) for x in cols],
            base=data['seq'],
            alphas=data['Diff'],
        )
    )
    
    p = figure(title='Human HSR1 prob diff', tools='resize,hover,save',
           x_range=col_range, y_range=row_range, x_axis_type=None, plot_width=800)

    p.rect('col', 'row', 0.9, 0.9, source=source, alpha='alphas', color='#FF7F00', line_color=None)
    text_props = {
        'source': source,
        'angle': 0,
        'color': 'black',
        'text_color': '#586e75',
        'text_align': 'center',
        'text_baseline': 'middle',
    }

    p.text(x=dict(field='col', units='data'),
           y=dict(field='row', units='data'),
           text=dict(field='base', units='data'),
           text_font_size='10pt', text_font_style='bold', **text_props)

    p.grid.grid_line_color = None
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
        ('base', '@base'),
        ('shape', '@alphas')
    ]
    ticker = SingleIntervalTicker(interval=10, num_minor_ticks=10)
    xaxis = LinearAxis(ticker=ticker)
    p.add_layout(xaxis, 'below')
    
    show(p)
