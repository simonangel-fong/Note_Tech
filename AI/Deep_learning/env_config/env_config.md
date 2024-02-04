# Environment Configuration

[Back](../index.md)

---

## Install Miniconda

- Link: https://docs.conda.io/projects/miniconda/en/latest/

---

## Create new env

- open "Anaconda Prompt (miniconda3)"
- Deativate the base env

```sh
conda deactivate
```

- Create a new env

```sh
conda create --name d2l python=3.9 -y
```

---

## Install packages

- Activate new env

```sh
conda activate d2l
```

- Install PyTorch

```sh
pip install torch==2.0.0 torchvision==0.15.1
```

- Install the d2l package

```sh
pip install d2l==1.0.3
```

---

## Downloading and Running the Code

```sh
mkdir d2l-en && cd d2l-en
curl https://d2l.ai/d2l-en-1.0.3.zip -o d2l-en.zip
unzip d2l-en.zip && rm d2l-en.zip       # for linux and mac
# for windows, unzip the download file
cd pytorch
```

- start the Jupyter Notebook server

```sh
jupyter notebook
```

---

## Shortcut to Jupyter Notebook server

```sh
conda deactivate
conda activate d2l
jupyter notebook
# then navigate to pytorch folder
```

---

[TOP](#environment-configuration)
