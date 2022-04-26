import os
import keyboard
import datetime

from PIL import ImageGrab
from tkinter import Tk, Canvas


class ScreenShot:
    def __init__(self, file_name, file_type, output_path, region=None):
        self._name = f"{file_name}.{file_type}"
        self._path = os.path.normpath(f"{output_path}\\{self._name}")

        self._region = region

        self._screenshot_image = None

    def save(self):
        if self._region is not None:
            self._screenshot_image = ImageGrab.grab(bbox=self._region)
        else:
            self._screenshot_image = ImageGrab.grab()

        self._screenshot_image.save(self._path)


class SelectionArea:
    def __init__(self):
        self.__canCreateCond = False
        self.x_0, self.y_0, self.x_1, self.y_1 = None, None, None, None

        self.__root = Tk()
        self.__screenwidth, self.__screenheight = self.__root.winfo_screenwidth(), self.__root.winfo_screenheight()
        self.__canvas = Canvas(self.__root, width=self.__screenwidth,
                               height=self.__screenheight, background="#2F2F2F",
                               borderwidth=0)

        self.__root.overrideredirect(True)
        self.__root.geometry(f"{self.__screenwidth}x{self.__screenheight}+0+0")
        self.__root.config(background="red")
        self.__root.wm_attributes("-topmost", True)
        self.__root.wm_attributes("-alpha", 0.25)
        self.__root.wm_attributes("-transparentcolor", "red")

        self.__bind()

        self.__canvas.place(x=-2, y=-2)
        self.__root.mainloop()

    def __selectStart(self, event=None):
        self.x_0, self.y_0, self.x_1, self.y_1 = event.x, event.y, event.x, event.y

        self.__canvasCreate()

    def __selectEnd(self, event=None):
        self.x_1, self.y_1 = event.x, event.y

        self.__canvasUpdate()

    def __selectComplete(self, event=None):
        self.x_1, self.y_1 = event.x, event.y

        self.__root.destroy()

    def __bind(self):
        self.__root.bind("<Button-1>", self.__selectStart)
        self.__root.bind("<B1-Motion>", self.__selectEnd)
        self.__root.bind("<ButtonRelease-1>", self.__selectComplete)

    def __canvasCreate(self):
        self.__canCreateCond = True

        self.__canvas = Canvas(self.__root, width=self.__screenwidth,
                               height=self.__screenheight, background="#2F2F2F",
                               borderwidth=0)
        self.__canvas.create_rectangle(self.x_0, self.y_0, self.x_1, self.y_1, fill="red")
        self.__canvas.place(x=-2, y=-2)

    def __canvasUpdate(self):
        if self.__canCreateCond:
            self.__canvas.destroy()

        self.__canvas = Canvas(self.__root, width=self.__screenwidth,
                               height=self.__screenheight, background="#2F2F2F",
                               borderwidth=0)
        self.__canvas.create_rectangle(self.x_0, self.y_0, self.x_1, self.y_1, fill="red")
        self.__canvas.place(x=-2, y=-2)

    def get(self):
        if self.x_0 > self.x_1:
            self.x_0, self.x_1 = self.x_1, self.x_0
        if self.y_0 > self.y_1:
            self.y_0, self.y_1 = self.y_1, self.y_0

        if self.x_1 > self.__screenwidth:
            self.x_1 -= (self.x_1 - self.__screenwidth)
        if self.y_1 > self.__screenheight:
            self.y_1 -= (self.y_1 - self.__screenheight)

        return self.x_0, self.y_0, self.x_1, self.y_1


class Main:
    def __init__(self):
        self.__outputPath = os.path.normpath(f"{os.getenv('USERPROFILE')}\\Pictures\\Vito Screenshots")
        self.__allScreenshotHotkey = "ctrl+shift+s"
        self.__selectScreenshotHotkey = "ctrl+shift+x"

        self.__createOutputFolder(
            path=self.__outputPath
        )

        self.__bindKeyboard()

    def __screenshotAllScreen(self):
        screenshot = ScreenShot(
            file_name=self.__getFileName(),
            file_type="png",
            output_path=os.path.normpath(f"{os.getenv('USERPROFILE')}\\Pictures\\Vito Screenshots")
        )

        screenshot.save()

    def __screenshotSelectScreen(self):
        selection_area = SelectionArea()

        screenshot = ScreenShot(
            file_name=self.__getFileName(),
            file_type="png",
            output_path=os.path.normpath(f"{os.getenv('USERPROFILE')}\\Pictures\\Vito Screenshots"),
            region=selection_area.get()
        )

        screenshot.save()

    def __bindKeyboard(self):
        keyboard.add_hotkey(self.__allScreenshotHotkey, self.__screenshotAllScreen)
        keyboard.add_hotkey(self.__selectScreenshotHotkey, self.__screenshotSelectScreen)

        keyboard.wait()

    @staticmethod
    def __getFileName():
        time = datetime.datetime.now()

        return f"Vito_{time.strftime('%d-%m-%Y_%H-%M-%S')}"

    @staticmethod
    def __createOutputFolder(path: str):
        if not os.path.exists(path):
            os.mkdir(path)


if __name__ == '__main__':
    app = Main()
