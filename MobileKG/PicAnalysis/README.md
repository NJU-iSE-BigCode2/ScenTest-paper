# WidgetRec

## Methods

- Nontext component extract methods
  - Canny
  - UIED
- Text extract methods
  - Baidu-ocr
- Merge methods
  - Canny-ocr-merge
  - UIED-merge

## How to use?

### Dependency

- Python 3.6
- The dependencies for this project are shown in ‘requirements.txt’. You can install them manually. Or you can run 'pip install -r requirements.txt' to install dependency.

### Preparation

- #### OCR Interface

Go to https://ai.baidu.com/ and request an app id, an api key and a secret key. Then replace the corresponding strings in the `text_algorithm/baidu_ocr/Baidu_ocr.py` line 16-19.

- #### Select the method to use

You can see the methods you can use in the file 'config/Config_enum.py'. Modify the configuration in the ‘config/Config.py‘ to match the methods

### Usage

To test your own image:

- Put your pictures in 'data/input'
- change image_path and output_path in main.py line27 and line 30
- run 'python main.py' to test your image, the result can be seen in 'data/output'

## File structure

component_algorithm/

- Nontext component extract methods

config/

- Algorithm parameters
- The path configuration

data/

- Input UI images and output detection results

merge_algorithm/

- Merge methods

text_algorithm/

- Text extract methods

utils/

- Tools used in the project

main.py/

- Program entry

requirements.txt/

- dependency





