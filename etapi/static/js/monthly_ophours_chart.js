$(document).ready(function () {
    $(function () {
        $('#monthly-ophours-chart').highcharts({
            chart: {
                type: 'column'
            },
            title: {
                text: 'Last 30 Days Operating Hours'
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                type: 'datetime', //y-axis will be in milliseconds
                dateTimeLabelFormats: { //force all formats to be hour:minute:second
                    second: '%H:%M:%S',
                    minute: '%H:%M:%S',
                    hour: '%H:%M:%S',
                    day: '%H:%M:%S',
                    week: '%H:%M:%S',
                    month: '%H:%M:%S',
                    year: '%H:%M:%S'
                },
                title: {
                  text: 'Stunden'
                },
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormatter: function () {
                    var duration = moment.duration(this.y, 'milliseconds');

                    var durationString = duration.hours() + ' h ' + duration.minutes() + ' m ' + duration.seconds() + ' s';
                    return '<tr><td style="color:{series.color};padding:0">Laufzeit: </td>' +
                            '<td style="padding:0">&nbsp<b>' + durationString + '</b></td></tr>';
                },
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
                    name: 'Laufzeit',
                    data: operating_hours_data
                }
            ]
        });
    });
});

