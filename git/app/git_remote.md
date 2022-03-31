# Git - 远程仓库操作

[返回Git首页](../git_index.md)

## 目录
- [Git - 远程仓库操作](#git---远程仓库操作) 
  - [目录](#目录)
  - [总结](#总结)
  - [远程仓库参数](#远程仓库参数)
    - [查看：远程仓库列表 git remote](#查看远程仓库列表git-remote)
      - [无参数：只显示别名](#无参数只显示别名)
      - [参数v：显示详细地址](#参数v显示详细地址)
    - [查看：指定远程仓库参数 git remote show](#查看指定远程仓库参数-git-remote-show)
    - [添加：远程仓库 git remote add](#添加远程仓库git-remote-add)
    - [查看：指定仓库的链接 git remote get-url](#查看指定仓库的链接-git-remote-get-url)
    - [修改：本地仓库别名 git remote rename](#修改本地仓库别名-git-remote-rename)
    - [修改：远程仓库参数 git config remote.](#修改远程仓库参数-git-config-remote)
    - [删除：远程仓库参数 git remote remove](#删除远程仓库参数-git-remote-remove)

***

## 总结

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

## 远程仓库参数

### 查看：远程仓库列表git remote

#### 无参数：只显示别名

命令

```git
git remote
```

- 只显示远程仓库在本地的别名。

![图片1](../pics/remote/%E5%9B%BE%E7%89%871.png)

#### 参数v：显示详细地址

命令

```git
git remote -v
```

- 显示的包括fetch和push的地址。

![图片2](../pics/remote/%E5%9B%BE%E7%89%872.png)

[回到目录](#目录)

***

### 查看：指定远程仓库参数 git remote show 

命令

```git
git remote show <remote_alias>
```

- <remote_alias>: 远程仓库在本地的别名

![图片4](../pics/remote/图片4.png)

[回到目录](#目录)

***

### 添加：远程仓库git remote add

命令

```git
git remote add <alias> <remote_url>
```

- <alias>: 远程仓库在本地的别名
- <remote_url>: 通常是github仓库链接地址

![图片3](../pics/remote/%E5%9B%BE%E7%89%873.png)

[回到目录](#目录)

***

### 查看：指定仓库的链接 git remote get-url

命令

```git
git remote get-url --push|--all <remote_alias>
```

- --push：获取push的地址
- --all：获取所有地址
- <remote_alias>: 指定仓库

![图片6](../pics/remote/%E5%9B%BE%E7%89%876.png)

[回到目录](#目录)

***

### 修改：本地仓库别名 git remote rename

命令

```git
git remote rename <old_name> <new_name>
```

- <old_name>: 旧名
- <new_name>：新名

![图片5](../pics/remote/%E5%9B%BE%E7%89%875.png)

[回到目录](#目录)

***

### 修改：远程仓库参数 git config remote.

1. 先使用 `git config --local -l` 查看；
2. 然后使用 `git config remote.<remote_alias>.url <new_url>` 修改。

![图片7](../pics/remote/%E5%9B%BE%E7%89%877.png)

[回到目录](#目录)

***

### 删除：远程仓库参数 git remote remove 

命令

```git
git remote remove <remote_alias>
```

- <remote_alias>: 远程仓库在本地的别名
- 
![图片8](../pics/remote/%E5%9B%BE%E7%89%878.png)

[回到目录](#目录)

***

