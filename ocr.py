import sys
import argparse
import io
import json
import os.path
import re
from datetime import datetime
from typing import Any, Dict
from google.cloud import vision
from PIL import Image

PATH = "C:\\Users\\Tal Meshali\\Desktop\\Discovery Winter"

PASSPORT_NUMBER_REGEX = r'\d{8}'
VALID_CHARACTERS_ONLY = r'[A-Z\$][A-Z01\$]+'
DATE_REGEX = r'(\d{2}\/\d{2}\/\d{4})'
DATE_FORMAT = '%d/%m/%Y'

COMPUTER_REGION_1_REGEX = r'[1I]SR((?>\w+<?)*)<((?>\w+<?)*)<*'  # ([^<]*)<
COMPUTER_REGION_2_REGEX = r'(\d{8})<\d[1I]SR(\d{6})\d[F|M](\d{6})'  # (\d{2})<(\d{7,8})<(\d)<+


def process_computer_region_1(data, raw_text: str):
    try:
        result = re.search(COMPUTER_REGION_1_REGEX, raw_text.replace(" ", ""))
        data["last_name"] = result.group(1).replace('<', ' ').replace('0', 'O').strip()
        data["first_name"] = result.group(2).replace('<', ' ').replace('0', 'O').strip()
        return True
    except AttributeError:
        return False


def process_computer_region_2(data, raw_text: str):
    try:
        result = re.search(COMPUTER_REGION_2_REGEX, raw_text.replace(" ", ""))
        data["passport_number"] = result.group(1)
        return True
    except AttributeError:
        return False


class Counter:
    def __init__(self, threshold, T1):
        self.num = 0
        self.threshold = threshold
        self.length_needed = len(T1) - threshold

    def increment(self, value):
        self.num = value


def recursive_match(T1: str, T2: str, counter: Counter, i=0, j=0, s=""):
    if len(s) + min(len(T1) - i, len(T2) - j) < counter.length_needed:
        return
    if i == len(T1) or j == len(T2):
        if len(s) > counter.num:
            counter.increment(len(s))
        return
    elif T1[i] == T2[j]:
        return recursive_match(T1, T2, counter, i + 1, j + 1, s + T2[j])
    else:
        return recursive_match(T1, T2, counter, i + 1, j, s), recursive_match(T1, T2, counter, i, j + 1, s)


# T1 is the name of the field, T2 is the result of what was scanned
# threshold indicates what is the maximum amount of mismatches can be between the string in order to approve it
def find_longest_similarity(T1: str, T2: str, threshold: int) -> int:
    T1, T2 = T1.lower(), T2.lower()
    result = Counter(threshold, T1)
    recursive_match(T1, T2, result)
    return max(len(T2), len(T1)) - threshold <= result.num


def find_name(word_list, word_dict, result, final_word_idx):
    # First and Last names
    first_name, last_name, parse_names, started_last = "", "", False, False
    for i in range(len(word_list) - 1, 1, -1):
        name = "last_name" if started_last else "first_name"
        if parse_names:
            if word_list[i] == "<<":
                started_last = True
                continue
            if word_list[i] == "<":
                if word_list[i - 1] == "P":
                    break
                result[name] = " " + result[name]
                continue
            if word_list[i - 1] == "ISR":
                result[name] = word_list[i] + result[name]
                break
            if not re.fullmatch(VALID_CHARACTERS_ONLY, word_list[i]) or (
                    not re.fullmatch(VALID_CHARACTERS_ONLY, word_list[i - 2]) and not re.fullmatch(
                VALID_CHARACTERS_ONLY,
                word_list[i - 3])):
                continue
            # for conf_idx, confidence in enumerate(word_dict[word_list[i]]):
            #     if confidence < 0.5:
            #         print(confidence, word_list[i][conf_idx])
            if "ISR" not in word_list[i] or "AEL" == word_list[i][3:6]:
                result[name] = word_list[i] + result[name]
            else:
                result[name] = word_list[i][3:] + result[name]
                final_word_idx["val"] = i - 1
                break
        if "<" in word_list[i] and re.match(VALID_CHARACTERS_ONLY, word_list[i - 1]):
            parse_names = True
    for field in ["last_name", "first_name"]:
        result[field] = result[field].replace("$", "S").replace("1", "I").replace("0", "O").strip()


def find_birth_place(word_list, word_dict, result, final_word_idx):
    # Place of Birth
    found_birth_place = False
    for i in range(2, final_word_idx["val"]):
        if found_birth_place:
            low_conf = False
            if len(word_list[i]) < 3 or not re.fullmatch(VALID_CHARACTERS_ONLY, word_list[i]):
                continue
            if word_list[i] in ["MIT", "JERUSALEM", "MAT"]:
                continue
            # for conf_idx, confidence in enumerate(word_dict[word_list[i]]):
            #     if confidence < 0.4:
            #         low_conf = True
            if not low_conf:
                result["birth_place"] = word_list[i]
                break
        field = word_list[i - 2] + " " + word_list[i - 1] + " " + word_list[i]
        if find_longest_similarity(field, "Place of birth", 2):
            found_birth_place = True
            final_word_idx['val'] = i - 2
    if not result['birth_place']:
        result['birth_place'] = 'ISRAEL'


def find_dates(word_list, result):
    # Dates:
    dates = []
    for word in word_list:
        try:
            dates.append(datetime.strptime(re.search(DATE_REGEX, word.replace("00/00", "01/01")).group(0), DATE_FORMAT))
        except AttributeError:
            continue
    for key, date in zip(['birth_date', 'issue_date', 'expiry_date'], sorted(dates)):
        result[key] = date.strftime(DATE_FORMAT)


def find_passport_number(word_list, result):
    # Passport Number
    passport_nums = []
    for word in word_list:
        if re.match(PASSPORT_NUMBER_REGEX, word):
            passport_nums.append(word)
    if len(passport_nums) == 2:
        if passport_nums[0] == passport_nums[1]:
            result['passport_number'] = passport_nums[0]
            return
    lengths = [len(s) if s[0] in ["2", "3"] else 0 for s in passport_nums]
    result['passport_number'] = passport_nums[lengths.index(max(lengths))]


def get_parameters(response):
    word_dict = {}
    word_list = []
    for page in response.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_symbols = []
                    word_key = ""
                    for symbol in word.symbols:
                        word_symbols.append(symbol.confidence)
                        word_key += symbol.text
                    word_dict[word_key] = word_symbols
                    word_list.append(word_key)
    return word_dict, word_list, {"val": len(word_list) - 1}


def parse_passport_image(image_path: str) -> Dict:
    result = {key: "" for key in ["passport_number", "last_name", "first_name", "birth_place",
                                  "birth_date", "issue_date", "expiry_date"]}
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image).full_text_annotation  # pylint: disable=no-member
    word_dict, word_list, final_word_idx = get_parameters(response)
    for item in response.text.split("\n")[::-1]:
        item = item.replace(" ", "")
        if "<" * 3 in item and "SR" in item:
            if "<" * 6 in item or "P<ISR" in item:
                computer_regions = process_computer_region_1(result, item)
                if not computer_regions:
                    find_name(word_list, word_dict, result, final_word_idx)
            else:
                computer_regions = process_computer_region_2(result, item)
                if not computer_regions:
                    find_passport_number(word_list, result)
    find_birth_place(word_list, word_dict, result, final_word_idx)
    find_dates(word_list, result)
    print(result)
    return result


def write_passport_to_file(passport: Dict[str, str], output_path: str):
    """
    Write passport object to file in JSON format
    :param passport: passport object
    :param output_path: path to output file
    """
    with open(output_path, 'w') as output_file:
        output_file.write(json.dumps(passport, indent=4, default=str))


def find_file(trip, passenger, file_type):
    path = os.path.join(PATH, trip, "READY FOR VISA", passenger)
    try:
        for file in os.listdir(path):
            if file_type in file:
                return os.path.join(path, file), os.path.join(path, file.split(".")[0] + ".json")
    except Exception:
        raise FileNotFoundError("Passport isn't its valid directory")


def find_file_bot(phone, idx, file_type):
    path = os.path.join(PATH, phone, idx)
    try:
        for file in os.listdir(path):
            if file_type in file:
                return os.path.join(path, file), os.path.join(path, file.split(".")[0] + ".json")
    except Exception:
        raise FileNotFoundError("Passport isn't its valid directory")


def extract_face(filename):
    """Finds a polygon around the faces, and crops the image to be on a 3X4 scale.
    Args:
      image: a file containing the image with the faces.
      face: the face found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          face is cropped and saved accordingly.
    """
    with open(filename, "rb") as image:
        face = detect_face(image)
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        im = Image.open(image)
        confidence = face.detection_confidence
        width, height = im.size
        if confidence < 0.9:
            return False
            # return ValueError(f"File isn't a valid photo, confidence is {confidence}")
        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        x1, x2, y1, y2 = box[0][0], box[2][0], box[0][1], box[2][1]
        if x2 - x1 < y2 - y1:
            addition = height * 0.1
            y1, y2 = max(0, y1 - addition), min(height, y2 + addition)
            diff = ((y2 - y1) * 0.75 - (x2 - x1)) / 2
            x1 -= diff
            x2 += diff
            im.crop((max(0, x1), y1, min(width, x2), y2)).save(filename)
            print(filename.split("\\")[-1].split('.')[0] + " cropped successfully!")
            return True
        else:
            return False
            # return ValueError(f"File isn't a valid photo, try flipping sideways")


def detect_face(face_file):
    """Uses the Vision API to detect faces in the given file.
    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()
    content = face_file.read()
    image = vision.Image(content=content)
    return client.face_detection(image=image, max_results=1).face_annotations[0]  # pylint: disable=no-member


def main_no_args(trip, passenger):
    image_path, output_path = find_file(trip, passenger, "PASSPORT")
    self_photo_path = find_file(trip, passenger, "PHOTO")[0]
    extract_face(self_photo_path)
    write_passport_to_file(parse_passport_image(image_path), output_path)


def verify_fields(sender, ben_num, doc_type):
    if re.match(r'\d{12}', sender) and re.match(r'\d{1,2}', ben_num) and doc_type in ['photo', 'passport']:
        file_name = os.path.join('Public', sender, ben_num, f"{doc_type}.jpg")
        if os.path.exists(file_name):
            return True
        print("File does not exist: ", file_name)
        return False
    print("Fields are invalid: ", sender, ben_num, doc_type)
    return False


def verify_documents(sender, ben_num, doc_type):
    if verify_fields(sender, ben_num, doc_type):
        if doc_type == "photo":
            return extract_face(os.path.join('Public', sender, ben_num, "photo.jpg"))
        elif doc_type == "passport":
            result = parse_passport_image(os.path.join('Public', sender, ben_num, "passport.jpg"))
            if sum([1 if x else 0 for x in result.values()]) == 7:
                with open(os.path.join('Public', sender, ben_num, "data.json"), 'w') as output_file:
                    output_file.write(json.dumps(result, indent=4, default=str))
                return True
    return False


def parse_args() -> Dict[str, Any]:
    """
    Parse command line arguments
    WARNING: This function will exit the program if arguments are invalid
    :return: dictionary of arguments
    """
    parser = argparse.ArgumentParser(description='Passport OCR')
    parser.add_argument(
        '-n', '--sender_name',
        type=str,
        required=True,
        help='Sender identifier (phone number)')
    parser.add_argument(
        '-b', '--beneficiary_index',
        type=str,
        required=False,
        help='Beneficiary identifier (index)')
    parser.add_argument(
        '-d', '--doc_type',
        type=str,
        required=True,
        help='Document type (photo/passport)')

    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    verify_documents(args['sender_name'], "0", args['doc_type'])
