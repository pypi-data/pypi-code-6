import csv

def get_questions(source):
    """
    Reads data from CSV file.
    """
    with open(source, 'rb') as csvfile:
        line = csv.reader(csvfile, delimiter=';')
        return [[unicode(cell, 'utf-8') for cell in row] for row in line]