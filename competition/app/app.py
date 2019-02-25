from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '{"status":0,"msg":"success","data":{"game_game_array":[{"game_game_name":"First Match","game_game_id":1,"count_down_time":1550986308,"game_disk_array":[{"game_disk_id":11,"game_disk_name":"1_1","game_disk_result":9},{"game_disk_id":12,"game_disk_name":"1_2","game_disk_result":9}]},{"game_game_name":"Second Match","game_game_id":2,"count_down_time":1550986308,"game_disk_array":[{"game_disk_id":13,"game_disk_name":"2_1","game_disk_result":9},{"game_disk_id":14,"game_disk_name":"2_2","game_disk_result":9}]},{"game_game_name":"Third Match","game_game_id":3,"count_down_time":1550986308,"game_disk_array":[{"game_disk_id":15,"game_disk_name":"3_1","game_disk_result":9}]}]}}'

if __name__ == '__main__':
    app.run(debug=True)
