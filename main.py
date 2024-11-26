import dash
import plotly.graph_objects as go
import numpy as np
import pandas as pd

from dash import dcc, html, dash_table
from config import tws
from thecalc import calculate_tw_multiplier

class MultiplierCalculator:
    @staticmethod
    def calculate(tw: float) -> float:
        return calculate_tw_multiplier(tw)

class TWCalculation:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.df, self.data_table = self.prepare_data()
        self.layout = self.create_layout()

    def prepare_data(self):
        nilai_tw = np.arange(90, 151)
        multiplier = [MultiplierCalculator.calculate(tw) for tw in nilai_tw]

        df = pd.DataFrame({
            'tw': nilai_tw,
            'multiplier': multiplier
        })

        data_table = pd.DataFrame({
            'tw': tws,
            'multiplier': [MultiplierCalculator.calculate(tw) for tw in tws],
            'rumus': [
                '-(4 * (100 - tw) / 100)² [dibatasi]' if tw < 100
                else '(tw - 100) * pow(1.02, max(0, (tw - 100) // 5 - 1)) / 150'
                for tw in tws
            ]
        })
        return df, data_table

    def create_layout(self):
        return html.Div(
            style={
                'maxWidth': '1200px',
                'margin': '0 auto',
                'padding': '20px',
                'fontFamily': 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
                'color': '#f0f0f0',
                'backgroundColor': '#121212',
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': '#252525',
                        'padding': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.5)',
                        'marginBottom': '20px'
                    },
                    children=[
                        html.H1('analisis: timewarp multiplier', style={'marginBottom': '20px'}),
                        dcc.Graph(
                            id='grafik-multiplier',
                            figure={
                                'data': [
                                    go.Scatter(
                                        x=self.df['tw'],
                                        y=self.df['multiplier'],
                                        mode='lines',
                                        name='Multiplier',
                                        line={'color': '#00bcd4'}
                                    ),
                                    go.Scatter(
                                        x=[100, 100],
                                        y=[self.df['multiplier'].min(), self.df['multiplier'].max()],
                                        mode='lines',
                                        name='Titik Transisi',
                                        line={'color': '#f44336', 'dash': 'dash'}
                                    ),
                                    go.Scatter(
                                        x=[90, 130],
                                        y=[0, 0],
                                        mode='lines',
                                        name='Garis Nol',
                                        line={'color': '#9e9e9e', 'dash': 'dash'}
                                    )
                                ],
                                "layout": go.Layout(
                                    title="analisis multiplier timewarp",
                                    xaxis={"title": "nilai tw", "color": "#f0f0f0"},
                                    yaxis={"title": "multiplier", "color": "#f0f0f0"},
                                    hovermode="closest",
                                    plot_bgcolor="#1e1e1e",
                                    paper_bgcolor="#121212",
                                )
                            }
                        ),
                        dash_table.DataTable(
                            id='tabel',
                            columns=[
                                {'name': 'TW', 'id': 'tw'},
                                {'name': 'Multiplier', 'id': 'multiplier', 'format': {'specifier': '.4f'}},
                                {'name': 'Rumus', 'id': 'rumus'}
                            ],
                            data=self.data_table.to_dict('records'),
                            style_table={'overflowX': 'auto'},
                            style_header={
                                'backgroundColor': '#333333',
                                'fontWeight': 'bold',
                                'padding': '10px',
                                'color': '#e0e0e0'
                            },
                            style_cell={
                                'textAlign': 'left',
                                'padding': '10px',
                                'backgroundColor': '#252525',
                                'color': '#e0e0e0',
                                'border': '1px solid #333333'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': '#2e2e2e'
                                }
                            ]
                        ),
                        html.Div(
                            style={'marginTop': '20px'},
                            children=[
                                html.H3('Pengamatan:', style={'color': '#e0e0e0'}),
                                html.Ul([
                                    html.Li(f'nilai minimum: {self.df["multiplier"].min():.4f} (pada TW = 90)'),
                                    html.Li(f'nilai maksimum: {self.df["multiplier"].max():.4f} (pada TW = 150)'),
                                    html.Li('titik transisi: 0 (pada TW = 100)')
                                ], style={'color': '#e0e0e0'})
                            ]
                        )
                    ]
                )
            ]
        )

    def run(self, debug=True):
        self.app.layout = self.layout
        self.app.run_server(debug=debug)

if __name__ == '__main__':
    TWCalculation().run()