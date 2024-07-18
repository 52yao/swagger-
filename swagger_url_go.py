import requests  
import pandas as pd  
from urllib.parse import urljoin  
  
# Swagger文档的URL  
swagger_base_url = 'https://www.test.com/'  
swagger_json_url = f'{swagger_base_url}/api/v2/api-docs'  
  
# 发送GET请求以获取Swagger文档  
response = requests.get(swagger_json_url)  
  
# 检查请求是否成功  
if response.status_code == 200:  
    try:  
        # 加载Swagger文档为JSON对象  
        swagger_data = response.json()  
  
        # 初始化一个DataFrame来存储提取的信息  
        data = []  
  
        # 遍历Swagger文档中的每个路径  
        for path, path_item in swagger_data['paths'].items():  
            # 遍历该路径下的每个HTTP方法  
            for method, operation in path_item.items():  
                # 拼接完整URL  
                full_url = urljoin(swagger_base_url, path.lstrip('/'))  
  
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
                    '是否存在未授权漏洞': '',  # 初始为空字符串，后续可根据实际情况填充
                    '是否为敏感数据': '',  # 初始为空字符串   
                    '数据样本': '',      # 初始为空字符串，用于记录测试时使用的数据样本  
                    '备注': ''  # 初始为空字符串，用于记录其他相关的漏洞信息或备注 
                }  
  
                # 将提取的信息添加到列表中  
                data.append(row)  
  
        # 创建DataFrame  
        df = pd.DataFrame(data)  
  
        # 将DataFrame保存到xlsx文件  
        df.to_excel('test.xlsx', index=False, engine='openpyxl')  
  
    except requests.exceptions.JSONDecodeError:  
        # 如果解析失败，提示用户获取的内容不是JSON格式  
        print("解析Swagger文档失败。内容不是JSON格式。")  
    except KeyError as e:  
        # 处理可能的KeyError（例如，如果Swagger文档结构不符合预期）  
        print(f"KeyError: Swagger文档中缺少键 {e}。")  
else:  
    print(f"获取Swagger文档失败。状态码: {response.status_code}")
