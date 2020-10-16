import PySimpleGUI as sg

layout = [
    [sg.Button("选择文件夹"), sg.FolderBrowse()]
]
while True:
    window = sg.Window("关键词",layout)