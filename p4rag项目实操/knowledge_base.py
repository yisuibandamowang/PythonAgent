import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str:str):
    if not os.path.exists(config.md5_path):
        # 文件不存在
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False

def save_md5(md5_str:str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding='utf-8').close()
    else:
        open(config.md5_path,'a',encoding='utf-8').write(md5_str+'\n')

def get_string_md5(input_str:str,encoding="utf-8"):
    # 将字符串转换为bytes字节数组
    str_bytes = input_str.encode(encoding=encoding)
    # 创建MD5对象
    md5 = hashlib.md5()
    # 对字节数组进行MD5计算
    md5.update(str_bytes)
    return md5.hexdigest()

class KnowledgeBaseService(object):
    def __init__(self):
        #如果文件夹不存在则创建    如果存在则跳过
        os.makedirs(config.persist_directory,exist_ok=True)
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=OllamaEmbeddings(model="qwen3-embedding:8b-fp16"),
            persist_directory=config.persist_directory
        )        # 向量数据库
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=config.separators,
            length_function=len,
        )       # 文本切分

    def upload_by_str(self,data,filename):
        "将传入的字符串进行向量化，存入向量数据库"
        md5_str = get_string_md5(data)

        if check_md5(md5_str):
            print("文件已存在")
            return "文件已存在"

        if len(data) > config.max_split_char_num:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else :
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"xiaohei",
        }

        self.chroma.add_texts(       # 添加向量
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        #
        save_md5(md5_str)

        return "上传成功"




if __name__ == '__main__':
    service = KnowledgeBaseService()
    res = service.upload_by_str("周杰伦1","testfile")
    print(res)