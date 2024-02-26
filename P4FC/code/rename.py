"""
@Title        : 
@Author(s)    : Stephen CUI
@LastEditor(s): Stephen CUI
@CreatedTime  : 2023-12-09 13:32:10
@Description  : 
"""
import os

for file in os.listdir():
    os.rename(file, file.lower().replace(' ', '_'))
