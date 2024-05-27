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
    "Prime Key": list(range(1, 11)),
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
                       "Member F", "Member G", "Member H", "Member I", "Member J"],
    "Timestamp": [datetime(2024, 5, 27, 23, 59, 59) for _ in range(10)]
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
        row_deletable=False,
        filter_action="native",
        sort_action="native",
        row_selectable='single'
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
    
    # 자 프로젝트 추가 폼
    html.Div([
        html.H3("Add Subtask"),
        dcc.Input(id='sub-area', type='text', placeholder='Area', required=True),
        dcc.Input(id='sub-start-date', type='date', placeholder='Start Date', required=True),
        dcc.Input(id='sub-end-date', type='date', placeholder='End Date', required=True),
        dcc.Input(id='sub-topic', type='text', placeholder='Topic', required=True),
        dcc.Input(id='sub-progress', type='number', placeholder='Progress Percentage', required=True),
        dcc.Input(id='sub-leader', type='text', placeholder='Project Leader', required=True),
        dcc.Input(id='sub-member', type='text', placeholder='Project Member', required=True),
        dcc.Input(id='sub-password', type='password', placeholder='Password', required=True),
        html.Button('Add Subtask', id='add-subtask-button', n_clicks=0)
    ], style={'display': 'none'}, id='subtask-form'),
    
    # 과제 삭제 폼
    html.Div([
        html.H3("Delete Task"),
        dcc.Input(id='delete-key', type='number', placeholder='Prime Key', required=True),
        dcc.Input(id='delete-password', type='password', placeholder='Password', required=True),
        html.Button('Delete Task', id='delete-button', n_clicks=0)
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

# 콜백 정의: 데이터 테이블 업데이트 및 자 프로젝트 추가 폼 표시
@app.callback(
    Output('datatable', 'data'),
    Output('subtask-form', 'style'),
    [Input('add-button', 'n_clicks'), Input('add-subtask-button', 'n_clicks'), Input('delete-button', 'n_clicks')],
    [State('area', 'value'), State('start-date', 'value'), State('end-date', 'value'),
     State('topic', 'value'), State('progress', 'value'), State('leader', 'value'),
     State('member', 'value'), State('password', 'value'), State('datatable', 'data'),
     State('datatable', 'selected_rows'), State('sub-area', 'value'), State('sub-start-date', 'value'),
     State('sub-end-date', 'value'), State('sub-topic', 'value'), State('sub-progress', 'value'),
     State('sub-leader', 'value'), State('sub-member', 'value'), State('sub-password', 'value'),
     State('delete-key', 'value'), State('delete-password', 'value')]
)
def modify_table(add_clicks, sub_clicks, delete_clicks, area, start_date, end_date, topic, progress, leader, member, password, rows, selected_rows, sub_area, sub_start_date, sub_end_date, sub_topic, sub_progress, sub_leader, sub_member, sub_password, delete_key, delete_password):
    if selected_rows is not None and len(selected_rows) > 0:
        subtask_form_style = {'display': 'block'}
    else:
        subtask_form_style = {'display': 'none'}

    if add_clicks > 0 and password == "rabbit1":
        new_row = {
            "Prime Key": max([row['Prime Key'] for row in rows]) + 1 if rows else 1,
            "Area": area,
            "Start Date": start_date,
            "End Date": end_date,
            "Topic": topic,
            "Progress Percentage": progress,
            "Project Leader": leader,
            "Project Member": member,
            "Timestamp": datetime.now()
        }
        rows.append(new_row)
    
    if sub_clicks > 0 and sub_password == "rabbit1" and selected_rows is not None and len(selected_rows) > 0:
        parent_row = rows[selected_rows[0]]
        sub_row = {
            "Prime Key": max([row['Prime Key'] for row in rows]) + 1,
            "Area": sub_area,
            "Start Date": sub_start_date,
            "End Date": sub_end_date,
            "Topic": f"{parent_row['Topic']} - {sub_topic}",
            "Progress Percentage": sub_progress,
            "Project Leader": sub_leader,
            "Project Member": sub_member,
            "Timestamp": datetime.now()
        }
        rows.append(sub_row)
    
    if delete_clicks > 0 and delete_password == "rabbit1":
        rows = [row for row in rows if row['Prime Key'] != delete_key]

    return rows, subtask_form_style

# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True)
