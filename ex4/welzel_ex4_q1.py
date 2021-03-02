import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'browser'

x=np.linspace(0.01,10,100)
y=1/(np.exp(x)+np.exp(-x))

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, name="plot",
                    line_shape='spline'))

fig.update_xaxes(title_text='l/Ln')
fig.update_yaxes(title_text='1/(e^(l/Ln)+e^(l/Ln)')

fig.write_html("./1b_plot.html")
fig.show()