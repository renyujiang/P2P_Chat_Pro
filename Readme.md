# P2P Pro - EC530
This is P2P Pro project

API doc: API.md

Presentation Link: https://docs.google.com/presentation/d/1jCKI4AsXwgbstk6mi6an6p3H3BnKyAKw_XqlJ0u-bXA/edit?usp=sharing

## Requirements

### Software: 

System: macOS 13.1 or later version

Python Package: Python 3.7, PyQt5, Flask, requests

### Hardware:

CPU:    It has only been tested on Apple Silicon M1 Pro, but it should work on other Macs with Intel chips.

Memory: 8GB or more

Monitor: 1920x1080 or higher resolution (Low resolution may cause the GUI to be displayed incorrectly)

### <span style="color:red">This program's full function works on macOS only, don't run it on Windows or Linux.</span>

### <span style="color:red">This program's full function works on macOS only, don't run it on Windows or Linux.</span>

### <span style="color:red">This program's full function works on macOS only, don't run it on Windows or Linux.</span>

## Features of this program:

1. It has connection confirmation process, so you can reject connections from other clients.
2. It can send all kinds of files, including images, documents, even python codes.
3. It uses multithreading and multiprocessing, chatting with other clients is continuously, you can send as many messages as you want.
4. Moreover, the processing of connecting other clients is total automatic, you don't need to do anything, just wait for new terminals to show up.
5. Robust, chatting windows can be closed without affecting the main process and the listening thread wouldn't block the console window's main functions.

## How to use

Start with login.py, it will call other modules automatically. Remember to start central_server.py first.

If you want to use terminal to run this program, please check the API.md file.

## User Stories

1. As a user, I want to be able to send messages to other users, so that I can communicate with them. As a modern chat program, it should be able to communicate with multiple users at the same time.
2. As a user, I want to be able to send files to other users, including common formats like .docx, .pdf, .png, .jpg, .py, etc.
3. As a user, I want to be able to send images to other users.
4. As a user, I want to be able to reject connections from other users, so that I can control who I want to talk to.
5. As a user, I want a robust program, so that I can use it without worrying about it crashing.
6. As a user, I want to know how many files I store in remote storage, and what are they.

## Examples

<div style="display:flex">
  <img src="./images/MainWindow.png" width="50%" />
  <img src="./images/ChatWindow.png" width="50%" />
</div>

License
This program is released under the MIT License. See the LICENSE file for details.