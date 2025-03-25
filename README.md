# GitHub CLI MCP服务器

这个MCP服务器为GitHub CLI提供了简单友好的接口，让你可以通过MCP协议访问GitHub的功能。

## 功能特点

- 仓库管理：查看、创建仓库
- Issue管理：查看、创建issue
- PR管理：查看、创建、查看差异
- Gist管理：查看、创建gist

## 安装要求

1. 安装GitHub CLI (gh)
   ```bash
   # MacOS
   brew install gh
   
   # Ubuntu/Debian
   apt install gh
   
   # 其他系统请参考GitHub CLI官方文档
   ```

2. 通过`gh auth login`完成GitHub认证

## 参数类型说明

本服务对参数类型有以下要求：

- PR编号必须使用整数类型：`pr_view(123, "owner/repo")`
- Issue编号必须使用整数类型：`issue_view(456, "owner/repo")`
- PR基础分支名称使用字符串类型：`pr_create("owner/repo", "标题", "内容", "main")`

所有整数参数在内部都会被自动转换为字符串，确保命令正确执行。

## 使用示例

```python
# 查看PR差异
diff = pr_diff(2543, "qianshouapp/kyc")

# 查看仓库
repo_info = repo_view("microsoft/vscode")

# 创建issue
issue_create("owner/repo", "标题", "这是issue的内容")
```

## PR差异查看

PR差异查看功能支持完整输出所有差异内容，不会进行截断，确保您可以查看到完整的代码变更。

使用示例：
```python
diff = pr_diff(2543, "qianshouapp/kyc")
print(diff)  # 显示完整差异
```

## 开发说明

如果需要扩展功能，可以修改`main.py`文件，添加新的工具函数并注册到MCP服务器。

## 可用工具

### 仓库操作

- `repo_list()` - 列出你拥有或参与的GitHub仓库
- `repo_view(repo)` - 查看仓库详细信息
- `repo_create(name, description, private)` - 创建新仓库

### Issue操作

- `issue_list(repo, state)` - 列出仓库中的issue
- `issue_view(issue, repo)` - 查看特定issue详情
- `issue_create(repo, title, body)` - 创建新issue

### PR操作

- `pr_list(repo, state)` - 列出仓库中的PR
- `pr_view(pr, repo)` - 查看特定PR详情
- `pr_diff(pr, repo)` - 查看特定PR的代码差异
- `pr_create(repo, title, body, base)` - 创建新PR

### Gist操作

- `gist_list()` - 列出你的Gist
- `gist_create(files, description, public)` - 创建新Gist

## 可用资源

- `repo://{owner}/{name}` - 获取仓库信息
- `user://{username}` - 获取用户信息

## 故障排除

如果遇到问题：

1. 确保GitHub CLI已正确安装，可通过运行 `gh --version` 验证
2. 确保已通过 `gh auth login` 进行身份验证
3. 检查是否有权限访问相应的仓库或资源
4. 如果使用JSON格式输出有问题，尝试使用标准输出格式

## 示例

查看PR：
```python
from main import pr_view
result = pr_view(pr="123", repo="owner/repo")
print(result)
```

查看PR代码差异：
```python
from main import pr_diff
result = pr_diff(pr="123", repo="owner/repo")
print(result)
```

创建Issue：
```python
from main import issue_create
result = issue_create(
    repo="owner/repo",
    title="测试Issue",
    body="这是通过MCP创建的测试Issue"
)
print(result)
```
