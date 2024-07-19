import requests  
import pandas as pd  
import argparse 
from urllib.parse import urljoin
from datetime import datetime
import json

def extract_base_url_with_port(full_url):  
    # 找到最后一个'/'的位置  
    last_slash_index = full_url.rfind('/')  
    # 如果找到了'/'，则截断字符串到该位置之前（不包括'/'）  
    if last_slash_index != -1:  
        base_url = full_url[:last_slash_index]  
    else:  
        # 如果没有找到'/'，则整个URL（假设它是有效的）就是base_url  
        # 但实际上，这种情况不太可能发生，因为URL通常会包含路径或至少一个'/'  
        base_url = full_url  
      
    # 确保base_url不以'/'结尾（尽管在这个特定的函数中，由于我们总是截断到最后一个'/'之前，  
    # 所以这一步其实是多余的，但保留它以保持函数的清晰性和通用性）  
    if base_url.endswith('/'):  
        base_url = base_url[:-1]  
      
    return base_url  
  

def save_swagger_to_file(url, file_name): 
    # 发送GET请求以获取Swagger文档  
    response = requests.get(url)  
  
    # 检查请求是否成功  
    if response.status_code == 200:  
        try:  
            # 加载Swagger文档为JSON对象  
            swagger_data = response.json() 

            # 将JSON对象转换为字符串（如果它还不是字符串的话） 
            swagger_data_str = json.dumps(swagger_data, indent=4)  # indent=4 用于美化输出


            # 将JSON字符串写入到.txt文件中
            with open(f"{file_name}.txt", 'w') as f:
               f.write(swagger_data_str)


            # 初始化一个DataFrame来存储提取的信息  
            data = []  
  
            # 遍历Swagger文档中的每个路径  
            for path, path_item in swagger_data['paths'].items():  
                # 遍历该路径下的每个HTTP方法  
                for method, operation in path_item.items():  
                    # 拼接完整URL  
                    full_url = urljoin(extract_base_url_with_port(url), path.lstrip('/'))    
  
                    # 初始化参数列表  
                    parameters = []  
  
                    # 检查是否存在parameters字段  
                    if 'parameters' in operation:  
                        # 遍历所有参数  
                        for param in operation['parameters']:  
                            # 提取参数名和类型  
                            param_name = param['name']  
                            param_type = param['in']  # 'in'字段指定了参数的类型（如path, query, header等）  
                            # 可以添加更多参数信息，如description, required等  
                            parameters.append(f"{param_type}: {param_name}")  
  
                    # 提取所需的信息  
                    row = {  
                         '路径': path,  
                         '方法': method,  
                         '标签': ', '.join(operation.get('tags', [])),  
                         '摘要': operation.get('summary', ''),  
                         '完整URL': full_url,  
                         '参数': ', '.join(parameters) if parameters else '无参数', 
                         '是否存在未授权访问漏洞': '',  # 初始为空字符串   
                         '是否为敏感数据': '',  # 初始为空字符串  
                         '数据样本': '',      # 初始为空字符串，用于记录测试时使用的数据样本  
                         '备注': ''  # 初始为空字符串，用于记录其他相关的信息或备注 
                        }  
  
                    # 将提取的信息添加到列表中  
                    data.append(row)  
  
            # 创建DataFrame  
            df = pd.DataFrame(data)  
  
            # 将DataFrame保存到xlsx文件  
            df.to_excel(f"{file_name}.xlsx", index=False, engine='openpyxl') 
  
        except requests.exceptions.JSONDecodeError:  
            # 如果解析失败，提示用户获取的内容不是JSON格式  
            print("解析Swagger文档失败。内容不是JSON格式。")  
        except KeyError as e:  
            # 处理可能的KeyError（例如，如果Swagger文档结构不符合预期）  
            print(f"KeyError: Swagger文档中缺少键 {e}。")  
    else:  
        print(f"获取Swagger文档失败。状态码: {response.status_code}")


def main():  
    # 创建解析器  
    parser = argparse.ArgumentParser(description='下载并保存Swagger JSON文档')  
  
    # 添加参数  
    parser.add_argument('-u', '--url', type=str, required=True,  
                        help='Swagger JSON文档的URL')  
    parser.add_argument('-f', '--file', type=str, default=lambda:f'api_docs_{datetime.now().strftime("%Y%m%d%H%M%S")}',  
                        help='保存Swagger文档的文件名（默认为当前时间命名的文件）')
    # 解析命令行参数  
    args = parser.parse_args()  
  
    # 注意：由于default是一个lambda函数，我们需要在这里调用它来获取文件名  
    file_name = args.file() if callable(args.file) else args.file
  
    # 调用函数保存Swagger文档  
    save_swagger_to_file(args.url, file_name)  
  
if __name__ == '__main__':  
    main()
