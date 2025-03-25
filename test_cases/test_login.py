# test_cases/test_login.py
import pytest
from libs.web_client import WebClient

@pytest.fixture(scope="module")
def web_client():
    """共享的HTTP客户端"""
    client = WebClient()
    yield client
    client.session.close()

@pytest.fixture
def valid_account():
    """从配置文件加载有效账号"""
    with open("config/config.yaml") as f:
        import yaml
        config = yaml.safe_load(f)
        return config["test_account"]["valid"]

@pytest.fixture
def invalid_account():
    """从配置文件加载无效账号"""
    with open("config/config.yaml") as f:
        import yaml
        config = yaml.safe_load(f)
        return config["test_account"]["invalid"]

def test_web_login_success(web_client,valid_account):
    """验证成功登录"""
    password=valid_account["password"]
    print(password)
    data = web_client.web_login(password)
    print(data)
    #assert data["msg"] != "not auth"
    assert data==0

def test_web_login_failed(web_client,invalid_account):
    """验证错误密码登录失败"""
    password=invalid_account["password"]
    # print(password)
    # assert not web_client.web_login(password), "错误密码意外成功"
    data = web_client.web_login(password)
    #assert data["msg"] != "not auth"
    assert data==401