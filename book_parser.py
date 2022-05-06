with open('./text_files/the_great_gatsby.txt', 'r', encoding="utf8") as f:
    gatsby = f.read()

tests = gatsby.split("\n\n")
paragraph = []

for i in range(len(tests)):
    paragraph.append(tests[i].replace("\n", " "))

print(paragraph[1:10])