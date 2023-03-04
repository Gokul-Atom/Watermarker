# watermarking-app
A watermarking app developed with pillow and tkinter, with font choices and layers. It also supports keyboard shortcuts.

![](https://img.shields.io/badge/python-v3.9.5-blue) ![](https://img.shields.io/badge/Pillow-v8.3.1-yellowgreen)

## Technologies Used
### Languages Used
* Python 3.9.5

### Modules Used
* Sys
* Tkinter
* PIL (Pillow) 8.3.1

## Modules Installation
PIL is not pre-installed with python.

To install this module, type the following command in terminal.

```
pip install pillow==8.3.1
```
or use the requirements.txt file

```
pip install -r requirements.txt
```

## Instructions
* **Run** the program.
* A new window will be opened.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2001.png)

* Click **Open Image** button on the **right side of the viewport** to open the image for watermarking.
* Check **keyboard shortcuts** below in **Shortcuts** section.
* Once the image is opened, the top bar in window is already populated with some default properties.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2002.png)

* The properties from left to right are **X Co-ordinate**, **Y Co-ordinate** textbox in pixels, **Font Style** drop-down combo-box, **Font Size** spinbox, **Watermark Color** color-picker, **Watermark Text** textbox and **Create Watermark** button.
* Then edit the properties, to match watermark preferences and click **Create Watermark** button.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2003.png)

* Watermark will then be placed on the image.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2004.png)

* Once the watermark is placed, it can further be edited by using **EDIT WATERMARK** section on bottom right of the window.
* Many watermarks can be placed on the image and each watermark can be found as layer on the **Watermark Layers** section.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2005.png)

* The active watermark will be highlighted both in **Watermark Layers** section and **viewport**.
* Previously added watermark can be edited by selecting the watermark from **Watermark Layers** section to make it active watermark and using **EDIT WATERMARK** section.
* Active watermark can be removed by using **Remove** button which can be found below **Watermark Layers** section.
* All watermarks can be removed by using **Remove All** button which can be found next to **Remove** button.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2008.png)

* Once all watermarks are removed, the border indicating position of the last active watermark can still be seen on the viewport.
* Don't worry, this is **not reflected** in the final output image.
* After all watermarks are added, the image can be previewed for any adjustments by clicking **Preview Image** button.
* Once the result is satisfactory, the final image can saved by clicking **Save Image** button.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2006.png)

* The watermark resolution may **decrease** based on the **resolution** of the used image.
* In the final output (see below), watermark looks **blurry** because the **resolution** of the image is **lower**.

![](https://github.com/Gokul-Atom/watermarking-app/blob/main/Screenshots/screenshot%2007.png)

## Keyboard Shortcuts
Hotkey | Function
-|-
Esc | Removes focus from the active element
Ctrl + N | Open new image
Alt + N | Create new watermark
Ctrl + S | Save image
Ctrl + P | Preview image
Ctrl + Q | Exit program
Del | Delete active watermark
Ctrl + Del | Deletes all watermark
{ | Decrease font size
} | Increase font size
Shift + &uarr; | Move up by 1 px
Shift + &darr; | Move down by 1 px
Shift + &larr; | Move left by  px
Shift + &rarr; | Move right by 1 px
Ctrl + &uarr; | Move up by 5 px
Ctrl + &darr; | Move down by 5 px
Ctrl + &larr; | Move left by 5 px
Ctrl + &rarr; | Move right by 5 px
Ctrl + I | Open color picker

## License
This repository is licensed under GNU General Public License family.

![](https://img.shields.io/badge/License-GPL-color)
