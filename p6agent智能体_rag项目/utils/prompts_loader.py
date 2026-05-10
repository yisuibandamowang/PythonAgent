from tokenize import endpats

from p6agent智能体_rag项目.utils.config_handler import prompts_conf
from p6agent智能体_rag项目.utils.path_tool import get_abs_path
from p6agent智能体_rag项目.utils.logger_handler import logger

def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_system_prompts]配置文件中未找到main_prompt_path，{str(e)}")
        raise e

    try :
        return open(system_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_system_prompts]加载系统提示失败，{str(e)}")
        raise e



def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]配置文件中未找到 rag_summarize_prompt_path，{str(e)}")
        raise e

    try :
        return open(rag_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]加载RAG提示失败，{str(e)}")
        raise e



def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except KeyError as e:
        logger.error(f"[load_report_prompts]配置文件中未找到 report_prompt_path，{str(e)}")
        raise e

    try :
        return open(report_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"[load_report_prompts]加载系统提示失败，{str(e)}")
        raise e


if __name__ == "__main__":
    print(load_system_prompts())
    print(load_rag_prompts())
    print(load_report_prompts())