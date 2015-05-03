$(document).ready(function () {
    $(function () {
        var x = new Date();
        var currentTimeZoneOffsetInHours = x.getTimezoneOffset() / 60;

        Highcharts.setOptions({
            global: {
                timezoneOffset: currentTimeZoneOffsetInHours * 60
            }
        });
    });
});
