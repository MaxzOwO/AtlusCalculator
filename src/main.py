import fusion.fusion_engine as fusion_engine
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




@app.route('/api/fuse', methods=['POST'])
def fuse():
    print("start fuse")
    data = request.json
    race1 = data.get('race1')
    race2 = data.get('race2')
    name1 = data.get('name1')
    name2 = data.get('name2')

    demons = fusion_engine.load_demon_data("p5r")
    by_race = fusion_engine.list_demons_by_race(demons)
    charts = fusion_engine.load_fusion_chart_data("p5r")

    result_race = fusion_engine.calculate_fusion(race1, race2, demons, charts, by_race)
    result_name = fusion_engine.calculate_fusion(name1, name2, demons, charts, by_race)

    def format_demon(name):
        demon = demons[name]
        return {
            "name": name,
            "race": demon["race"],
            "lvl": demon["lvl"],
            "inherits": demon["inherits"],
            "trait": demon["trait"],
            "item": demon["item"],
            "itemr": demon["itemr"],
            "stats": demon["stats"],
            "resists": demon["resists"],
            "skills": demon["skills"]
        }

    return jsonify({
        "fusion_by_race": format_demon(result_race),
        "fusion_by_name": format_demon(result_name)
    })

if __name__ == '__main__':
    app.run(port=5000)


def get_user_input(prompt="输入两个字符串，用,分隔："):
    while True:
        try:
            a,b=map(str, input(prompt).split(","))
            return a,b
        except ValueError:
            print("无效输入，请重新输入")


def print_demon(result_name):
    demons = fusion_engine.load_demon_data("p5r")
    demon = demons[result_name]
    print(f"=== {result_name} ===")
    print(f"Race: {demon['race']}")
    print(f"Level: {demon['lvl']}")
    print(f"Inherits: {demon['inherits']}")
    print(f"Trait: {demon['trait']}")
    print(f"Item (normal): {demon['item']}")
    print(f"Item (rare): {demon['itemr']}")
    print(f"Stats: {demon['stats']}")
    print(f"Resists: {demon['resists']}")

    print("Skills:")
    for skill, value in demon['skills'].items():
        print(f"  - {skill}: {value}")

def main():
    demons = fusion_engine.load_demon_data("p5r")
    by_race = fusion_engine.list_demons_by_race(demons)
    charts = fusion_engine.load_fusion_chart_data("p5r")
    # print(by_race)
    # for race, names in by_race.items():
    #    print(f"{race} ({len(names)} demons): {names}")
        
    #  print("\nFusion charts:")
    # print(charts)
    race1,race2=get_user_input("输入race: ,分隔 ")
    name1,name2=get_user_input("输入name: ,分隔 ")
    result_same_race = fusion_engine.calculate_fusion(race1, race2, demons, charts, by_race)
    result_name = fusion_engine.calculate_fusion(name1, name2, demons, charts, by_race)


    #result_same_race = fusion_engine.calculate_fusion("Satanael", "Legion", demons, charts, by_race)
    #result_name = fusion_engine.calculate_fusion("Unicorn", "Hell Biker", demons, charts, by_race)
    print_demon(result_same_race)
    print_demon(result_name)
    

    

    
    
#main()