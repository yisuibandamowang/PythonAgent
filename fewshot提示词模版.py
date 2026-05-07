from langchain_classic.chains.constitutional_ai.prompts import examples
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ALI_API_KEY")

example_prompt = PromptTemplate.from_template("单词：{word},反义词:{antonym}")

examples_data = [
    {"word": "good", "antonym": "bad"},
    {"word": "big", "antonym": "small"}
]

few_shot_template = FewShotPromptTemplate(
    example_prompt=example_prompt,        #示例数据的模版
    examples=examples_data,              #示例数据  用来注入动态数据的
    prefix="告知我反义词的示例，我提供的示例如下",                  #示例的之前的提示词
    suffix="基于前面的示例告知我{input_word}的反义词是什么",                  #示例的之后的提示词
    input_variables=['input_word'],         #声明在前缀或后缀中所需要注入的变量
)

prompt_text = few_shot_template.invoke({"input_word": "left"})
print(prompt_text)

model = Tongyi(model="qwen-max",api_key=api_key)
res = model.invoke(prompt_text)
print(res)
