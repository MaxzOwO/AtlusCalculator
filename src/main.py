import fusion.fusion_engine as fusion_engine

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
    result_same_race = fusion_engine.calculate_fusion("Satanael", "Legion", demons, charts, by_race)
    result_name = fusion_engine.calculate_fusion("Unicorn", "Hell Biker", demons, charts, by_race)
    print_demon(result_same_race)
    print_demon(result_name)
    

    

    
    
main()