import sys

def parse_text(text_file):
    with open(f'./text_files/{text_file}', 'r', encoding="utf8") as f:
        gatsby = f.read()

    tests = gatsby.split("\n\n")
    paragraphs = []

    for paragraph in tests:
        if paragraph != "------------------------------------------------------------------------":
            paragraphs.append(paragraph.replace("\n", " "))

    print("Number of paragraphs in this book: ", len(paragraphs))

if __name__ == '__main__':
    parse_text(sys.argv[1])