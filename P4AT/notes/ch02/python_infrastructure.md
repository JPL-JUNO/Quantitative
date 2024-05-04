# Python 基础架构

## conda 作为软件包管理器

### conda 的基本操作

conda 可用于高效地处理 Python 软件包的安装，更新和删除，下面概述了其主要功能：

- 安装 Python x.x 版本

```shell
conda install python=x.x
```

- 更新 Python

```shell
conda update python
```

- 安装一个软件包

```shell
conda install $PACKAGE_NAME
```

- 更新一个软件包

```shell
conda update $PACKAGE_NAME
```

- 移除一个软件包

```shell
conda remove $PACKAGE_NAME
```

- 更新 conda

```shell
conda update conda
```

- 寻找软件包

```shell
conda search $SEARCH_TERM
```

- 列出已安装的软件包

```shell
conda list
```

也可以一次安装多个软件包。`-y` 标志表示所有（潜在的）问题都应回答 yes。

```shell
conda install -y ipython matplotlib pandas pytables scikit-learn scipy
```

## conda 作为虚拟环境管理器

安装包含 conda 的 Miniconda 后会提供默认的 Python 安装，具体取决于选择的 Miniconda 版本。例如，conda 的虚拟环境管理功能允许将完全独立的 Python 2.7.x 安装添加到 Python 3.8 默认安装中。为此，conda 提供了以下功能：

- 创建一个虚拟环境

```shell
conda create --name $ENVIRONMENT_NAME python=x.x
```

- 激活一个虚拟环境

```shell
conda activate $ENVIRONMENT_NAME
```

- 停用一个虚拟环境

```shell
conda deactivate $ENVIRONMENT_NAME
```

- 删除一个虚拟环境

```shell
conda env remove --name $ENVIRONMENT_NAME
```

- 导出到一个环境文件

```shell
conda env export > $FILE_NAME
```

- 根据文件创建一个环境

```shell
conda env create -f $FILE_NAME
```

- 列出所有环境

```shell
conda info --envs
```

有时需要与其他人共享环境信息或在多台计算机上使用环境信息。为此，可以使用 `conda env export` 将已安装的软件包列表导出到文件中。但是，默认情况下，这仅适用于同一操作系统，因为**构建版本**是在生成的 yaml 文件中指定的。 但是，可以删除它们以仅通过 `--no-builds` 标志指定包版本：

```shell
conda env export --no-builds > base.yml
```
