# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from flask import (Blueprint, request, render_template, redirect, url_for)

from etapi.lib.helpers import get_timestamps
from etapi.lib.helpers import get_todays_date
from etapi.lib.helpers import convert_series_to_local_time
from etapi.tables.helpers import get_table_data


tables = Blueprint('tables', __name__, url_prefix='/tables',
                    static_folder="../static")


@tables.route("/")
def index():
    data = get_table_data()
    return render_template("tables/tables.html", data=data)
