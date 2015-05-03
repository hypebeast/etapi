$(document).ready(function () {
    $(function () {
        $('#daily-puffer-chart').highcharts({
            chart: {
                type: 'spline'
            },
            title: {
                text: 'Puffer'
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
                    '<td style="padding:0"><b>{point.y:.1f} °C</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                series: {
                    marker: {
                        radius: 2
                    }
                }
            },
            series: [
                {
                    name: 'Temperatur Oben',
                    data: puffer_temp_top_data
                },
                {
                    name: 'Temperatur Unten',
                    data: puffer_temp_bottom_data
                },
                {
                    name: 'Warmwasserspeicher',
                    data: puffer_temp_hot_water_storage
                }
            ]
        });
    });
});

