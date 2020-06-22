import leather

def total_case_chart(data):
    leather.theme.axis_title_gap=30
    leather.theme.default_chart_width=1000
    leather.theme.default_series_colors = ['#87dcce']

    chart = leather.Chart('Total COVID-19 Cases in Ontario')
    chart.add_line(data)
    chart.add_y_axis(name='Number of Cases')
    chart.add_x_axis(name='Days Since Jan 26, 2020', ticks=[i for i in range(0, 150, 10)])
    chart.to_svg('total_cases.svg')

    return