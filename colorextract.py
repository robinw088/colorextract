from PIL import Image
import pandas as pd

class ColorExtract:
    def __init__(self, file, color_number):

        self.colors = color_number
        self.img = Image.open(file).quantize(colors=self.colors).convert()
        self.df=pd.DataFrame(self.img.getcolors(), columns=['count','rgb']).sort_values(['count'],ascending=False,ignore_index=True)
        self.df['percent']=self.df['count']/self.df['count'].sum()
        self.colors_hex = ["#{0:02x}{1:02x}{2:02x}".format(color[0], color[1], color[2]) for color in self.df['rgb']]
        self.percentage=self.df['percent'].round(decimals=4)
