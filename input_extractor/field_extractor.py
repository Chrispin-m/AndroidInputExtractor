import os
import re
import json
import xml.etree.ElementTree as ET
from input_extractor.xml.xml_parser import parse_xml
from validations.country_codes import get_country_by_code
from utils.adb_utils import run_adb_command
from com.dtmilano.android.viewclient import ViewClient
import sys
from PIL import Image
import pytesseract

def gather_text(node):
    texts = [node.attrib.get('text', '')] if node.attrib.get('text', '') else []
    for child in node:
        texts.append(gather_text(child))
    return ', '.join(texts)

def gather_rid(node):
    rids = [node.attrib.get('resource-id', '')] if node.attrib.get('resource-id', '') else []
    for child in node:
        rids.append(gather_rid(child))
    return ', '.join(rids)

def gather_content(node):
    contents = [node.attrib.get('content-desc', '')] if node.attrib.get('content-desc', '') else []
    for child in node:
        contents.append(gather_content(child))
    return ', '.join(contents)

def process_node(node, index=""):
    result = []
    if node.attrib.get('clickable', 'false') == 'true':
        label = gather_text(node)
        if not label:
            label = gather_content(node)
        resource_id = gather_rid(node)
        result.append({
            'label': label,
            'resource_id': resource_id,
            'xy/bounds': node.attrib.get('bounds', ''),
            'index': index
        })
    for i, child in enumerate(node):
        result.extend(process_node(child, f"{index}[{i}]"))
    return result
def extract_input_fields(app_package, recurs):

    dump_command = f"adb shell uiautomator dump /sdcard/{app_package}.xml"
    run_adb_command(dump_command)

    try:
        pull_command = f"adb pull /sdcard/{app_package}.xml input_extractor/xml/xml_dumps"

        run_adb_command(pull_command)
    except Exception as e:
        print(f"ERROR: {e}")
        pull_command = f"adb pull /sdcard/handled_idle_state.xml input_extractor/xml/xml_dumps"
        run_adb_command(pull_command)

    root = parse_xml(f"input_extractor/xml/xml_dumps/{app_package}.xml")
    package=root[0].get('package')
    print(package)
    url_pattern = re.compile(r'\bhttps?://\S+\b')

    classified_input_fields = []
    unclassified_input_fields = []

    for element in root.iter():
        field_type = ""
        label = ""
        resource_id = ""
        validations = []
        interactive = False
        bounds = element.attrib.get("bounds")
        #print(bounds)
        
        # Further split each part by comma to get individual coordinates
        try:
            bounds2 = bounds.strip('[]').split('][')
            #print(bounds2)
            left, top = map(int, bounds2[0].split(','))
            right, bottom = map(int, bounds2[1].split(','))
        except:
            bounds2="None"

        if element.attrib.get('clickable', 'false') == 'true':
            label = gather_text(element)
            if not label:
                label = gather_content(element)
            resource_id = gather_rid(element)
            interactive = True
            class_id = element.attrib.get('class')

            if element.attrib.get('class') == "android.widget.EditText":
                if element.attrib.get('password') == "true" or "password" in resource_id:
                    field_type = "password"
                    if label == "":
                        label = "Password"
                    validations = ["min_length:6", "max_length:20", "contains_uppercase", "contains_lowercase", "contains_number", "contains_special_character"]
                elif "textEmailAddress" in resource_id:
                    field_type = "email"
                    validations = ["email_format"]
                elif "dialer" in resource_id:
                    field_type = "digits"
                    validations = ["phone_number", "USSD_code"]
                elif "digit" in label:
                    field_type = "digit"
                    validations = ["valid", "single digit"]
                elif "MM/YY" in label:
                    field_type = "date"
                    validations = ["date_format"]
                else:
                    #print("mm")
                    field_type = "text input"
                    validations = ["min_length:1", "max_length:4096"]
                    if label =="":
                        device, serialno = ViewClient.connectToDeviceOrExit()
                        filename = "temp/screenco.png"
                        device.takeSnapshot(box=(left, top, right, bottom)).save(filename, 'PNG')
                        image = Image.open(filename)

                        # Performs OCR on the image using pytesseract
                        text = pytesseract.image_to_string(image).lower()
                        print(text)
                        label=text
                        if ("number" or "phone") and "email" in label:
                            field_type = "email/phone_number"
                            validations = ["phone_number", "email_format"]
                        elif "email" in label:
                            field_type = "email"
                            validations = ["email_format"]
                        elif "password" in label:
                            field_type = "password"
                            validations = ["min_length:6", "max_length:20", "contains_uppercase", "contains_lowercase", "contains_number", "contains_special_character"]
                        elif "%" in label:
                           field_type = "percentage"
                           validations = ["1-100%"]
                        elif "amount" in label:
                            field_type = "currency"

                        try:
                            if element.attrib.get('NAF')=='true' and label=="":
                                label += "userdetails"
                                field_type = "username/email/phone_number"
                                validations = ["Valid user detail"]
                        except:
                            NAF = False
                    if "url" in resource_id:
                        field_type = "url input"
                        validations = "url_format"

            elif element.attrib.get('class') == "android.widget.AutoCompleteTextView":
                if "MM/YY" in label:
                    field_type = "date"
                    validations = ["date_format"]
                else:
                    #print("yy")
                    field_type = "text input"
                    validations = ["min_length:1", "max_length:4096"]

            elif element.attrib.get('class') == "android.widget.Spinner":
                field_type = "select"
                validations = ["multiselect", "single_select"]

            elif element.attrib.get('class') == "android.widget.ImageView":
                if "uploadPhoto" in resource_id:
                    field_type = "file"
                    validations = ["file_size", "file_format", "file_quality"]
                    if not label:
                        label = "Upload Photo"
                else:
                    if "search" in resource_id and "voice" in resource_id:
                        field_type = "ViewGroup"
                    elif "add_cc_bcc" in resource_id:
                        field_type = 'email'
                        validations = ["email_format"]

                    else:
                        field_type = "image"

            elif element.attrib.get('class') == "android.widget.TextView":
                if element.attrib.get('clickable') == "true":
                    field_type = "ViewGroup"
                else:
                    field_type = "display text"

            elif element.attrib.get('class') == "android.widget.CheckBox":
                field_type = "checkbox"
                validations = ["multicheck", "single_check"]

            elif element.attrib.get('class') == "android.widget.RadioButton":
                field_type = "radio button"

            elif element.attrib.get('class') == "android.widget.DatePicker":
                field_type = "date"
                validations = ["date_format"]

            elif element.attrib.get('class') == "android.widget.TimePicker":
                field_type = "time"
                validations = ["time_format"]

            elif element.attrib.get('class') == "android.widget.SeekBar":
                field_type = "slider"

            elif element.attrib.get('class') == "android.widget.Button":
                field_type = "button"
                validations = ["active"]

            elif element.attrib.get('class') == "android.widget.Switch":
                field_type = "switch"
                validations = ["active"]

            elif element.attrib.get('class') == "android.view.ViewGroup":
                field_type = "ViewGroup"

            elif "button" in resource_id:
                field_type = "button"
                validations = ["active"]

            elif "search" in resource_id:
                if "voice" in label.lower() or "camera" in label.lower():
                    field_type = "ViewGroup"
                else:
                    field_type = "text input"
                    validations = ["min_length:1", "max_length:4096"]

            elif field_type == "" and url_pattern.search(label):
                field_type = "HyperLink"

            elif "Layout" in element.attrib.get('class'):
                field_type = "ViewGroup"
            elif "Button" in class_id:
                field_type = "button"
                validations = ["active"]
            elif class_id == "android.view.View":
                if element.attrib.get('checkable')=='true':
                    field_type = "switch"
                    label += "On/Off"
                else:
                    field_type = "ViewGroup"
            elif element.attrib.get("checkable") == "true":
                field_type = "checkbox"
                validations = ["multicheck", "single_check"]
            elif label == "":
                device, serialno = ViewClient.connectToDeviceOrExit()
                filename = "temp/screenco.png"
                device.takeSnapshot(box=(left, top, right, bottom)).save(filename, 'PNG')
                image = Image.open(filename)

                # Performs OCR on the image using pytesseract
                text = pytesseract.image_to_string(image).lower()
                print(text)
                label=text       

            input_field = {"label": label, "type": field_type, "interactive": interactive, "resource-id": resource_id, "validations": validations, "xy/bounds": bounds}

            if field_type == "":
                unclassified_input_fields.append(input_field)
            else:
                classified_input_fields.append(input_field)
    
    if (recurs<1) and (not classified_input_fields or "chrome" in package or "browser" in package):
        extract_input_fields(app_package, 1)
    return classified_input_fields, unclassified_input_fields