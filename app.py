import dash
from dash import dcc, html, Input, Output, State
import dash_table
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 대시 앱 초기화
app = dash.Dash(__name__)

# 예시 데이터 생성
data = {
    "Area": ["Photo Resist", "Chemicals", "Slurry", "Bulk Gas", "Process Gas", "Wafer",
             "Photo Resist", "Chemicals", "Slurry", "Bulk Gas"],
    "Start Date": [datetime(2024, 1, 1) + timedelta(days=i*10) for i in range(10)],
    "End Date": [datetime(2024, 1, 1) + timedelta(days=(i*10 + 30)) for i in range(10)],
    "Topic": ["Project A", "Project B", "Project C", "Project D", "Project E",
              "Project F", "Project G", "Project H", "Project I", "Project J"],
    "Progress Percentage": [10*i for i in range(10)],
    "Project Leader": ["Leader A", "Leader B", "Leader C", "Leader D", "Leader E",
                       "Leader F", "Leader G", "Leader H", "Leader I", "Leader J"],
    "Project Member": ["Member A", "Member B", "Member C", "Member D", "Member E",
                       "Member F", "Member G", "Member H", "Member I", "Member J"]
}

df = pd.DataFrame(data)

# 색상 매핑을 위한 사전 정의
color_map = {
    "Photo Resist": "#1f77b4",  # blue
    "Chemicals": "#ff7f0e",     # orange
    "Slurry": "#2ca02c",        # green
    "Bulk Gas": "#d62728",      # red
    "Process Gas": "#9467bd",   # purple
    "Wafer": "#8c564b"          # brown
}

# 앱 레이아웃 정의
app.layout = html.Div([
    html.H1("Gantt Chart Example"),
    
    # Gantt 차트 렌더링
    dcc.Graph(id='gantt-chart'),
    
    # 테이블 렌더링
    dash_table.DataTable(
        id='datatable',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        filter_action="native",
        sort_action="native"
    ),
    
    # 입력 폼
    html.Div([
        html.H3("Add New Task"),
        dcc.Input(id='area', type='text', placeholder='Area', required=True),
        dcc.Input(id='start-date', type='date', placeholder='Start Date', required=True),
        dcc.Input(id='end-date', type='date', placeholder='End Date', required=True),
        dcc.Input(id='topic', type='text', placeholder='Topic', required=True),
        dcc.Input(id='progress', type='number', placeholder='Progress Percentage', required=True),
        dcc.Input(id='leader', type='text', placeholder='Project Leader', required=True),
        dcc.Input(id='member', type='text', placeholder='Project Member', required=True),
        dcc.Input(id='password', type='password', placeholder='Password', required=True),
        html.Button('Add Task', id='add-button', n_clicks=0)
    ]),
    
    # 숨겨진 div, 상태를 저장하기 위한 용도
    html.Div(id='hidden-div', style={'display': 'none'})
])

# 콜백 정의: Gantt 차트 업데이트
@app.callback(
    Output('gantt-chart', 'figure'),
    [Input('datatable', 'data')]
)
def update_gantt_chart(rows):
    df = pd.DataFrame(rows)
    fig = px.timeline(df, x_start="Start Date", x_end="End Date", y="Topic", color="Area",
                      title="Gantt Chart Example", color_discrete_map=color_map)
    fig.update_yaxes(categoryorder="total ascending")
    return fig

# 콜백 정의: 데이터 테이블 업데이트
@app.callback(
    Output('datatable', 'data'),
    [Input('add-button', 'n_clicks')],
    [State('area', 'value'), State('start-date', 'value'), State('end-date', 'value'),
     State('topic', 'value'), State('progress', 'value'), State('leader', 'value'),
     State('member', 'value'), State('password', 'value'), State('datatable', 'data')]
)
def add_row(n_clicks, area, start_date, end_date, topic, progress, leader, member, password, rows):
    if n_clicks > 0:
        if password == "rabbit1":
            new_row = {
                "Area": area,
                "Start Date": start_date,
                "End Date": end_date,
                "Topic": topic,
                "Progress Percentage": progress,
                "Project Leader": leader,
                "Project Member": member
            }
            rows.append(new_row)
        else:
            print("Incorrect password")
    return rows

# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True)
