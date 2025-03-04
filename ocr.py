import argparse
import io
import json
import os.path
import re
from typing import Any, Dict
from google.cloud import vision
from ocrequests.api.visa_requests.information.beneficiary_attributes_filler import (
    BeneficiaryAttributesFiller,
)


def get_parameters(response):
    word_list = []
    for page in response.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_key = ""
                    for symbol in word.symbols:
                        word_key += symbol.text
                    word_list.append(word_key)
    return word_list


def parse_passport_image(image_path: str) -> Dict:
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(
        image=image
    ).full_text_annotation  # pylint: disable=no-member
    word_list = get_parameters(response)
    result = BeneficiaryAttributesFiller().fill_in_details(word_list, {}, "01/01/2020")
    return result


def write_passport_to_file(passport: Dict[str, str], output_path: str):
    """
    Write passport object to file in JSON format
    :param passport: passport object
    :param output_path: path to output file
    """
    with open(output_path, "w") as output_file:
        output_file.write(json.dumps(passport, indent=4, default=str))


def find_file(trip, passenger, file_type):
    path = os.path.join(PATH, trip, "READY FOR VISA", passenger)
    try:
        for file in os.listdir(path):
            if file_type in file:
                return os.path.join(path, file), os.path.join(
                    path, file.split(".")[0] + ".json"
                )
    except Exception:
        raise FileNotFoundError("Passport isn't its valid directory")


def find_file_bot(phone, idx, file_type):
    path = os.path.join(PATH, phone, idx)
    try:
        for file in os.listdir(path):
            if file_type in file:
                return os.path.join(path, file), os.path.join(
                    path, file.split(".")[0] + ".json"
                )
    except Exception:
        raise FileNotFoundError("Passport isn't its valid directory")


def main_no_args(trip, passenger):
    image_path, output_path = find_file(trip, passenger, "PASSPORT")
    self_photo_path = find_file(trip, passenger, "PHOTO")[0]
    extract_face(self_photo_path)
    write_passport_to_file(parse_passport_image(image_path), output_path)


def verify_fields(sender, ben_num, doc_type):
    if (
        re.match(r"\d{12}", sender)
        and re.match(r"\d{1,2}", ben_num)
        and doc_type in ["photo", "passport"]
    ):
        file_name = os.path.join("Public", sender, ben_num, f"{doc_type}.jpg")
        if os.path.exists(file_name):
            return True
        print("File does not exist: ", file_name)
        return False
    print("Fields are invalid: ", sender, ben_num, doc_type)
    return False


def verify_documents(sender, ben_num, doc_type):
    if verify_fields(sender, ben_num, doc_type):
        if doc_type == "photo":
            return extract_face(os.path.join("Public", sender, ben_num, "photo.jpg"))
        elif doc_type == "passport":
            result = parse_passport_image(
                os.path.join("Public", sender, ben_num, "passport.jpg")
            )
            if sum([1 if x else 0 for x in result.values()]) == 7:
                with open(
                    os.path.join("Public", sender, ben_num, "data.json"), "w"
                ) as output_file:
                    output_file.write(json.dumps(result, indent=4, default=str))
                return True
    return False


def parse_args() -> Dict[str, Any]:
    """
    Parse command line arguments
    WARNING: This function will exit the program if arguments are invalid
    :return: dictionary of arguments
    """
    parser = argparse.ArgumentParser(description="Passport OCR")
    parser.add_argument(
        "-n",
        "--sender_name",
        type=str,
        required=True,
        help="Sender identifier (phone number)",
    )
    parser.add_argument(
        "-b",
        "--beneficiary_index",
        type=str,
        required=False,
        help="Beneficiary identifier (index)",
    )
    parser.add_argument(
        "-d",
        "--doc_type",
        type=str,
        required=True,
        help="Document type (photo/passport)",
    )

    return vars(parser.parse_args())


if __name__ == "__main__":
    args = parse_args()
    verify_documents(args["sender_name"], "0", args["doc_type"])
