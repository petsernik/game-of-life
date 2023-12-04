import pygame.display


class Rect:
    def __init__(self, rect=(0, 0, 0, 0)):
        self.rect = rect

    def width(self):
        return self.rect[2]

    def height(self):
        return self.rect[3]

    def pos(self):
        return self.rect[0], self.rect[1]

    def size(self):
        return self.rect[2], self.rect[3]

    def upd_pos(self, x, y):
        self.rect[0], self.rect[1] = x, y

    def upd_rect(self, x, y, w, h):
        self.rect = (x, y, w, h)

    def collide_point(self, x, y):
        return self.rect[0] <= x <= self.rect[0] + self.rect[2] \
            and self.rect[1] <= y <= self.rect[1] + self.rect[3]


def fill(surface, color):
    w, h = surface.get_size()
    for x in range(w):
        for y in range(h):
            if surface.get_at((x, y))[3] > 0:
                surface.set_at((x, y), color)


class Button(Rect):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = list(image.get_rect())
        self.hidden = False
        self.active = False
        self.__action = lambda: None

    def set_color(self, color):
        self.image = self.image.convert_alpha()
        fill(self.image, color)

    def set_action(self, action):
        self.__action = action

    def collide_point(self, x, y):
        return not self.hidden and super().collide_point(x, y)

    def blit(self):
        if not self.hidden:
            pygame.display.get_surface().blit(self.image, self.rect)

    def action(self, as_btn=True):
        if (self.active and not self.hidden) or not as_btn:
            self.__action()
        self.active = False


class Text(Rect):
    def __init__(self, render_text):
        super().__init__()
        self.text = render_text
        self.rect = list(render_text.get_rect())

    def blit(self):
        pygame.display.get_surface().blit(self.text, self.rect)


def blit_text(
        surface,
        text,
        position,
        font,
        color='black',
        word_wrap=True
):
    """
    Render multiline text onto a surface with intelligent word wrapping.

    Args:
        surface (pygame.Surface): Target surface for drawing
        text (str): Text content to render
        position (tuple): (x, y) starting coordinates
        font (pygame.font.Font): Font object for rendering
        color (tuple): RGB/RGBA text color (default: black)
        word_wrap (bool): Enable word wrapping (default: True)
    """
    start_x, start_y = position
    surface_width = surface.get_width()
    space_width, _ = font.size(' ')
    current_x, current_y = start_x, start_y
    line_height = 0  # Track maximum height in current line

    # Pre-calculate surface dimensions once
    surface_right = surface_width - start_x
    surface_bottom = surface.get_height()

    # Cache for rendered words
    word_cache = {}

    def get_word_surface(word):
        """Get cached or newly rendered word surface"""
        if word not in word_cache:
            word_cache[word] = font.render(word, True, color)
        return word_cache[word]

    def process_word(word):
        """Process a single word, handling wrapping and rendering."""
        nonlocal current_x, current_y, line_height, get_word_surface
        nonlocal surface_bottom
        word_surface = get_word_surface(word)
        word_width, word_height = word_surface.get_size()

        # Update line height
        if word_height > line_height:
            line_height = word_height

        # Handle word wrapping
        if (word_wrap and
                current_x + word_width > surface_width and
                current_x != start_x):
            current_x = start_x
            current_y += line_height
            line_height = word_height

        # Blit the word if it fits vertically
        if current_y + word_height <= surface_bottom:
            surface.blit(word_surface, (current_x, current_y))

        # Advance position
        current_x += word_width

    # Process text line-by-line
    for line in text.splitlines():
        line_words = line.split(' ')
        word_count = len(line_words)

        line_height = 0
        current_x = start_x

        for i, word in enumerate(line_words):
            # Handle words exceeding surface width
            if word_wrap and font.size(word)[0] > surface_right:
                # Split long words that can't fit even alone
                chunks = []
                current_chunk = ''
                for char in word:
                    test_chunk = current_chunk + char
                    test_width, _ = font.size(test_chunk)
                    if test_width <= surface_right:
                        current_chunk = test_chunk
                    else:
                        chunks.append(current_chunk)
                        current_chunk = char
                if current_chunk:
                    chunks.append(current_chunk)

                # Process word chunks
                for chunk in chunks:
                    process_word(chunk)
                continue

            # Process the word
            process_word(word)

            # Add space between words (except after the last word)
            if i != word_count - 1:
                current_x += space_width

        # Move to next line
        current_y += line_height


def blit_button(btn, screen):
    screen.blit(btn.image, btn.rect)
