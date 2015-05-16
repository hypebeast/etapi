$(document).ready(function () {
    $(function () {
        $('#monthly-pellets-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Last 30 Days Pellets Consumption'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'kg'
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0">&nbsp<b>{point.y:.1f} kg</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: [
                {
                    name: 'Pellets',
                    data: pellets_data
                }
            ]
        });
    });
});

