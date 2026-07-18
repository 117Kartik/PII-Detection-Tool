import re
import spacy


class Detector:

    def __init__(self):

        self.nlp = spacy.load("en_core_web_lg")

        self.patterns = {

            "EMAIL": re.compile(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
            ),

            "PHONE": re.compile(
                r"(?:\+91[-\s]?)?[6-9]\d{9}\b"
            ),

            "DOB": re.compile(
                r"\b(?:\d{2}[/-]\d{2}[/-]\d{4}|\d{4}[/-]\d{2}[/-]\d{2})\b"
            ),

            "IP_ADDRESS": re.compile(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            ),

            "CREDIT_CARD": re.compile(
                r"\b(?:\d{4}[- ]?){3}\d{4}\b"
            ),

            "PAN": re.compile(
                r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
            ),

            "AADHAAR": re.compile(
                r"\b\d{4}\s?\d{4}\s?\d{4}\b"
            ),

            "PASSPORT": re.compile(
                r"\b[A-Z][0-9]{7}\b"
            )
        }

        self.rule_pattern = re.compile(
            r"\b[A-Z]{2,}(?:\s+[A-Z]{2,}){1,5}\b"
        )

        self.blacklist = {
            "RED",
            "HERRING",
            "PROSPECTUS",
            "LIMITED",
            "CORPORATE",
            "IDENTITY",
            "NUMBER",
            "EMAIL",
            "TELEPHONE",
            "OUR",
            "PROMOTERS",
            "FAMILY",
            "TRUST",
            "INDIA",
            "MAHARASHTRA",
            "FRESH",
            "ISSUE",
            "SALE",
            "COMPANY",
            "SECRETARY",
            "OFFICER"
        }

    def detect_regex(self, text):

        matches = []

        for pii_type, pattern in self.patterns.items():

            for match in pattern.finditer(text):

                matches.append({
                    "type": pii_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "source": "regex"
                })

        return matches

    def detect_rules(self, text):

        matches = []

        for match in self.rule_pattern.finditer(text):

            value = match.group().strip()

            words = value.split()

            if len(words) < 2:
                continue

            if any(word in self.blacklist for word in words):
                continue

            matches.append({
                "type": "PERSON",
                "value": value,
                "start": match.start(),
                "end": match.end(),
                "source": "rule"
            })

        return matches

    def detect_spacy(self, text):

        matches = []

        doc = self.nlp(text)

        allowed_entities = {
            "PERSON",
            "ORG",
            "GPE",
            "LOC"
        }

        for ent in doc.ents:

            if ent.label_ in allowed_entities:

                matches.append({
                    "type": ent.label_,
                    "value": ent.text,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "source": "spacy"
                })

        return matches

    def remove_duplicates(self, matches):

        matches.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))

        filtered = []

        occupied = set()

        for match in matches:

            overlap = False

            for i in range(match["start"], match["end"]):

                if i in occupied:
                    overlap = True
                    break

            if overlap:
                continue

            filtered.append(match)

            for i in range(match["start"], match["end"]):
                occupied.add(i)

        return filtered

    def detect(self, text):

        matches = []

        matches.extend(self.detect_regex(text))
        matches.extend(self.detect_rules(text))
        matches.extend(self.detect_spacy(text))

        matches = self.remove_duplicates(matches)

        matches.sort(key=lambda x: x["start"])

        return matches