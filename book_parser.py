import sys

def parse_text(book_name):
    with open(f'./text_files/{book_name}.txt', 'r', encoding="utf8") as f:
        book_text = f.read()

    tests = book_text.split("\n\n")
    paragraphs = []

    for paragraph in tests:
        paragraphs.append(paragraph.replace("\n", " "))

    print(paragraphs)
    print("Number of paragraphs in this book: ", len(paragraphs))

if __name__ == '__main__':
    parse_text(sys.argv[1])