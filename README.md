作用：发现swagger未授权访问的时候，将里面的接口都提取出来


## v2.0
使用方法：</br>
-u api-docs文件路径，如 https://www.test.com:9999/v2/api-docs</br>
-f 可选参数，保存的文件名，如为空，默认以当前时间戳命名</br>

如：</br>
python .\swagger_url_go2.0.py -u https://www.test.com:9999/v2/api-docs  -f test</br>
python .\swagger_url_go2.0.py -u https://www.test.com:9999/v2/api-docs

</br>
执行完后当前目录下会生成两个文件，test.txt，test.xlxs文件</br>
test.txt文件为https://www.test.com:9999/v2/api-docs 页面原文，便于swagger未授权漏洞修复后的查漏补缺</br>
test.xlsx文件为提取路径、url、参数值，便于测试</br>

## v1.0
使用前需知：</br>
从api-docs文档获取数据，所以使用前需要将下图中的内容换成实际的url</br>
![图片](https://github.com/user-attachments/assets/f2f58e1e-ff5d-4591-aa8a-b06c32ad4540)


使用方法：python swagger_url_go.py

