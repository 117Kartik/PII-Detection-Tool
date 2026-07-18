import random
import string

from faker import Faker


class Replacer:

    def __init__(self):

        self.fake = Faker()

        self.mapping = {}

        self.generators = {
            "EMAIL": self.fake.email,
            "PHONE": self.generate_phone,
            "DOB": self.generate_dob,
            "IP_ADDRESS": self.fake.ipv4,
            "CREDIT_CARD": self.fake.credit_card_number,
            "PAN": self.generate_pan,
            "AADHAAR": self.generate_aadhaar,
            "PASSPORT": self.generate_passport,
            "PERSON": self.fake.name,
            "ORG": self.generate_company,
            "GPE": self.generate_location,
            "LOC": self.generate_location,
        }

    def generate_phone(self):

        return "".join(random.choices("6789", k=1)) + "".join(
            random.choices(string.digits, k=9)
        )

    def generate_dob(self):

        return self.fake.date(pattern="%d/%m/%Y")

    def generate_pan(self):

        return (
            "".join(random.choices(string.ascii_uppercase, k=5))
            + "".join(random.choices(string.digits, k=4))
            + random.choice(string.ascii_uppercase)
        )

    def generate_aadhaar(self):

        return "".join(random.choices(string.digits, k=12))

    def generate_passport(self):

        return (
            random.choice(string.ascii_uppercase)
            + "".join(random.choices(string.digits, k=7))
        )

    def replace(self, match):

        original = match["value"]

        if original in self.mapping:
            return self.mapping[original]

        pii_type = match["type"]

        generator = self.generators.get(pii_type)

        if generator:
            replacement = generator()
        else:
            replacement = original

        self.mapping[original] = replacement

        return replacement
    
    # def build_character_map(self, paragraph):
    #     char_map = []

    #     position = 0

    #     for run_index, run in enumerate(paragraph.runs):

    #         for offset, ch in enumerate(run.text):

    #             char_map.append({
    #                 "position": position,
    #                 "run": run_index,
    #                 "offset": offset,
    #                 "character": ch
    #             })

    #             position += 1

    #     return char_map

    def replace_in_paragraph(self, paragraph, matches):

        for match in matches:

            original = match["value"]
            replacement = self.replace(match)

            for run in paragraph.runs:

                if original in run.text:
                    run.text = run.text.replace(original, replacement)


    def generate_company(self):
        suffixes = [
            "Ltd.",
            "Limited",
            "Private Limited",
            "Industries",
            "Technologies"
        ]

        return (
            self.fake.company().split(",")[0]
            + " "
            + random.choice(suffixes)
        )
    
    def generate_location(self):
        return f"{self.fake.city()}, India"