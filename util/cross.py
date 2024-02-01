def cross(dataframe_a, dataframe_b=0):
    # dataframe_b가 숫자인 경우
    if isinstance(dataframe_b, (int, float)):
        up_cross = (dataframe_a.shift(1) < dataframe_b) & (dataframe_a > dataframe_b)
        down_cross = (dataframe_a.shift(1) > dataframe_b) & (dataframe_a < dataframe_b)
    else:
        # dataframe_b가 Series 또는 DataFrame 열인 경우
        up_cross = (dataframe_a.shift(1) < dataframe_b.shift(1)) & (dataframe_a > dataframe_b)
        down_cross = (dataframe_a.shift(1) > dataframe_b.shift(1)) & (dataframe_a < dataframe_b)

    return up_cross, down_cross
