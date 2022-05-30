# Voice Record program
<p align="center"><img src="eyenix.ico" title="로고" alt="EYENIX"></img></p>
Voice Recored for Speech Classification Model  

## Development Environment

* window10
* python 3.8
* PYCHARM

## Module

- Just run build.sh
```bash
./build.sh
```

## How to make exe program


```bash
pyinstaller -F -n voice_record.exe main.py --noconsole --icon eyenix.ico --add-data "eyenix.ico;."
```

## DEMO
- Just run voice_record.exe  

- GIF
![demo](https://user-images.githubusercontent.com/66294848/171068617-0257a61e-34ba-408e-8671-e559954ab24f.gif)
