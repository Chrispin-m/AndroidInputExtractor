import json
from input_extractor.field_extractor import extract_input_fields
from utils.adb_utils import get_current_app_package

def main():
    app_package = get_current_app_package()
    input_fields = extract_input_fields(app_package, 0)
    print("-------------------------------------------------------------")
    print("\033[92m" + json.dumps(input_fields[0], indent=4) + "\033[0m")
    print("-------------------------------------------------------------")
    print("\033[93m" + json.dumps(input_fields[1], indent=4) + "\033[0m")


if __name__ == "__main__":
    main()
