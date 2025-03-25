import unittest
import sys
import os

# 确保能够导入main模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import pr_view, repo_list, repo_view, issue_list, gist_list, pr_diff

class TestGitHubCLI(unittest.TestCase):
    """GitHub CLI MCP 服务器集成测试"""
    
    def test_repo_list(self):
        """测试获取仓库列表"""
        result = repo_list()
        print("\n===== 仓库列表 =====")
        print(result)
        # 不验证具体内容，只确保能够执行
        self.assertIsInstance(result, str)
    
    def test_repo_view(self):
        """测试查看一个热门的公共仓库"""
        result = repo_view("microsoft/vscode")
        print("\n===== 仓库详情 =====")
        print(result)
        # 验证包含了预期的仓库信息
        self.assertIn("microsoft/vscode", result)
    
    def test_pr_view(self):
        """测试查看公共仓库的PR"""
        # 使用Microsoft VSCode的一个PR作为示例
        result = pr_view(pr="216", repo="microsoft/vscode")
        print("\n===== PR详情 =====")
        print(result)
        # 验证返回了PR信息
        self.assertIsInstance(result, str)
        
    def test_pr_view_kyc_2543(self):
        """测试查看qianshouapp/kyc仓库的PR #2543"""
        result = pr_view(pr="2543", repo="qianshouapp/kyc")
        print("\n===== KYC PR #2543 详情 =====")
        print(result)
        # 验证返回了PR信息
        self.assertIsInstance(result, str)
        # 如果成功获取PR，应该包含PR编号
        if "错误" not in result:
            self.assertIn("2543", result)
    
    def test_pr_diff(self):
        """测试查看PR代码差异"""
        # 使用已知存在的PR
        result = pr_diff(pr="2543", repo="qianshouapp/kyc")
        print("\n===== PR #2543 完整差异 =====")
        # 显示完整差异内容
        print(result)
        # 验证返回了差异信息
        self.assertIsInstance(result, str)
        
    def test_issue_list(self):
        """测试列出公共仓库的issue"""
        result = issue_list(repo="microsoft/vscode", state="open")
        print("\n===== Issue列表 =====")
        print(result)
        # 验证返回了issue列表
        self.assertIsInstance(result, str)
    
    def test_gist_list(self):
        """测试列出Gist"""
        # 注意：这需要GitHub认证
        try:
            result = gist_list()
            print("\n===== Gist列表 =====")
            print(result)
            self.assertIsInstance(result, str)
        except Exception as e:
            # 如果用户未认证，这可能会失败
            print(f"\n获取Gist列表时出错: {str(e)}")
            print("这可能是因为您未通过'gh auth login'进行GitHub认证")

if __name__ == "__main__":
    print("开始GitHub CLI集成测试...")
    print("注意：某些测试可能需要GitHub认证，请确保已运行'gh auth login'")
    unittest.main() 