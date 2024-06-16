# Input Field Extractor

This project extracts input fields from the Android application using ADB and XML parsing. The main function classifies and unclassifies fields from the XML dump of the UI elements of an Android app. It also incoporate ocr for better labeling and accuracy.

## Requirements

- Python 3.12
- Android Debug Bridge (ADB)
- Enabled debugging mode on the Android device

## Installation

1. **Extract the project:**
    ```bash
    unzip <path-folder>
    cd <path-folderr>
    ```
2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
Pytessarct package may require some installs:
On **Windows:**
1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

2. Note the tesseract path from the installation. Default installation path at the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

3. pip install pytesseract

4. Set the tesseract path in the script before calling image_to_string: pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
**On Linux:**
```bash
sudo apt-get update
sudo apt-get install libleptonica-dev tesseract-ocr tesseract-ocr-dev libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn
```
you can remove any package above that is not found in your distribution and it will still work (just means it is preinstalled)
**On Mac:**
```bash
brew install tesseract
```
3. **Ensure ADB is installed:**
    - You can download ADB from the [official website](https://developer.android.com/studio/releases/platform-tools).
    - Add ADB to your system's PATH.

4. **Enable debugging mode on your Android device:**
    - Go to `Settings` -> `About phone`.
    - Tap `Build number` seven times to unlock developer options.
    - Go to `Settings` -> `System` -> `Developer options`.
    - Enable `USB debugging`.
    - Alternatively Enable `Wireless Debugging` - <<Recommended since you can still use in on the phone as long as it is accessible on the network>>: If you decide to use wireless debugging:
    ```bash
    adb pair <<IP-address:port>>
    adb connect <<IP-address:port>> 
    ```

## Usage

1. **Connect your Android device:**
    - Connect your Android device to your computer via USB.
    - Ensure USB debugging is enabled and allow the connection if prompted.
    - You can also use wireless debugging - you can run the connect.py file to help you connect via wireless debugging
    - NB: When using wireless debugging it is reccommended you continuously ping the phone or IP-address of the phone eg:
     ```bash
     ping 192.168.0.101
    ```
2. **Run the main script:**
    ```bash
    python main.py
    ```

## Explanation

### Main Function Output

The main function prints the classified and unclassified input fields in JSON format:

- **Classified Input Fields:** These are the fields that have been identified and categorized based on their attributes and properties and is always shown as a green color
- **Unclassified Input Fields:** These are the fields that could not be categorized and are shown as yellow color in the display. - You will not come into this condition since the classifier is 100% accurate at this point

### Input Fields and Validations

The project categorizes input fields based on their attributes and classifies them accordingly. Here are the details:

- **Label:** The text associated with the input field.
- **Type:** The type of input field (e.g., `text input`, `password`, `button`).
- **Interactive:** Indicates if the field is interactive.
- **Resource ID:** The resource ID of the input field.
- **Validations:** The validations associated with the field (e.g., `min_length:6`, `email_format`).
- **Bounds:** The coordinates or bounds of the input field on the screen.

### Example of an Input Field Object

```json
{
    "label": "Username",
    "type": "text input",
    "interactive": true,
    "resource-id": "com.example:id/username",
    "validations": ["min_length:1", "max_length:4096"],
    "xy/bounds": "[0,100][300,200]"
}
```
# Input Field Extractor - Validations

Each input field can have various validations associated with it to ensure proper data entry.

## Validations

The following validations are applied to the input fields based on their type and attributes:

### General Validations

- **min_length:N**: Ensures that the input has at least `N` characters.
- **max_length:N**: Ensures that the input does not exceed `N` characters.

### Specific Validations

#### Text Input

- **email_format**: Ensures the input follows a valid email format.
- **url_format**: Ensures the input follows a valid URL format.

#### Password

- **contains_uppercase**: Ensures the input contains at least one uppercase letter.
- **contains_lowercase**: Ensures the input contains at least one lowercase letter.
- **contains_number**: Ensures the input contains at least one numerical digit.
- **contains_special_character**: Ensures the input contains at least one special character.

#### Date

- **date_format**: Ensures the input follows a valid date format, such as MM/YY.

#### Digits

- **valid**: Ensures the input contains only valid digits.
- **single_digit**: Ensures the input is a single digit.

#### Phone Number

- **phone_number**: Ensures the input is a valid phone number.
- **USSD_code**: Ensures the input follows a valid USSD code format.

### File Upload

- **file_size**: Ensures the uploaded file size is within the allowed limit.
- **file_format**: Ensures the uploaded file is of a valid format (e.g., jpg, png, pdf).
- **file_quality**: Ensures the uploaded file meets the required quality standards.

### Select (Dropdowns)

- **multiselect**: Ensures the input allows multiple selections.
- **single_select**: Ensures the input allows only a single selection.

### Checkboxes

- **multicheck**: Ensures that multiple checkboxes can be checked.
- **single_check**: Ensures that only a single checkbox can be checked.

### Date and Time

- **date_format**: Ensures the input follows a valid date format.
- **time_format**: Ensures the input follows a valid time format.

### Switches and Buttons

- **active**: Ensures that the switch or button is in an active state.

