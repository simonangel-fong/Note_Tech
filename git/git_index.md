# 技术笔记: Git

[返回Page首页](../index.md)

Git 是一个开源的分布式版本控制系统，用于敏捷高效地处理任何或小或大的项目。

基本关系：
![图片1](./pics/general.jpg)


教程地址：
https://www.runoob.com/git/git-workspace-index-repo.html

***

#### 目录
- [Git - 配置文件及层级](./app/git_config_file.md)
  - 系统级别system(优先级最低)
  - 用户级别global(优先级次之)
  - 仓库级别local(优先级最高)
- [Git - 设置配置参数](./app/git_config.md)
  - 查询:所有配置的参数list
    - system:查看系统的所有配置
    - global:查看用户的所有配置
    - local:查看本地的所有配置
  - 查询:特定key的配置值get section.key或section.key
  - 添加:特定key的配置值add
  - 修改：特定key的配置值 section.key value
  - 删除：删除特定键值 unset
  - 编辑器编辑:edit或-e
- [Git - 工作区操作](../app/git_workspace.md)
  - 添加/删除/更改:使用IDE
  - 查看:使用命令 ls(powershell)/dir(CMD)
  - 查看历史:工作区指定文件的修改历史git blame
    - 参数\<filename>: 必须指定文件名
  - 恢复:从缓存区复制到工作区 git checkout
    - 参数\<filename>: 恢复指定缓存区指定文件到工作区
    - 参数-f:强制恢复缓存区所有文件

***

[返回Page首页](../index.md)
