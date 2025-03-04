import json

from google.cloud.vision import ImageAnnotatorClient, Image
from ocrequests.api.visa_requests.information.beneficiary_attributes_filler import (
    BeneficiaryAttributesFiller,
)

if __name__ == "__main__":
    client = ImageAnnotatorClient()
    with open("./AVIV OSNAT PASSPORT.jpg", "rb") as image_file:
        content = image_file.read()
    image = Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    word_list = []
    for page in document.pages:
        for block in page.blocks:
            block_words = []
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_key = ""
                    for symbol in word.symbols:
                        word_key += symbol.text
                    word_list.append(word_key)

    with open("./templates/beneficiary_update_details.json", "r") as json_file:
        request = json.loads(json_file.read())
        form = request["PUT"]["CONSTANT"]
        BeneficiaryAttributesFiller().fill_in_details(word_list, form, "12/11/22")
        print(form)
