from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    send_file,
    Response
)
from database import (
    initialize_database,
    add_food_entry,
    get_food_entries,
    update_food_entry,
    delete_food_entry,
    add_food_master,
    get_food_master,
    get_app_foods,
    get_food_by_fdc_id,
    calculate_food_nutrition,
    get_daily_totals,
    add_custom_food,
    create_custom_item,
    delete_app_food,
    update_app_food
)
import csv
import sqlite3
from datetime import datetime, timedelta


app = Flask(__name__)

initialize_database()

TIME_SLOTS = [
    '7AM','8AM','9AM','10AM','11AM',
    '12PM','1PM','2PM','3PM','4PM',
    '5PM','6PM','7PM','8PM','9PM',
    '10PM','11PM','12AM','1AM'
]

@app.route("/")
def home():

    week_offset = int(
      request.args.get(
         "week_offset",
         0
      )
    )

    today = datetime.today() + timedelta(
      weeks=week_offset
    )

    monday = today - timedelta(days=today.weekday())
    current_week = monday.isocalendar().week

    week_dates = []

    for i in range(7):

        current_date = monday + timedelta(days=i)

        week_dates.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "display_date": current_date.strftime("%b %d"),
            "day": current_date.strftime("%a")
        })

    foods = get_food_entries()
    app_foods = get_app_foods()
    daily_totals = get_daily_totals()

    daily_totals_dict = {}

    for row in daily_totals:

        daily_totals_dict[row[0]] = {
            "calories": row[1],
            "protein": row[2],
            "carbs": row[3],
            "fat": row[4],
            "fiber": row[5],
            "sugar": row[6],
            "sodium": row[7]
        }

    return render_template(
        "index.html",
        week_dates=week_dates,
        time_slots=TIME_SLOTS,
        app_foods=app_foods,
        foods=foods,
        week_offset=week_offset,
        current_week=current_week,
        current_offset=week_offset,
        daily_totals=daily_totals_dict
    )




@app.route("/add-food", methods=["POST"])
def add_food():

    data = request.get_json()

    print("ADD FOOD HIT")
    print(data)

    nutrition = calculate_food_nutrition(
        int(data["fdc_id"]),
        float(data["quantity"]),
        data["unit"]
    )

    add_food_entry(
        data["date"],
        data["slot"],
        data["food_name"],
        float(data["quantity"]),
        data["unit"],
        int(data["fdc_id"]),
        nutrition["calories"],
        nutrition["protein"],
        nutrition["carbs"],
        nutrition["fat"],
        nutrition["fiber"],
        nutrition["sugar"],
        nutrition["sodium"]
    )

    return jsonify({
        "success": True
    })

@app.route("/update-food", methods=["POST"])
def update_food():

    data = request.get_json()

    nutrition = calculate_food_nutrition(
        int(data["fdc_id"]),
        float(data["quantity"]),
        data["unit"]
    )

    update_food_entry(
        data["id"],
        data["food_name"],
        float(data["quantity"]),
        data["unit"],
        int(data["fdc_id"]),
        nutrition["calories"],
        nutrition["protein"],
        nutrition["carbs"],
        nutrition["fat"],
        nutrition["fiber"],
        nutrition["sugar"],
        nutrition["sodium"]
    )

    return jsonify({
        "success": True
    })

@app.route("/delete-food", methods=["POST"])
def delete_food():

    data = request.get_json()

    delete_food_entry(
        data["id"]
    )

    return jsonify({
        "success": True
    })


@app.route(
    "/add-custom-food",
    methods=["POST"]
)
def add_custom_food_route():

    data = request.get_json()

    add_custom_food(

        data["display_name"],

        float(data["calories"]),

        float(data["protein"]),

        float(data["carbs"]),

        float(data["fat"]),

        float(data["fiber"]),

        float(data["sugar"]),

        float(data["sodium"]),

        float(data["serving_weight"])

    )

    return jsonify({
        "success": True
    })


@app.route("/foods")
def foods():

    foods = get_food_master()

    return render_template(
        "foods.html",
        foods=foods
    )

@app.route("/add-food-master", methods=["POST"])
def add_food_master_route():

    add_food_master(
        request.form["food_name"],
        request.form["calories"],
        request.form["protein"],
        request.form["carbs"],
        request.form["fat"],
        request.form["fiber"],
        request.form["sugar"],
        request.form["sodium"]
    )

    return redirect(
        url_for("foods")
    )

@app.route(
    "/save-custom-item",
    methods=["POST"]
)
def save_custom_item():
    # print("SAVE CUSTOM ITEM HIT")

    data = request.get_json()

    if not data["name"].strip():

        return jsonify({

            "success": False

        }), 400

    if len(data["items"]) == 0:

        return jsonify({

            "success": False

        }), 400

    totals = {

        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "fiber": 0,
        "sugar": 0,
        "sodium": 0

    }

    for item in data["items"]:

        nutrition = calculate_food_nutrition(
                item["fdc_id"],
                item["quantity"],
                item["unit"]
            )

        totals["calories"] += nutrition["calories"]
        totals["protein"] += nutrition["protein"]
        totals["carbs"] += nutrition["carbs"]
        totals["fat"] += nutrition["fat"]
        totals["fiber"] += nutrition["fiber"]
        totals["sugar"] += nutrition["sugar"]
        totals["sodium"] += nutrition["sodium"]

    create_custom_item(

        data["name"],

        totals["calories"],
        totals["protein"],
        totals["carbs"],
        totals["fat"],
        totals["fiber"],
        totals["sugar"],
        totals["sodium"]

    )

    return jsonify({
        "success": True
    })

@app.route(

    "/delete-app-food",

    methods=["POST"]

)

def delete_app_food_route():

    data = request.get_json()

    if int(data["fdc_id"]) < 9000000:

        return jsonify({

            "success": False,

            "message": "Cannot delete built-in foods"

        }), 400

    delete_app_food(

        int(data["fdc_id"])

    )

    return jsonify({

        "success": True

    })

@app.route("/food/<int:fdc_id>")
def get_food_data(fdc_id):

    food = get_food_by_fdc_id(fdc_id)

    return jsonify({

        "fdc_id": food[0],
        "food_name": food[1],
        "calories": food[2],
        "protein": food[3],
        "carbs": food[4],
        "fat": food[5],
        "fiber": food[6],
        "sugar": food[7],
        "sodium": food[8],
        "serving_weight": food[9]

    })

@app.route(
    "/update-app-food",
    methods=["POST"]
)
def update_app_food_route():

    data = request.get_json()

    update_app_food(

        int(data["fdc_id"]),

        data["food_name"],

        float(data["calories"]),
        float(data["protein"]),
        float(data["carbs"]),
        float(data["fat"]),
        float(data["fiber"]),
        float(data["sugar"]),
        float(data["sodium"]),
        float(data["serving_weight"])

    )

    return jsonify({
        "success": True
    })


@app.route("/export-db")
def export_db():

    return send_file(
        "nutrition.db",
        as_attachment=True
    )

@app.route("/export-csv")
def export_csv():

    foods = get_food_entries()

    def generate():

        yield (
            "id,date,time_slot,food_name,"
            "quantity,unit,fdc_id,"
            "calories,protein,carbs,"
            "fat,fiber,sugar,sodium\n"
        )

        for row in foods:

            yield ",".join(
                str(value)
                for value in row
            ) + "\n"

    return Response(

        generate(),

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=nutrition.csv"
        }

    )



@app.route("/export-foods-csv")
def export_foods_csv():

    conn = sqlite3.connect("nutrition.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM app_foods
        ORDER BY food_name
    """)

    rows = cursor.fetchall()

    conn.close()

    def generate():

        yield (
            "fdc_id,food_name,calories,"
            "protein,carbs,fat,fiber,"
            "sugar,sodium,display_name,"
            "serving_weight\n"
        )

        for row in rows:

            yield ",".join(
                str(value) if value is not None else ""
                for value in row
            ) + "\n"

    return Response(

        generate(),

        mimetype="text/csv",

        headers={
            "Content-Disposition":
            "attachment; filename=app_foods.csv"
        }

    )

if __name__ == "__main__":
    app.run(debug=True)