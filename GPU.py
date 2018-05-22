

class GPU:
    def __init__(self, pixel_size, tkinter):
        self.width = 64
        self.height = 32
        self.pixel_size = pixel_size
        try:
            self.master = tkinter.Tk()
            self.window = tkinter.Canvas(self.master, width=self.width * self.pixel_size, height=self.height * self.pixel_size)
        except:
            pass
        self.pixels = []
        self.memory = []
        for x in range(self.width):
            self.pixels.append([])
            self.memory.append([])
            for y in range(self.height):
                try:
                    element = self.window.create_rectangle(x * self.pixel_size, y * self.pixel_size,
                                                       (x + 1) * self.pixel_size, (y + 1) * self.pixel_size,
                                                       fill="black", width=0)
                    self.pixels[x].append(element)
                except:
                    pass
                self.memory[x].append(0)

    def main(self):
        try:
            self.window.pack()
        except:
            pass

    def clear_screen(self):
        """
        Checks each pixel, and if pixel is sets to 1, it will be set to 0 and updated
        """
        for x in range(self.width):
            for y in range(self.height):
                if self.memory[x][y] != 0:
                    self.memory[x][y] = 0
                    self.update_pixel(x, y)

    def update_pixel(self, pixel_x, pixel_y):
        """
        Sets pixel in coords (pixel_x, pixel_y) to value, stored in memory (pixel_x, pixel_y
        :param pixel_x: pixel X coordinate
        :param pixel_y: pixel Y coordinate
        """
        if self.memory[pixel_x][pixel_y] == 0:
            color = "black"
        else:
            color = "white"
        try:
            self.window.itemconfig(self.pixels[pixel_x][pixel_y], fill=color)
        except:
            pass

    def draw_sprite(self, x, y, sprite):
        """
        Draws a sprite at coordinate (x, y) that has a width of 8 pixels.
        :param x: X coordinate of the start of the sprite drawing
        :param y: Y coordinate of the start of the sprite drawing
        :param sprite: Bit-coded sprite
        :return: 1 if any screen pixels are flipped from set to unset when the sprite is drawn,
        and to 0 if that doesn’t happen
        """
        output = 0
        for sprite_y in range(len(sprite)):
            for sprite_x in range(len(sprite[sprite_y])):  # Sprite is reversed
                if x + sprite_x >= self.width or y + sprite_y >= self.height:
                    continue
                if self.memory[x + sprite_x][y + sprite_y] == 1 and int(sprite[sprite_y][sprite_x]) == 1:
                    output = 1
                self.memory[x + sprite_x][y + sprite_y] ^= int(sprite[sprite_y][sprite_x])
                self.update_pixel(x + sprite_x, y + sprite_y)
        return output
