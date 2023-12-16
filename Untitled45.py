#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import geopandas as gpd
import pydeck as pdk
import plotly.graph_objects as go
import dash
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
from ipywidgets import interact, widgets



df = pd.read_excel('c:/analysis/data-mining/data/사고1.xlsx')
df['month'] = df['사고일시'].str.slice(start = 5, stop = 9)
a = df['month'].value_counts().sort_index()
months = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월','10월','11월','12월']
accident_counts = [50, 49, 70, 53, 78, 65, 58, 47, 57,72,65,56]
trace = go.Bar(
   x = months,
   y = accident_counts,
   marker=dict(color='slategray'),
   opacity=1
  
    
    # text = 마우스 커서 선택 시 나타낼 추가정보
   ) 

data = [trace]

layout = go.Layout(title = '월별 사고발생수')

fig4 = go.Figure(data, layout)

#날씨별 교통량
total_accidents = 720
sunny_accidents = 650
rainy_accidents = 65
snowy_accidents = 5

labels = ['맑음', '비', '눈']
values = [sunny_accidents, rainy_accidents, snowy_accidents]
colors = ['firebrick', 'steelblue', 'darkgray']

fig5 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3,marker=dict(colors=colors))])
fig5.update_layout(title=f'전체 사고 중 각 날씨 조건별 사고 비율 (총 사고 수: {total_accidents}건)')


weather=['맑음', '비', '눈']

average_traffic_by_weather = df.groupby('기상상태')['구간별 통행량'].mean()

colors = {'맑음': 'firebrick', '비': 'steelblue', '눈': 'darkgray'}
trace = go.Bar(
   x = weather,
   y = average_traffic_by_weather,
   marker=dict(color=[colors[weather_type] for weather_type in weather])
    # text = 마우스 커서 선택 시 나타낼 추가정보
   ) 

data = [trace]

layout = go.Layout(title = '날씨별 평균 통행량',yaxis=dict(
        title='통행량',  # y축 제목 설정
        tickformat=',',  # 천 단위 구분 기호 설정
    ))

fig6 = go.Figure(data, layout)

percent = df.groupby('기상상태')['사고발생비율'].mean()
colors = {'맑음': 'firebrick', '비': 'steelblue', '눈': 'darkgray'}
trace = go.Bar(
   x = weather,
   y = percent,
   marker=dict(color=[colors[weather_type] for weather_type in weather])
    # text = 마우스 커서 선택 시 나타낼 추가정보
   ) 

data = [trace]

layout = go.Layout(title = '날씨별 평균 사고발생비율',
                   yaxis=dict(
                       tickformat='%'
                   )
                  )

fig7= go.Figure(data, layout)

# 데이터 불러오기
df = pd.read_excel('c:/analysis/data-mining/data/사고1.xlsx')

# '사고일시' 열에서 월 정보 추출
df['month'] = df['사고일시'].str.slice(start=5, stop=8)

# 월별 시간대 사고량 계산
df_g = df.groupby(['month', '시간대']).size().reset_index(name='accident_count')

# 그래프 그리기
new_fig = px.line(df_g, x='month', y='accident_count', color='시간대', markers=True,
                  title='월별 시간대 사고량 계산', labels={'month': '월', 'accident_count': '사고량'})


filtered_sections = df['구간'].unique()
# 기상상태에 따른 색상 및 크기 지정
weather_colors = {'맑음': 'firebrick', '눈': 'darkgray', '비': 'steelblue'}
size_column = '구간별 통행량'  # Bubble chart에서 크기를 나타낼 열 선택

# 특정 구간에 대한 기상상태별 사고일시별 통행량 그래프 함수
def plot_traffic_by_weather_and_date(section):
    subset_df = df[df['구간'] == section]

    # 각 사고일시별 구간 교통량 합계 계산
    traffic_sum = subset_df.groupby(['사고일시', '기상상태', '시군구'])[size_column].sum().reset_index()

    # 각 점에 대한 레이블 추가
    traffic_sum['label'] = range(1, len(traffic_sum) + 1)

    # 평균 교통량 빨간색 점선으로 추가
    avg_traffic = traffic_sum[size_column].mean()

    # Plotly를 활용한 기상상태별 사고일시별 통행량 Bubble chart 생성
    fig8 = px.scatter(traffic_sum, x='label', y=size_column, color='기상상태', size=size_column,
                     color_discrete_map=weather_colors,  # 기상상태에 따른 색상 지정
                     title=f'구간: {section}, 사고구간 교통량',
                     labels={size_column: '교통량', 'label': '사고'},
                     height=500,
                     width=1000,
                     hover_data={'label': False, '사고일시': True, size_column: True, '시군구': True})  # 툴팁으로 표시할 데이터 지정

  

    # 정수만 표시되도록 x축 설정
    fig8.update_xaxes(tickvals=list(traffic_sum['label']), ticktext=list(traffic_sum['label']))
    fig8.update_layout(yaxis=dict(tickformat=','))
    # 레이아웃 설정
    fig8.update_layout(xaxis_title='사고', xaxis=dict(showgrid=False))

# 인터랙티브 드롭다운을 통한 시각화
interact(plot_traffic_by_weather_and_date, section=widgets.Dropdown(options=filtered_sections, description='구간'))


df9 = pd.read_excel('c:/analysis/data-mining/data/사고1.xlsx')

# 요일 순서 정의
days_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

# 요일별 사고 건수 계산
accidents_count_by_day = df9['요일'].value_counts().reindex(days_order).reset_index()
accidents_count_by_day.columns = ['요일', '사고 건수']
bar_color = 'cadetblue'
# Plotly를 사용하여 동적 시각화
fig3 = px.bar(accidents_count_by_day, x='요일', y='사고 건수', title='요일별 교통사고 건수')
fig3.update_traces(marker_color=bar_color)
# y 축 눈금 간격을 30의 배수로 설정
fig3.update_yaxes(dtick=30)

# y 축 범위를 0에서 130으로 설정
fig3.update_layout(yaxis=dict(range=[0, 140]))


# Read data for Plotly bar chart
df1 = pd.read_csv('c:/analysis/data-mining/data/vdsmonth.csv', encoding='utf-8')
# Create a Plotly bar chart
trace1 = go.Bar(
    x=df1['구간'],
    y=df1['평균 통행량'],
    name='평균 통행량',
    marker=dict(color='seagreen'),
    width=0.4,
)

data = [trace1]

layout = go.Layout(
    title='평균 교통량 상위 10개 구간',
    yaxis=dict(
        title='평균 통행량',
        side='left',
        position=0,
        tickformat=',',  # 천 단위 구분 기호 설정
    ),
    yaxis2=dict(
        title='사고발생수',
        overlaying='y',
        side='right',
        position=0.99,
        range=[0, df1['사고발생수'].max()],
    ),
)

fig = go.Figure(data, layout)
fig.add_trace(go.Bar(
    x=df1['구간'],
    y=df1['사고발생수'],
    name='사고발생수',
    marker=dict(color='crimson'),
    width=0.4,
    yaxis='y2'
))

# Read data for additional Plotly line chart
df2 = pd.read_csv('c:/analysis/data-mining/data/vdsless.csv', encoding='EUC-KR')

trace2 = go.Bar(
    x=df2['구간'],
    y=df2['평균 통행량'],
    name='평균 통행량',
    marker=dict(color='seagreen'),
    width=0.4,
)

data2 = [trace2]

layout2 = go.Layout(
    title='평균 교통량 하위 10개 구간',
    yaxis=dict(
        title='평균 통행량',
        side='left',
        position=0,
        tickformat=',',  # 천 단위 구분 기호 설정
    ),
    yaxis2=dict(
        title='사고발생수',
        overlaying='y',
        side='right',
        position=1.0,
        range=[0, df2['사고발생수'].max()],
        tickformat=',',  # 천 단위 구분 기호 설정
    )
)

fig2 = go.Figure(data2, layout2)
fig2.add_trace(go.Bar(
    x=df2['구간'],
    y=df2['사고발생수'],
    name='사고발생수',
    marker=dict(color='crimson'),
    width=0.4,
    yaxis='y2'
))

# Read data for PyDeck map
df3 = pd.read_csv('c:/analysis/data-mining/data/3.csv', encoding='euc-kr')
df3['width_factor'] = df3['평균 통행량'] / 8000

# Create PyDeck LineLayer
line_layer = pdk.Layer(
    "LineLayer",
    df3,
    get_source_position="[lon_x, lat_x]",
    get_target_position="[lon_y, lat_y]",
    get_color='[사고발생수*4, 150, 0, 250]',
    get_width='[width_factor]',
    highlight_color=[255, 255, 0],
    picking_radius=10,
    auto_highlight=True,
    pickable=True,
)

# PyDeck view state and tooltip

TOOLTIP_TEXT = {"html": "구간: {구간}<br />평균통행량 {평균 통행량}<br />사고발생수 {사고발생수} <br />"}

view_state = pdk.ViewState(latitude=36.65141, longitude=127.8106, zoom=8)

# Create PyDeck Deck
r = pdk.Deck(layers=line_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
r.to_html("line_layer.html")



with open("line_layer.html", "r", encoding="utf-8") as f:
    pydeck_html = f.read()

dropdown_options = [{'label': section, 'value': section} for section in filtered_sections]
    
# Dash app setup
app = dash.Dash(__name__)

# Tabs layout
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='1', value='tab-1'),
        dcc.Tab(label='2', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def update_tab(selected_tab):
    if selected_tab == 'tab-1':
        return html.Div([
            # main title
            html.H2('경부고속도로 교통사고',
                    style={'textAlign': 'center',
                           'marginBottom': 8,
                           'marginTop': 8}),

            # Left layout
            html.Div([
                html.Div(className='Bar',
                         children=[
                             html.Div(dcc.Graph(id='날씨별 사고 발생률', figure=fig5),
                                      style={'float': 'left', 'display': 'inline-block', 'width': '33%'}),
                             html.Div(dcc.Graph(id='날씨별 평균 통행량', figure=fig6),
                                      style={'float': 'left', 'display': 'inline-block', 'width': '33%'}),
                             html.Div(dcc.Graph(id='날씨별 평균 사고발생비율', figure=fig7),
                                      style={'float': 'right', 'display': 'inline-block', 'width': '33%'}),
                         ]),

                # bar chart
                html.Div(className='Bar',
                         children=[
                             html.Div(dcc.Graph(id='요일별 사고량', figure=fig3),
                                      style={'float': 'left', 'display': 'inline-block', 'width': '50%'}),
                             html.Div(dcc.Graph(id='월별 사고량', figure=fig4),
                                      style={'float': 'right', 'display': 'inline-block', 'width': '50%'}),
                         ]),

                # scatter line
                html.Div(className='Bar',
                         children=[dcc.Graph(id='사고시간대', figure=new_fig)],
                         style={'float': 'left', 'display': 'inline-block', 'width': '100%'}),
            ]),
        ])

    elif selected_tab == 'tab-2':
        return html.Div([
        # main title
        html.H2('경부고속도로 교통사고',
                style={'textAlign': 'center',
                       'marginBottom': 8,
                       'marginTop': 8}),

        # Right layout
        html.Div([
    # Dropdown and interactive-plot
    html.Div([
        dcc.Dropdown(
            id='section-dropdown',
            options=dropdown_options,
            value=filtered_sections[0],
            style={'width': '50%'}
        ),
        dcc.Graph(id='interactive-plot', style={'width': '100%'})  # Adjust width here
    ], style={'float': 'left', 'display': 'inline-block', 'width': '100%'}),

            # Bar charts
            html.Div(className='Bar',
                     children=[
                         html.Div(dcc.Graph(id='많은 통행량', figure=fig),
                                  style={'float': 'left', 'display': 'inline-block', 'width': '100%'}),
                         html.Div(dcc.Graph(id='적은 통행량', figure=fig2),
                                  style={'float': 'left', 'display': 'inline-block', 'width': '100%'}),
                     ]),
        ], style={'float': 'left', 'display': 'inline-block', 'width': '50%'}),

        # PyDeck graph
        html.Div([
            dcc.Dropdown(
                id='section-dropdown-pydeck',
                options=[{'label': 'All Sections', 'value': 'All Sections'}] +
                        [{'label': section, 'value': section} for section in df3['구간']],
                value='All Sections',
                style={'width': '50%'}
            ),
            html.Div(className='pydeck',
                     children=[html.Iframe(
                         id='pydeck-graph',
                         srcDoc=pydeck_html,
                         width='100%',
                         height='1000px',
                     )]),
        ], style={'float': 'right', 'display': 'inline-block', 'width': '50%'}),
    ])

            
    

@app.callback(
    Output('interactive-plot', 'figure'),
    [Input('section-dropdown', 'value')]
)
def update_interactive_plot(selected_section):
    subset_df = df[df['구간'] == selected_section]
    traffic_sum = subset_df.groupby(['사고일시', '기상상태', '시군구'])[size_column].sum().reset_index()
    traffic_sum['label'] = range(1, len(traffic_sum) + 1)
    avg_traffic = traffic_sum[size_column].mean()

    fig = px.scatter(traffic_sum, x='label', y=size_column, color='기상상태', size=size_column,
                     color_discrete_map=weather_colors,
                     title=f'구간: {selected_section}, 사고구간 교통량',
                     labels={size_column: '교통량', 'label': '사고'},
                     height=500,
                     width=800,
                     hover_data={'label': False, '사고일시': True, size_column: True, '시군구': True})
    fig.update_xaxes(tickvals=list(traffic_sum['label']), ticktext=list(traffic_sum['label']))
    fig.update_layout(xaxis_title='사고', xaxis=dict(showgrid=False))

    return fig


@app.callback(
    Output('pydeck-graph', 'srcDoc'),
    [Input('section-dropdown-pydeck', 'value')]
)
def update_pydeck_graph(selected_section):
    if selected_section == 'All Sections':
        subset_df = df3.copy()
    else:
        subset_df = df3[df3['구간'] == selected_section]

    # Update PyDeck Deck with new data
    new_line_layer = pdk.Layer(
        "LineLayer",
        subset_df,
        get_source_position="[lon_x, lat_x]",
        get_target_position="[lon_y, lat_y]",
        get_color='[사고발생수*7, 150, 0, 250]',
        get_width='[width_factor]',
        highlight_color=[255, 255, 0],
        picking_radius=10,
        auto_highlight=True,
        pickable=True,
    )

    new_r = pdk.Deck(layers=new_line_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
    new_r.to_html("line_layer.html")

    with open("line_layer.html", "r", encoding="utf-8") as f:
        updated_pydeck_html = f.read()

    return updated_pydeck_html

    
    
if __name__ == '__main__':
    app.run_server(debug=False, port=8072)

