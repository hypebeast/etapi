$(document).ready(function () {
    $(function () {
        $('#weather-daily-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Temperature'
            },
            colors: ['#B4C7DA', '#153E7E', '#ED561B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'],
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: '°C'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b> {point.y:.1f} °C</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.0,
                    groupPadding: 0.5,
                    borderWidth: 0,
                    pointWidth: 5
                }
            },
            series: [
                {
                    name: 'Temperature',
                    data: data
                }
            ]
        });
    });
});

