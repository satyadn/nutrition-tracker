import sqlite3

DB_NAME = "nutrition.db"


def initialize_database():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_entries (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            entry_date TEXT NOT NULL,

            time_slot TEXT NOT NULL,

            food_name TEXT NOT NULL,

            quantity REAL NOT NULL,

            unit TEXT NOT NULL

        )
    """)

    cursor.execute("""

      CREATE TABLE IF NOT EXISTS food_master (

         id INTEGER PRIMARY KEY AUTOINCREMENT,

         food_name TEXT NOT NULL UNIQUE,

         calories REAL NOT NULL,

         protein REAL NOT NULL,

         carbs REAL NOT NULL,

         fat REAL NOT NULL,

         fiber REAL NOT NULL,

         sugar REAL NOT NULL,

         sodium REAL NOT NULL

       )

    """)

    conn.commit()
    conn.close()


def add_food_entry(
    entry_date,
    time_slot,
    food_name,
    quantity,
    unit,
    fdc_id,

    calories,

    protein,

    carbs,

    fat,

    fiber,

    sugar,

    sodium
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO food_entries
        (
            entry_date,
            time_slot,
            food_name,
            quantity,
            unit,
            fdc_id,
            calories,
            protein,
            carbs,
            fat,
            fiber,
            sugar,
            sodium
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry_date,
        time_slot,
        food_name,
        quantity,
        unit,
        fdc_id,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sugar,
        sodium
    ))

    conn.commit()
    conn.close()
    

def get_food_entries():

   conn = sqlite3.connect(DB_NAME)

   cursor = conn.cursor()

   cursor.execute("""
    SELECT
        id,
        entry_date,
        time_slot,
        food_name,
        quantity,
        unit,
        fdc_id,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sugar,
        sodium
    FROM food_entries
    """)

   rows = cursor.fetchall()

   conn.close()

   return rows


def update_food_entry(
    food_id,
    food_name,
    quantity,
    unit,
    fdc_id,
    calories,
    protein,
    carbs,
    fat,
    fiber,
    sugar,
    sodium
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE food_entries
        SET
            food_name = ?,
            quantity = ?,
            unit = ?,
            fdc_id = ?,
            calories = ?,
            protein = ?,
            carbs = ?,
            fat = ?,
            fiber = ?,
            sugar = ?,
            sodium = ?
        WHERE id = ?
    """, (
        food_name,
        quantity,
        unit,
        fdc_id,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sugar,
        sodium,
        food_id
    ))

    conn.commit()
    conn.close()


def delete_food_entry(food_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM food_entries
        WHERE id = ?
    """, (food_id,))

    conn.commit()
    conn.close()


def add_food_master(
    food_name,
    calories,
    protein,
    carbs,
    fat,
    fiber,
    sugar,
    sodium
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO food_master
        (
            food_name,
            calories,
            protein,
            carbs,
            fat,
            fiber,
            sugar,
            sodium
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        food_name,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sugar,
        sodium
    ))

    conn.commit()
    conn.close()


def get_food_master():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM food_master
        ORDER BY food_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_app_foods():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            fdc_id,
            display_name
        FROM app_foods
        ORDER BY display_name
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_food_by_fdc_id(fdc_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            fdc_id,
            food_name,
            calories,
            protein,
            carbs,
            fat,
            fiber,
            sugar,
            sodium,
            serving_weight
        FROM app_foods
        WHERE fdc_id = ?
    """, (fdc_id,))

    row = cursor.fetchone()

    conn.close()

    return row


def calculate_food_nutrition(
    fdc_id,
    quantity,
    unit
):

    # print("QUANTITY:", quantity, type(quantity))
    # print("UNIT:", unit)

    food = get_food_by_fdc_id(fdc_id)


    # print("FOOD:", food)
    # print("UNIT:", unit)
    # print("SERVING WEIGHT:", food[9])


    if not food:
        return None

    serving_weight = float(food[9] or 100)

    if unit == "count":

        grams = quantity * serving_weight

    else:

        grams = quantity
    # print("GRAMS:", grams, type(grams))
    factor = grams / 100
    # print(food)
    return {

        "calories": (food[2] or 0) * factor,
        "protein":  (food[3] or 0) * factor,
        "carbs":    (food[4] or 0) * factor,
        "fat":      (food[5] or 0) * factor,
        "fiber":    (food[6] or 0) * factor,
        "sugar":    (food[7] or 0) * factor,
        "sodium":   (food[8] or 0) * factor

    }


def get_daily_totals():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            entry_date,
            ROUND(SUM(COALESCE(calories, 0)), 1),
            ROUND(SUM(COALESCE(protein, 0)), 1),
            ROUND(SUM(COALESCE(carbs, 0)), 1),
            ROUND(SUM(COALESCE(fat, 0)), 1),
            ROUND(SUM(COALESCE(fiber, 0)), 1),
            ROUND(SUM(COALESCE(sugar, 0)), 1),
            ROUND(SUM(COALESCE(sodium, 0)), 1)
        FROM food_entries
        GROUP BY entry_date
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows



def add_custom_food(
    display_name,
    calories,
    protein,
    carbs,
    fat,
    fiber,
    sugar,
    sodium,
    serving_weight
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO app_foods
        (
            fdc_id,
            food_name,
            calories,
            protein,
            carbs,
            fat,
            fiber,
            sodium,
            sugar,
            display_name,
            serving_weight
        )

        VALUES
        (
            (
                SELECT
                    COALESCE(
                        MAX(
                            CASE
                                WHEN fdc_id >= 9000000
                                THEN fdc_id
                            END
                        ),
                        9000000
                    ) + 1
                FROM app_foods
            ),

            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )

    """, (

        display_name,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sodium,
        sugar,
        display_name,
        serving_weight

    ))

    conn.commit()
    conn.close()


def create_custom_item(
    item_name,
    calories,
    protein,
    carbs,
    fat,
    fiber,
    sugar,
    sodium
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO app_foods
        (
            fdc_id,
            food_name,
            calories,
            protein,
            carbs,
            fat,
            fiber,
            sodium,
            sugar,
            serving_weight
        )

        VALUES
        (
            (
                SELECT
                    COALESCE(
                        MAX(
                            CASE
                                WHEN fdc_id >= 9000000
                                THEN fdc_id
                            END
                        ),
                        9000000
                    ) + 1
                FROM app_foods
            ),

            ?,?,?,?,?,?,?,?,100

        )

    """, (

        item_name,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sodium,
        sugar

    ))

    conn.commit()
    conn.close()


def delete_app_food(fdc_id):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM app_foods
        WHERE fdc_id = ?
    """, (fdc_id,))

    conn.commit()
    conn.close()


def update_app_food(
    fdc_id,
    food_name,
    calories,
    protein,
    carbs,
    fat,
    fiber,
    sugar,
    sodium,
    serving_weight
):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE app_foods

        SET
            food_name = ?,
            display_name = ?,
            calories = ?,
            protein = ?,
            carbs = ?,
            fat = ?,
            fiber = ?,
            sugar = ?,
            sodium = ?,
            serving_weight = ?

        WHERE fdc_id = ?

    """, (

        food_name,
        food_name,
        calories,
        protein,
        carbs,
        fat,
        fiber,
        sugar,
        sodium,
        serving_weight,
        fdc_id

    ))

    conn.commit()
    conn.close()