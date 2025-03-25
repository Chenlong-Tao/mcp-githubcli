import subprocess
import json
from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP, Context

# 创建MCP服务器
mcp = FastMCP("github-cli")

def run_gh_command(args: List[str]) -> str:
    """执行GitHub CLI命令并返回结果"""
    try:
        result = subprocess.run(
            ["gh"] + args, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"错误: {e.stderr}"

# 仓库相关工具
@mcp.tool()
def repo_list() -> str:
    """列出你拥有或参与的GitHub仓库"""
    return run_gh_command(["repo", "list"])

@mcp.tool()
def repo_view(repo: str) -> str:
    """查看仓库详细信息"""
    return run_gh_command(["repo", "view", repo])

@mcp.tool()
def repo_create(name: str, description: Optional[str] = None, private: bool = False) -> str:
    """创建新仓库"""
    args = ["repo", "create", name]
    if description:
        args.extend(["--description", description])
    if private:
        args.append("--private")
    return run_gh_command(args)

# Issue相关工具
@mcp.tool()
def issue_list(repo: str, state: str = "open") -> str:
    """列出仓库中的issue"""
    return run_gh_command(["issue", "list", "--repo", repo, "--state", state])

@mcp.tool()
def issue_view(issue: int, repo: str) -> str:
    """查看特定issue详情"""
    # 确保issue参数是字符串
    issue_str = str(issue)
    
    return run_gh_command(["issue", "view", issue_str, "--repo", repo])

@mcp.tool()
def issue_create(repo: str, title: str, body: str) -> str:
    """创建新issue"""
    return run_gh_command(["issue", "create", "--repo", repo, "--title", title, "--body", body])

# PR相关工具
@mcp.tool()
def pr_list(repo: str, state: str = "open") -> str:
    """列出仓库中的PR"""
    return run_gh_command(["pr", "list", "--repo", repo, "--state", state])

@mcp.tool()
def pr_view(pr: int, repo: str) -> str:
    """查看特定PR详情"""
    try:
        # 确保pr参数是字符串
        pr_str = str(pr)
        
        # 首先尝试使用标准视图
        result = run_gh_command(["pr", "view", pr_str, "--repo", repo])
        
        # 检查是否有错误
        if result.startswith("错误:"):
            # 尝试使用JSON格式，可能更稳定
            json_result = run_gh_command(["pr", "view", pr_str, "--repo", repo, "--json", "title,state,author,url,number,additions,deletions"])
            
            # 解析JSON结果
            try:
                data = json.loads(json_result)
                # 构建友好格式
                formatted_result = f"""
标题: {data.get('title', 'N/A')}
状态: {data.get('state', 'N/A')}
作者: {data.get('author', {}).get('login', 'N/A')}
编号: {data.get('number', 'N/A')}
URL: {data.get('url', 'N/A')}
增加行数: {data.get('additions', 'N/A')}
删除行数: {data.get('deletions', 'N/A')}
"""
                return formatted_result
            except json.JSONDecodeError:
                # JSON解析失败，返回原始错误
                return result
        
        return result
    except Exception as e:
        return f"错误: 查看PR时发生异常: {str(e)}"

@mcp.tool()
def pr_diff(pr: int, repo: str) -> str:
    """查看特定PR的代码差异"""
    try:
        # 确保pr参数是字符串
        pr_str = str(pr)
        
        # 使用GitHub CLI的pr diff命令
        result = run_gh_command(["pr", "diff", pr_str, "--repo", repo])
        
        # 检查是否有错误
        if result.startswith("错误:"):
            return result
        
        # 返回完整结果，不进行任何截断
        return result
    except Exception as e:
        return f"错误: 查看PR差异时发生异常: {str(e)}"

@mcp.tool()
def pr_create(repo: str, title: str, body: str, base: str = "main") -> str:
    """创建新PR"""
    return run_gh_command(["pr", "create", "--repo", repo, "--title", title, "--body", body, "--base", base])

# Gist相关工具
@mcp.tool()
def gist_list() -> str:
    """列出你的Gist"""
    return run_gh_command(["gist", "list"])

@mcp.tool()
def gist_create(files: List[str], description: Optional[str] = None, public: bool = False) -> str:
    """创建新Gist"""
    args = ["gist", "create"]
    if description:
        args.extend(["--desc", description])
    if not public:
        args.append("--private")
    args.extend(files)
    return run_gh_command(args)

# 资源: 获取仓库信息(JSON格式)
@mcp.resource("repo://{owner}/{name}")
def get_repo_info(owner: str, name: str) -> str:
    """获取仓库信息"""
    result = run_gh_command(["repo", "view", f"{owner}/{name}", "--json", "name,description,owner,isPrivate,stargazerCount"])
    return result

# 资源: 获取用户信息
@mcp.resource("user://{username}")
def get_user_info(username: str) -> str:
    """获取用户信息"""
    result = run_gh_command(["api", f"users/{username}"])
    return result

def main():
    mcp.run()

if __name__ == "__main__":
    main()
