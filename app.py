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
climat_dist = {
    "1": "風",
    "2": "風沙",
    "3": "霧或煙",
    "4": "雪",
    "5": "雨",
    "6": "陰",
    "6": "晴",
}
light_dist = {
    "1": "有照明且開啟",
    "2": "有照明未開啟或故障",
    "3": "無照明",
}
road_category_dist = {
    "1": "國道",
    "2": "省道",
    "3": "快速(公)道路",
    "4": "縣道",
    "5": "鄉道",
    "6": "市區道路",
    "7": "村里道路",
    "8": "專用道路",
    "9": "其他",
}
road_type_dist = {
    "1": "有遮斷器",
    "2": "無遮斷器",
    "3": "三岔路",
    "4": "四岔路",
    "5": "多岔路",
    "6": "隧道",
    "7": "地下道",
    "8": "橋樑",
    "9": "涵洞",
    "10": "高架道路",
    "11": "彎曲路及附近",
    "12": "坡路",
    "13": "直路",
    "14": "圓環",
    "15": "廣場",
    "16": "休息站或服務區",
    "17": "輕軌共用道路",
    "18": "其他",
}
accident_location_dist = {
    "1": "交岔路口內",
    "2": "交岔路口附近",
    "3": "機慢車待轉區",
    "4": "機慢車停等區",
    "5": "交通島(含槽化線)",
    "6": "迴轉道",
    "7": "快車道",
    "8": "慢車道",
    "9": "一般車道(未劃分快慢車道)",
    "10": "公車專用道",
    "11": "機車專用道",
    "12": "機車優先道",
    "13": "自行車專用道",
    "14": "路肩、路緣",
    "15": "加速車道",
    "16": "減速車道",
    "17": "直線閘道",
    "18": "環線閘道",
    "19": "行人穿越道",
    "20": "行人穿越道附近",
    "21": "人行道",
    "22": "人行道標線",
    "23": "騎樓",
    "24": "其他",
}
pavemet_dist = {
    "1": "柏油",
    "2": "水泥",
    "3": "碎石",
    "4": "其他鋪裝",
    "5": "無鋪裝",
}
road_condition_dist = {
    "1": "冰雪",
    "2": "油滑",
    "3": "泥濘",
    "4": "濕潤",
    "5": "乾燥",
}
road_defect_dist = {
    "1": "路面鬆軟",
    "2": "隆起或凹陷不平",
    "3": "有坑洞",
    "4": "無缺陷",
}
barrier_dist = {
    "1": "道路工事(程)中",
    "2": "有堆積物",
    "3": "路上有停車",
    "4": "攤位、棚架",
    "5": "其他障礙物",
    "6": "無障礙物",
}
sight_distance_dist = {
    "1": "建築物",
    "2": "樹木、農作物",
    "3": "路上停放車輛",
    "4": "施工圍籬",
    "5": "其他",
    "6": "良好",
}
signal_type_dist = {
    "1": "行車管制號誌",
    "2": "行車管制號誌(附設行人專用號誌)",
    "3": "閃光號誌",
    "4": "無號誌",
}
signal_action_dist = {
    "1": "正常",
    "2": "不正常",
    "3": "無動作",
    "4": "無號誌",
}
accident_type_dist = {
    "1": "對向通行中(人與車)",
    "2": "同向通行中(人與車)",
    "3": "穿越道路中(人與車)",
    "4": "在路上嬉戲(人與車)",
    "5": "在路上作業中(人與車)",
    "6": "衝進路中(人與車)",
    "7": "從停車後(或中)穿出(人與車)",
    "8": "佇立在路邊(外)(人與車)",
    "9": "其他(人與車)",
    "10": "對撞(車與車)",
    "11": "對向擦撞(車與車)",
    "12": "同向擦撞(車與車)",
    "13": "追撞(車與車)",
    "14": "倒車撞(車與車)",
    "15": "路口交叉撞(車與車)",
    "16": "側撞(車與車)",
    "17": "其他(車與車)",
    "18": "路上翻車、摔倒(車輛本身)",
    "19": "衝出路外(車輛本身)",
    "20": "撞護欄(樁)(車輛本身)",
    "21": "撞號誌、標誌桿(車輛本身)",
    "22": "撞橋樑(橋墩)(車輛本身)",
    "23": "撞交通島(車輛本身)",
    "24": "撞非固定設施(車輛本身)",
    "25": "撞建築物(車輛本身)",
    "26": "撞路樹(車輛本身)",
    "27": "撞電桿(車輛本身)",
    "28": "撞動物(車輛本身)",
    "29": "撞工程施工(車輛本身)",
    "30": "其他(車輛本身)",
    "31": "衝過(或撞壞)遮斷器(平交道事故)",
    "32": "正越過平交道中(平交道事故)",
    "33": "暫停位置不當(平交道事故)",
    "34": "在平交道內無法行動(平交道事故)",
    "35": "其他(平交道事故)",
}
causing_factor_dist = {
    "1": "違規超車",
    "2": "爭(搶)道行駛",
    "3": "危險駕駛",
    "4": "逆向行駛",
    "5": "超速駕駛",
    "6": "未依規定減速",
    "7": "未保持行車安全距離",
    "8": "未保持行車安全間隔",
    "9": "未遵守依法令授權交通指揮人員之指揮",
    "10": "車輛未依規定暫停讓行人先行",
    "11": "有號誌路口，轉彎車未讓直行車先行",
    "12": "無號誌路口，支線道未讓幹線道先行",
    "13": "無號誌路口，少線道未讓多線道先行",
    "14": "無號誌路口，轉彎車未讓直行車先行",
    "15": "無號誌路口，左方車未讓右方車先行",
    "16": "山路會車，靠山壁車未讓外緣車先行",
    "17": "峻狹坡路會車，下坡車未讓上坡車先行",
    "18": "行經圓環未依規定讓車",
    "19": "未依規定避讓(併駛、超車)消防、救護、警備、工程救險車、毒性化學物質災害事故應變車等執行緊急任務車",
    "20": "其他未依規定讓車",
    "21": "闖紅燈直行",
    "22": "闖紅東右轉",
    "23": "闖紅燈左轉(或迴轉)",
    "24": "違反閃光號誌",
    "25": "違反其他號誌",
    "26": "違反遵行方向標誌(線)",
    "27": "違反車輛專用標誌(線)",
    "28": "違反行人專用標誌(線)",
    "29": "違反禁止進入標誌",
    "30": "違反禁止各種車輛進入標誌",
    "31": "違反禁止會車標誌",
    "32": "違反禁止回轉或迴車標誌",
    "33": "違反車輛改道逼照",
    "34": "違反禁止超車標誌(線)",
    "35": "違反禁止變換車道標線",
    "36": "違反二段式左(右)轉標誌(線)",
    "37": "違反進行車種標誌(字)",
    "38": "違反禁止左轉、又轉標誌",
    "39": "違反其他標誌(線)禁制",
    "40": "變換車道不當",
    "41": "未靠右行駛",
    "42": "方向不定(不包括危險駕車)",
    "43": "閃避不當(慎)",
    "44": "多車道迴轉，為先駛入內側車道",
    "45": "迴轉未依規定",
    "46": "橫越道路不慎",
    "47": "右轉彎未依規定",
    "48": "左彎未依規定",
    "49": "倒車未依規定",
    "50": "停車操作時未注意安全",
    "51": "起步時未注意安全",
    "52": "吸食違禁物駕駛",
    "53": "酒醉(後)駕駛",
    "54": "患病或服用藥物(疲勞)駕駛",
    "55": "打瞌睡或疲勞駕駛(包括連續駕駛8小時)",
    "56": "飲食、抽(點)煙、拿(撿)物品分心駕駛",
    "57": "乘客、車上動(生)物干擾分心駕駛",
    "58": "觀看其他事故、活動、道路環境或車外資訊分心駕駛",
    "59": "恍神、緊張、心不在焉分心駕駛",
    "60": "使用車輛自動駕駛或先進駕駛輔助系統設備(裝置)不符規定",
    "61": "操作、觀看行車輔助或娛樂性顯示設備",
    "62": "使用手持行動電話",
    "63": "搶(闖)越平交道",
    "64": "未保持平交道淨空",
    "65": "未依規定使用燈光",
    "66": "暗處停車無燈光、標識",
    "67": "夜間行駛無燈光設備",
    "68": "裝載貨物不穩妥",
    "69": "載運貨物超重",
    "70": "超載人員",
    "71": "載運貨物超長、寬、高",
    "72": "裝卸貨物不當",
    "73": "裝載未盡安全措施",
    "74": "未待乘客安全上下而開車",
    "75": "其他裝載不當",
    "76": "開啟或關閉車門不當",
    "77": "違規(臨時)停車",
    "78": "車輛為停妥滑動致生事故",
    "79": "車輛拋錨未採安全措施",
    "80": "發生事故後，未採取安全措施",
    "81": "被車輛輾壓之不明物體彈飛",
    "82": "車輛或機械操作不當(慎)",
    "83": "因光線、視線遮蔽致生事故",
    "84": "其他不當駕車行為",
    "85": "相關跡證不足且無具體影像畫面，當事人各執一詞，經分析後無法釐清肇事原因",
    "86": "肇事逃逸未查獲，無法查明肇因",
    "87": "尚未發現肇事因素",
    "88": "煞車失靈或故障",
    "89": "方向操縱系統故障",
    "90": "車輪脫落或輪胎爆裂",
    "91": "車輛零件脫落",
    "92": "燈光系統故障",
    "93": "車輛附屬機具未盡安全措施",
    "94": "其他機件失靈或故障",
    "95": "未依標誌或標線穿越道路",
    "96": "未依號誌或手勢指揮(示)穿越道路",
    "97": "未依規定行有地下道、天橋穿越道路",
    "98": "穿越道路未注意左右來車",
    "99": "在道路上嬉戲或奔走不定",
    "100": "搶(闖)越平交道",
    "101": "事故發生時當事者逕自離開現場",
    "102": "開啟或關閉車門不當",
    "103": "頭手伸出窗外",
    "104": "乘坐不當(慎)",
    "105": "未待車輛停妥而上下車",
    "106": "上下車輛時未注意安全",
    "107": "在道路上工作未設適當標識",
    "108": "指揮不當(包括未依法令授權)",
    "109": "其他引起事故之疏失或行為",
    "110": "平交道看守疏失或未放柵欄",
    "111": "路況危險無安全(警告)設施",
    "112": "施工安全防護措施未依規定或未盡完善(備)",
    "113": "交通管制設施失靈或損毀",
    "114": "其他交通管制不當",
    "115": "道路設施(備)、植栽或其他裝置，倒塌或掉(斷)落",
    "116": "物品(件)滾(滑行)或飛(掉)落",
    "117": "強風、暴雨、濃霧(煙)",
    "118": "動物竄出",
    "119": "尚未發現肇事因素",
}
injury_degree_dist = {
    "1": "24小時內死亡",
    "2": "受傷",
    "3": "未受傷",
    "4": "不明",
    "5": "2-30日內死亡",
}


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("test.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # 哪個區交通事故最頻繁(排序)
        if request.form.get("choice") == "1":
            # 輸入quary進行資料庫查詢
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
                # 把區的英文名字轉成中文
                if row[0] in location_dist.keys():
                    row[0] = location_dist.get(row[0])
                answer.append(row)
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x2)顯示
            return render_template("answer(x2).html", data=csv_data_list)

        # 交通事故的肇事因素(排序)
        elif request.form.get("choice") == "2":
            # 輸入quary進行資料庫查詢
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
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x2)顯示
            return render_template("answer(x2).html", data=csv_data_list)

        # 哪個時段最容易發生交通事故
        elif request.form.get("choice") == "3":
            # 輸入quary進行資料庫查詢
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
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x2)顯示
            return render_template("answer(x2).html", data=csv_data_list)

        # 保護裝備和主要傷處之間的關聯
        elif request.form.get("choice") == "4":
            # 輸入quary進行資料庫查詢
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
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x3)顯示
            return render_template("answer(x3).html", data=csv_data_list)

        # 飲酒程度和受傷程度的關聯
        elif request.form.get("choice") == "5":
            # 輸入quary進行資料庫查詢
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
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x2)顯示
            return render_template("answer(x2).html", data=csv_data_list)

        # 天候和地點的關聯
        elif request.form.get("choice") == "6":
            # 輸入quary進行資料庫查詢
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
                # 把區的英文名字轉成中文
                if row[1] in location_dist.keys():
                    row[1] = location_dist.get(row[1])
                answer.append(row)
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x3)顯示
            return render_template("answer(x3).html", data=csv_data_list)

        # 哪裡容易因路面不平而造成車禍
        elif request.form.get("choice") == "7":
            # 輸入quary進行資料庫查詢
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
                # 把區的英文名字轉成中文
                if row[0] in location_dist.keys():
                    row[0] = location_dist.get(row[0])
                answer.append(row)
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x4)顯示
            return render_template("answer(x4).html", data=csv_data_list)

        # 時間和主要肇因的關聯
        elif request.form.get("choice") == "8":
            # 輸入quary進行資料庫查詢
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
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x2)顯示
            return render_template("answer(x2).html", data=csv_data_list)

        # 計算各區因酒駕肇事的排名
        elif request.form.get("choice") == "9":
            # 輸入quary進行資料庫查詢
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
                # 把區的英文名字轉成中文
                if row[0] in location_dist.keys():
                    row[0] = location_dist.get(row[0])
                answer.append(row)
            # 將結果轉成csv格式
            csv_buffer = io.StringIO()
            csv_writer = csv.writer(csv_buffer, delimiter=",", quotechar="'")
            for row in answer:
                csv_writer.writerow(row)
            csv_data = csv_buffer.getvalue()
            csv_data_list = [line.split(",") for line in csv_data.split("\n") if line]
            # 將結果回傳前端，用answer(x2)顯示
            return render_template("answer(x2).html", data=csv_data_list)

        # 用身分證或車牌查詢事故的相關資訊
        elif request.form.get("personID") and request.form.get("carID"):
            # 讀取前端的輸入
            persionID = request.form.get("personID")
            carID = request.form.get("carID")
            # 輸入quary進行資料庫查詢
            quary = """
                SELECT *
                FROM all_info
                WHERE License_num = %s AND ID_card = %s;
            """
            cursor.execute(quary, (carID, persionID))
            result = cursor.fetchall()
            split_result = []
            # 資料格式轉換
            for item in result[0]:
                if isinstance(item, int):
                    split_result.append(str(item))
                else:
                    split_result.append(item)
            end_result = []
            for row in split_result:
                # 把區的英文名字轉成中文
                if row in location_dist.keys():
                    row = location_dist.get(row)
                end_result.append(row)
            # 加入各資訊title
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
            # 將結果回傳前端，用answer(search)顯示
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
