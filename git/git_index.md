# 技术笔记: Git

[返回Page首页](../index.md)

Git 是一个开源的分布式版本控制系统，用于敏捷高效地处理任何或小或大的项目。

基本关系：
![图片1](./pics/general.jpg)


教程地址：  

https://www.runoob.com/git/git-workspace-index-repo.html

***

## 链接
- [Git - 配置文件及层级](./app/git_config_file.md#用户级别global(优先级次之) )
- [Git - 设置配置参数](./app/git_config.md)
- [Git - 工作区操作](./app/git_workspace.md)
- [Git - 缓存区操作](./app/git_stage.md)
- [Git - 本地仓库操作](./app/git_local_repo.md)
- [Git - 远程仓库操作](./app/git_remote.md)
- [Git - 比较差异 git diff](./app/git_diff.md)

*** 

## Cheat Sheet 速查表

### **工作区操作**

|动作|对象|Git命令|备注|
|---|---|---|---|
|**查看**|**工作区**文件|`dir | ls`|当前路径|
|**添加**|**工作区**文件||IDE|
|**删除**|**工作区**文件||IDE|
|**更改**|**工作区**文件||IDE|
|**查看**|<指定文件>历史|`git blame <filename>`|当前路径|
|**恢复**|**缓存区**<指定文件>|`git checkout <filename>`|当前路径|
|**恢复**|**缓存区**所有文件|`git checkout -f`|当前路径|

### **缓存区操作**

|动作|对象|命令|备注|
|---|---|---|---|
|**查看**|**缓存区**内文件|`git ls-files `||
|**添加**|<指定文件>|`git add <filename>`||
|**添加**|\\指定文件夹\\|`git add directory\`||
|**添加**|当前路径的**所有文件**|`git add .`|**不包含**已删除文件|
|**更新**|**已缓存的文件**|`git add -u|--update`|**不包含**新文件|
|**更新**|**已缓存的文件**|`git add -A`|**包含**已删除文件|
|**删除**|**缓存区**<指定文件>|`git rm --cached \<filename>`||
|**删除**|**工作区**和**缓存区**<指定文件>|`git rm -f <filename>`|**工作区文件**也删除|
|**删除**|**缓存区**当前路径下所有文件|`git rm -r * --cached`|Git: **工作区**当前路径|
|**删除**|**工作区**和**缓存区**当前路径下所有文件|`git rm -r * -f`|Git: **工作区**当前路径|

***

### **远程仓库操作**

|动作|对象|命令|备注|
|---|---|---|---|
|**查看**|远程仓库**别名列表**|`git remote`||
|**查看**|远程仓库**详细列表**|`git remote -v`||
|**查看**|指定远程仓库**详细参数**|`git remote show <remote_alias>`||
|**添加**|远程仓库**链接**|`git remote add <alias> <remote_url>`||
|**查看**|远程仓库**指定链接**|`git remote get-url --push|--all <remote_alias>`||
|**修改**|远程仓库**别名**|`git remote rename <old_name> <new_name>`||
|**修改**|远程仓库**链接**|`git config remote.<remote_alias>.url <new_url>`||
|**删除**|远程仓库|`git remote remove <remote_alias>`||

***

[返回Page首页](../index.md)
