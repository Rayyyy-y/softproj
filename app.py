from flask import Flask, render_template,jsonify
import mysql.connector

app = Flask(__name__)

# 配置数据库连接
db_config = {
    'user': 'root',
    'password': '598969Rr',
    'host': 'localhost',
    'database': 'softproj'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查询鱼的种类和数量
    fish_query = "SELECT species, COUNT(*) AS count FROM fish GROUP BY species"
    cursor.execute(fish_query)
    fish_data = cursor.fetchall()
    
    # 查询天气信息
    weather_query = "SELECT avg(浊度) as 浊度, avg(水温) as 水温, avg(pH) as pH, avg(溶解氧) as 溶解氧 FROM invironment"
    cursor.execute(weather_query)
    weather_data = cursor.fetchone()
    
    water_query = "SELECT AVG(电导率) AS 电导率, AVG(高锰酸盐指数) AS 高锰酸盐指数,  AVG(总氮) AS 总氮 FROM invironment GROUP BY 断面名称"
    cursor.execute(water_query)
    water_data = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # 处理数据
    species = [row[0] for row in fish_data]
    count = [row[1] for row in fish_data]
    
    weather = {
        'temperature': weather_data[0],
        'humidity': weather_data[1],
        'wind_speed': weather_data[2],
        'precipitation': weather_data[3]
    }

    water = [
        {'name': '电导率', 'type': 'line', 'data': [row[0] for row in water_data]},
        {'name': '高锰酸盐指数', 'type': 'line', 'data': [row[1] for row in water_data]},
        {'name': '总氮', 'type': 'line', 'data': [row[2] for row in water_data]}
    ]
    
    return render_template('index.html', species=species, count=count, weather=weather,water=water)

if __name__ == '__main__':
    app.run(debug=True)