import streamlit as st
import numpy as np
import plotly.graph_objs as go

def generate_data(normal_min, normal_max, abnormal_min, abnormal_max):
    # 정상 데이터 (0~79 인덱스): 무조건 normal_min과 normal_max 사이
    normal_samples = 80
    normal_data = np.random.uniform(normal_min, normal_max, normal_samples)
    
    # 비정상 데이터 (80~99 인덱스): 무조건 abnormal_min과 abnormal_max 사이
    abnormal_samples = 20
    abnormal_data = np.random.uniform(abnormal_min, abnormal_max, abnormal_samples)
    
    # 데이터 생성 (정상 데이터 먼저, 그 다음 비정상 데이터)
    combined_data = np.concatenate([normal_data, abnormal_data])
    
    return combined_data

def min_max_scaling(data, scale_min, scale_max):
    scaled = (data - scale_min) / (scale_max - scale_min)
    return scaled

def main():

    # 페이지 레이아웃 설정
    graph_placeholder_top = st.empty()
    input_placeholder = st.container()  # 입력 위젯을 담을 컨테이너
    graph_placeholder_bottom = st.empty()



    # 초기 세션 상태 설정
    if 'normal_min' not in st.session_state:
        st.session_state.normal_min = 0.25
    if 'normal_max' not in st.session_state:
        st.session_state.normal_max = 0.256
    if 'abnormal_min' not in st.session_state:
        st.session_state.abnormal_min = 0.28
    if 'abnormal_max' not in st.session_state:
        st.session_state.abnormal_max = 0.289
    if 'scale_min' not in st.session_state:
        st.session_state.scale_min = 0.27
    if 'scale_max' not in st.session_state:
        st.session_state.scale_max = 0.273

    # 입력 섹션
    with input_placeholder:

        # 정상 데이터 범위 입력
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.normal_min = st.number_input(
                'Normal Min', 
                value=st.session_state.normal_min, 
                step=0.001, 
                key='normal_min_input', 
                format="%.3f"
            )
        with col2:
            st.session_state.normal_max = st.number_input(
                'Normal Max', 
                value=st.session_state.normal_max, 
                step=0.001, 
                key='normal_max_input', 
                format="%.3f"
            )

        # 비정상 데이터 범위 입력
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.abnormal_min = st.number_input(
                'Abnormal Min', 
                value=st.session_state.abnormal_min, 
                step=0.001, 
                key='abnormal_min_input', 
                format="%.3f"
            )
        with col4:
            st.session_state.abnormal_max = st.number_input(
                'Abnormal Max', 
                value=st.session_state.abnormal_max, 
                step=0.001, 
                key='abnormal_max_input', 
                format="%.3f"
            )

        # 스케일링 범위 입력
        col5, col6 = st.columns(2)
        with col5:
            st.session_state.scale_min = st.number_input(
                'Scale Min', 
                value=st.session_state.scale_min, 
                step=0.001, 
                key='scale_min_input', 
                format="%.3f"
            )
        with col6:
            st.session_state.scale_max = st.number_input(
                'Scale Max', 
                value=st.session_state.scale_max, 
                step=0.001, 
                key='scale_max_input', 
                format="%.3f"
            )

    # 데이터 생성
    data = generate_data(
        st.session_state.normal_min, 
        st.session_state.normal_max, 
        st.session_state.abnormal_min, 
        st.session_state.abnormal_max
    )

    # 데이터 스케일링
    scaled_data = min_max_scaling(data, st.session_state.scale_min, st.session_state.scale_max)

    # 스케일링된 데이터 그래프 (맨 위)
    with graph_placeholder_top:
        st.header('Min-Max Scaled Data')
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(y=scaled_data, mode='lines+markers', 
                                   line=dict(color='blue'),
                                   marker=dict(color=['blue']*80 + ['red']*20)))

        # 0.7 수평선 추가
        fig2.add_shape(type='line',
                       x0=0, y0=0.7, x1=99, y1=0.7,
                       line=dict(color='green', width=2, dash='dash'))

        fig2.update_layout(
            xaxis_title='Sample Index', 
            yaxis_title='Scaled Value',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)

    # 원본 데이터 그래프 (맨 아래)
    with graph_placeholder_bottom:
        st.header('Original Data Distribution')
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(y=data, mode='lines+markers', 
                                   line=dict(color='blue'),
                                   marker=dict(color=['blue']*80 + ['red']*20)))
        fig1.update_layout(
            xaxis_title='Sample Index', 
            yaxis_title='Value',
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)

if __name__ == '__main__':
    main()
