# -*- coding: utf-8 -*-
from flask_assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "libs/metisMenu/dist/metisMenu.css",
    "libs/startbootstrap-sb-admin-2/dist/css/sb-admin-2.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "libs/metisMenu/dist/metisMenu.js",
    "libs/startbootstrap-sb-admin-2/dist/js/sb-admin-2.js",
    "libs/highcharts-release/highcharts.js",
    "libs/moment/moment.js",
    "js/plugins.js",
    output="public/js/common.js"
)

weather_js = Bundle(
    "js/weather-daily-chart.js",
    output="public/js/weather_prod.js"
)

charts_daily_js = Bundle(
    "js/daily_chart.js",
    "js/daily_kessel_chart.js",
    "js/daily_puffer_chart.js",
    output="public/js/dialy_charts.js"
)

charts_weekly_js = Bundle(
    "js/weekly_chart.js",
    "js/weekly_ophours_chart.js",
    "js/weekly_pellets_chart.js",
    output="public/js/weekly_charts.js"
)

charts_monthly_js = Bundle(
    "js/monthly_ophours_chart.js",
    "js/monthly_pellets_chart.js",
    output="public/js/monthly_charts.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
assets.register("js_weather", weather_js)
assets.register("js_charts_daily", charts_daily_js)
assets.register("js_charts_weekly", charts_weekly_js)
assets.register("js_charts_monthly", charts_monthly_js)
