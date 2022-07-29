import gutenbergpy.textget

book_text = gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(64317))
paragraphs = []
tests = book_text.decode("utf-8").split("\n\n")
for paragraph in tests:
    paragraphs.append(paragraph.replace("\n", " "))

print("Number of paragraphs in this book: ", len(paragraphs))