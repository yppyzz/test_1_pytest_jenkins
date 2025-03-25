'''
HTTP请求封装
'''
import requests
from requests.exceptions import RequestException
import yaml
from typing import Optional, Dict

class WebClient:
    def __init__(self, config_path: str = "config/config.yaml"):
        # 加载配置文件
        with open(config_path) as f:
            self.config = yaml.safe_load(f)["router"]
        self.base_url = f"http://{self.config['ip']}"
        self.login_url = f"{self.base_url}{self.config['login_path']}"
        self.session = requests.Session()
        
    def web_login(self, password: str) -> bool:
        """Web登录验证(支持异常重试）"""
        #login_url = f"{self.base_url}/cgi-bin/luci/api/xqsystem/login"
        #print("self.login_url",self.login_url)
        payload = {
            "username":"admin",
            "password": password
        }
        
        try:
            response = self.session.post(
                self.login_url,
                data=payload,
                timeout=5,
                allow_redirects=False
            )
            # 登录成功会返回302重定向
            data = response.json() # 自动解析JSON
            code_value = data["code"]
            #code_value = response.text
            print("code_value", code_value)
            return code_value
        except RequestException as e:
            print(f"登录请求失败: {str(e)}")
            return False
