from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
)

# 批量加载
# documents = loader.load()
# print(documents)
#
# for doc in documents:
#     print(doc.page_content)

# 懒加载
for doc in loader.lazy_load():
    print(doc.page_content)