import json
from xml_parser import parse_all_xml


def generate_report(directory_path, output_file):
    report_data = parse_all_xml(directory_path)

    # Write the parsed data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(report_data, json_file, indent=4)

    print(f"Report successfully generated at {output_file}")


if __name__ == "__main__":
    # Example: generate JSON report from the 'data/' folder and save it in 'report/report_data.json'
    generate_report('./report_generator/data', './report/report_data.json')
