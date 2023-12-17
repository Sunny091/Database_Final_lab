from flask import Flask, render_template, request, jsonify
import mysql.connector
import csv
import io

location_dist = {
    "Tanzi": "潭子區",
    "West": "西區",
    "Longjing": "龍井區",
    "Dali": "大里區",
    "Wuri": "烏日區",
    "Kamioka": "神岡區",
    "North": "北區",
    "Beitun": "北屯區",
    "Nantun": "南屯區",
    "Xinshe": "新社區",
    "Dadu": "大肚區",
    "Dongshi": "東勢區",
    "Shalu": "沙鹿區",
    "Taiping": "太平區",
    "Wuqi": "梧棲區",
    "Xitun": "西屯區",
    "Qingshui": "清水區",
    "Shigang": "石岡區",
    "East": "東區",
    "Daya": "大雅區",
    "South": "南區",
    "Waipu": "外埔區",
    "Fengyuan": "豐原區",
    "Central": "中區",
    "Houli": "后里區",
    "Wufeng": "霧峰區",
    "Dajia": "大甲區",
    "Da'an": "大安區",
    "Heping": "和平區",
}


# from gevent import pywsgi

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("test.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # 哪個區交通事故最頻繁(排序)
        if request.form.get("choice") == "1":
            quary = """
                SELECT District, COUNT(*) AS Accident_Count
                FROM Location
                GROUP BY District
                ORDER BY Accident_Count DESC;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["區", "次數"])
            for row in result:
                row = list(row)
                if row[0] in location_dist.keys():
                    row[0] = location_dist.get(row[0])
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x2).html", data=csv_data_list)

        # 交通事故的肇事因素(排序)
        elif request.form.get("choice") == "2":
            quary = """
                SELECT Causing_factor, COUNT(*) AS Factor_Count
                FROM accident
                GROUP BY Causing_factor
                ORDER BY Factor_Count DESC
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["因素", "次數"])
            for row in result:
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x2).html", data=csv_data_list)

        # 哪個時段最容易發生交通事故
        elif request.form.get("choice") == "3":
            quary = """
                SELECT Hour, COUNT(*) AS Accident_Count
                FROM time
                GROUP BY Hour
                ORDER BY Accident_Count DESC;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["時間", "次數"])
            for row in result:
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x2).html", data=csv_data_list)

        # 保護裝備和主要傷處之間的關聯
        elif request.form.get("choice") == "4":
            quary = """
                WITH ProtectiveEquipMainInjuryCounts AS (
                    SELECT
                        s.Protective_equipement,
                        a.Main_injury,
                        COUNT(*) AS InjuryCount
                    FROM state s
                    INNER JOIN accident a ON s.Accident_index = a.Accident_index
                    GROUP BY s.Protective_equipement, a.Main_injury
                ),
                RankedInjuriesByEquip AS (
                    SELECT
                        Protective_equipement,
                        Main_injury,
                        InjuryCount,
                        RANK() OVER (PARTITION BY Protective_equipement ORDER BY InjuryCount DESC) AS InjuryRank
                    FROM ProtectiveEquipMainInjuryCounts
                )
                SELECT
                    Protective_equipement,
                    Main_injury,
                    InjuryCount
                FROM RankedInjuriesByEquip
                WHERE InjuryRank <= 5
                ORDER BY Protective_equipement, InjuryRank;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["保護裝備", "主要傷處", "次數"])
            for row in result:
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x3).html", data=csv_data_list)

        # 飲酒程度和受傷程度的關聯
        elif request.form.get("choice") == "5":
            quary = """
                SELECT
                    s.Drinking_situation,
                    SUM(a.Injury_num) AS Total_Injuries,
                    SUM(a.Death_num) AS Total_Deaths
                FROM state s
                JOIN accident a ON s.Accident_index = a.Accident_index
                GROUP BY s.Drinking_situation;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["飲酒程度", "受傷＋死亡（人數）"])
            for row in result:
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x2).html", data=csv_data_list)

        # 天候和地點的關聯
        elif request.form.get("choice") == "6":
            quary = """
                WITH ClimateDistrictCounts AS (
                    SELECT
                        s.Climate,
                        l.District,
                        COUNT(*) AS DistrictCount
                    FROM state s
                    INNER JOIN location l ON s.Accident_index = l.Accident_index
                    GROUP BY s.Climate, l.District
                ),
                RankedDistrictsByClimate AS (
                    SELECT
                        Climate,
                        District,
                        DistrictCount,
                        RANK() OVER (PARTITION BY Climate ORDER BY DistrictCount DESC) AS DistrictRank
                    FROM ClimateDistrictCounts
                )
                SELECT
                    Climate,
                    District,
                    DistrictCount
                FROM RankedDistrictsByClimate
                WHERE DistrictRank <= 10
                ORDER BY Climate, DistrictRank;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["天候", "區", "次數"])
            for row in result:
                row = list(row)
                if row[1] in location_dist.keys():
                    row[1] = location_dist.get(row[1])
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x3).html", data=csv_data_list)

        # 哪裡容易因路面不平而造成車禍
        elif request.form.get("choice") == "7":
            quary = """
                SELECT l.District, COUNT(CASE WHEN r.Road_defect = 1 THEN 1 END) AS Road_defect_1_Count,
                    COUNT(CASE WHEN r.Road_defect = 2 THEN 1 END) AS Road_defect_2_Count,
                    COUNT(CASE WHEN r.Road_defect = 3 THEN 1 END) AS Road_defect_3_Count
                FROM location l
                JOIN road r ON l.Accident_index = r.Accident_index
                GROUP BY l.District
                ORDER BY l.District
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["區", "路面鬆軟（次數）", "隆起或凹陷不平（次數）", "有坑洞（次數）"])
            for row in result:
                row = list(row)
                if row[0] in location_dist.keys():
                    row[0] = location_dist.get(row[0])
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x4).html", data=csv_data_list)

        # 時間和主要肇因的關聯
        elif request.form.get("choice") == "8":
            quary = """
                -- 使用視圖和資料表連接，計算每個時段的肇因排名
                WITH RankedCausingFactors AS (
                    SELECT
                        t.Period,
                        a.Causing_factor,
                        COUNT(*) AS FactorCount
                    FROM TimePeriod t
                    INNER JOIN accident a ON t.Accident_index = a.Accident_index
                    GROUP BY t.Period, a.Causing_factor
                ),
                RankedFactorsByPeriod AS (
                    SELECT
                        Period,
                        Causing_factor,
                        FactorCount,
                        RANK() OVER (PARTITION BY Period ORDER BY FactorCount DESC) AS FactorRank
                    FROM RankedCausingFactors
                )
                SELECT
                    Period,
                    Causing_factor,
                    FactorCount
                FROM RankedFactorsByPeriod
                WHERE FactorRank <= 10
                ORDER BY Period, FactorRank;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["時間", "肇因"])
            for row in result:
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x2).html", data=csv_data_list)

        # 計算各區因酒駕肇事的排名
        elif request.form.get("choice") == "9":
            quary = """
                SELECT l.District, COUNT(s.Drinking_situation) AS Frequency
                FROM location l
                JOIN state s ON l.Accident_index = s.Accident_index
                WHERE s.Drinking_situation BETWEEN 4 AND 8
                GROUP BY l.District
                ORDER BY COUNT(s.Drinking_situation) DESC;
            """
            cursor.execute(quary)
            result = cursor.fetchall()
            answer = []
            answer.append(["區", "次數"])
            for row in result:
                row = list(row)
                if row[0] in location_dist.keys():
                    row[0] = location_dist.get(row[0])
                answer.append(row)
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            return render_template("answer(x2).html", data=csv_data_list)

        # 用身分證或車牌查詢事故的相關資訊
        elif request.form.get("personID") and request.form.get("carID"):
            persionID = request.form.get("personID")
            carID = request.form.get("carID")
            quary = """
                SELECT *
                FROM all_info
                WHERE License_num = %s AND ID_card = %s;
            """
            cursor.execute(quary, (carID, persionID))
            result = cursor.fetchall()
            split_result = []
            for item in result[0]:
                if isinstance(item, int):
                    split_result.append(str(item))
                else:
                    split_result.append(item)
            end_result = []
            for row in split_result:
                if row in location_dist.keys():
                    row = location_dist.get(row)
                end_result.append(row)
            title = [
                "Accident_index",
                "Year",
                "Month",
                "Day",
                "Hour",
                "Minute",
                "District",
                "Death_num",
                "Injury_num",
                "Climate",
                "Light",
                "Road_category",
                "Speed_limit",
                "Road_type",
                "Accident_location",
                "Pavement",
                "Road_conditon",
                "Road_defect",
                "Barrier",
                "Sight_distance",
                "Signal_type",
                "Signal_action",
                "Accident_type",
                "Causing_factory",
                "Injury_degree",
                "Main_injury",
                "Protective_equipement",
                "Action_status",
                "Driving_qualifications",
                "Driving_type",
                "Drinking_situation",
                "Impact_site",
                "Run_away",
                "Job",
                "GPS_X",
                "GPS_Y",
                "License_num",
                "ID_card",
                "Car_type",
                "Timestamp",
            ]
            combined = [[x, y] for x, y in zip(title, end_result)]
            return render_template("answer(search).html", data=combined)
        return (
            render_template("answer(no choice).html")
            + '<html> <body> <div style="text-align:center"> *show the accident info* </div></body></html>'
        )
        # return render_template('test.html') + request.form.get('personID') + "----" + request.form.get('carID')
    return render_template("test.html")


@app.route("/reset", methods=["GET", "POST"])
def reset():
    if request.method == "POST":
        return render_template("test.html")


if __name__ == "__main__":
    # connet mysql server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ss890919",
        database="lab",
    )
    cursor = conn.cursor()

    app.run(debug=True)
