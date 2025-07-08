from splitter import splitter

with open("data/00107-83-3.xml", "r") as file:
    file_str = file.read()

list_of_articles, message = splitter(file_str)
print(list_of_articles[0][0])