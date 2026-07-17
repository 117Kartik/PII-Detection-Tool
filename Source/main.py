import docx
import faker
import spacy
from faker import Faker

nlp = spacy.load("en_core_web_sm")
fake=Faker()

print("fake,name:",fake.name())
print("fake,address:",fake.address())