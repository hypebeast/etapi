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
    "js/plugins.js",
    "js/weather-daily-chart.js",
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
