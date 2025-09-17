import pygame, sys, os, re

from createbeats import beatarray

from utils import resource_path

# --- Get the folder where THIS script is located ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Assets folder path ---
ASSETS = os.path.join("assets", BASE_DIR)

# --- Assigns the window of time (in ms) around the note's schedule time for where a hit is valid ---
hit_window = 50

# --- Assigns width and height of the game screen ---
screen_width = 800
screen_height = 800

# --- Designates the frame rate as 60 fps ---
frames_per_second = 60

# --- Delays the start of the game ---
start_time = None
ready_delay = 3000 #3000ms = 3 seconds
music_started = False


white = (255, 255, 255)
black = (0, 0, 0)


position_a = 187
position_b = 258
position_c = 329
position_d = 400
position_e = 471
position_f = 542

# --- Configures certain game features --- 
speed = 3
visual_latency = 125
pixels_per_second = speed * frames_per_second


strum_position = 500

# --- Intializes game ---
pygame.init()

# --- Creates a font object that can render text
font = pygame.font.SysFont("Arial", 35, bold=True)

# --- Sets the display ---
screen = pygame.display.set_mode((screen_width, screen_height))

# ---  Loads the keyboard-like image for the game ---
strum = pygame.image.load(resource_path("assets/notestrum.png"))

# --- Loads the yellow bar to correspond with a button press during game ---
pressed = pygame.image.load(resource_path("assets/pressed.png"))

# --- Draws the title of the game ---
pygame.display.set_caption('VG Rhythm Game')

# --- Creates a background image ---
background = pygame.image.load(resource_path("assets/headphones_lady.jpg"))
background = pygame.transform.scale(background, (screen_width, screen_height))

# --- Retrives songs from song list subfolder ---
songs_folder = resource_path(os.path.join("assets/song list"))

class Button():
    """
    Represents a clickable text button for menus.
    Handles hover color change, click detection, and drawing.
    """
    def __init__(self, pos, text_input, font, base_color, hover_color, file_name = None):
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hover_color = base_color, hover_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.file_name = file_name

    # --- Updates screen to display text ---
    def update(self, screen):
        screen.blit(self.text, self.text_rect)

    # --- Checks for player input ---
    def checkForInput(self, position):
        if position[0] in range (self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
   

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
   
    def checkHover(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False


def main_menu():
    # --- fonts created once here ---
    title_font = pygame.font.SysFont("Roboto", 100)
    button_font = pygame.font.SysFont("Roboto", 80)
    controls_font = pygame.font.SysFont("Roboto", 26)   # --- smaller instructions font
    accent_color = "#ff5c5c"

    play_button = Button(pos=(400, 250), text_input="Play", font=button_font, base_color="#60d4fc", hover_color="white")
    quit_button = Button(pos=(400, 400), text_input="Quit", font=button_font, base_color="#60d4fc", hover_color="white")

    # --- pre-render title so we can center it ---
    menu_text = title_font.render("VG Rhythm Game", True, accent_color)
    menu_rect = menu_text.get_rect(center=(screen_width // 2, 100))

    # --- controls text lines ---
    controls_lines = [
        "While the music plays and the blocks fall,",
        "hit the button for the corresponding lane to get a hit.",
        "From left to right, the keys are: 1, 2, 3, 8, 9, and 0.",
        "Try to get a high score!"
    ]
    # --- pre-render controls surfaces ---
    controls_surfaces = [controls_font.render(line, True, (0, 0, 0)) for line in controls_lines]

    while True:
        # --- sets background image and static menu elements ---
        screen.blit(background, (0, 0))
        screen.blit(menu_text, menu_rect)

        pos = pygame.mouse.get_pos()

        # --- draw buttons ---
        play_button.changeColor(pos)
        play_button.update(screen)

        quit_button.changeColor(pos)
        quit_button.update(screen)

        # --- draw controls centered under the buttons/title ---
        start_y = 500  # y coordinate for first controls line (tweak if needed)
        spacing = 30   # vertical spacing between control lines
        for i, surf in enumerate(controls_surfaces):
            rect = surf.get_rect(center=(screen_width // 2, start_y + i * spacing))
            screen.blit(surf, rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.checkForInput(pos):
                    song_selection_menu()
                elif quit_button.checkForInput(pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def extract_number(filename):
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else float('inf')

def get_song_list():
    songs_folder = resource_path(os.path.join("assets", "song list"))

    if os.path.exists(songs_folder):
        song_files = [f for f in os.listdir(songs_folder) if f.lower().endswith((".mp3", ".wav"))]
        return sorted(song_files, key=extract_number)
    else:
        return []

# --- Prints song selection menu and displays available songs ---
def song_selection_menu():
    songs = get_song_list()
    print("Songs in game menu:", songs)
    song_buttons = []
    for idx, song in enumerate(songs):
        y = 100 + idx * 60
        song_buttons.append(Button(pos=(400, y), text_input=song, font=pygame.font.SysFont("Roboto", 30), base_color="#88fc5c", hover_color="white", file_name=song))
        
    while True:
        screen.blit(background, (0, 0))
        pos = pygame.mouse.get_pos()

        for button in song_buttons:
            button.changeColor(pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in song_buttons:
                    if button.checkForInput(pos):
                        initialize(os.path.join(songs_folder, button.file_name))

            pygame.display.update()


class Note(pygame.sprite.Sprite):
    def __init__(self, identity, strumTime, position):
        pygame.sprite.Sprite.__init__(self)
        self.idnum = identity
        self.strum = strumTime
        self.miss = False
        self.hit = False
        self.difference = -2000000

        # --- Assigns noteA to lane 1 ---
        if position == 1:
            self.image = pygame.image.load(resource_path("assets/noteA.png"))
            self.rect = self.image.get_rect()
            self.rect.move_ip(position_a, -100)

        # --- Assigns noteB to lane 2 --- 
        if position == 2:
           self.image = pygame.image.load(resource_path("assets/noteB.png"))
           self.rect = self.image.get_rect()
           self.rect.move_ip(position_b, -100)

        # --- Assigns noteC to lane 3 ---
        if position == 3:
            self.image = pygame.image.load(resource_path("assets/noteC.png"))
            self.rect = self.image.get_rect()
            self.rect.move_ip(position_c, -100)

        # --- Assigns noteC to lane 4 ---
        if position == 4:
            self.image = pygame.image.load(resource_path("assets/noteC.png"))
            self.rect = self.image.get_rect()
            self.rect.move_ip(position_d, -100)

        # --- Assigns noteB to lane 5 ---
        if position == 5:
            self.image = pygame.image.load(resource_path("assets/noteB.png"))
            self.rect = self.image.get_rect()
            self.rect.move_ip(position_e, -100)

        # --- Assigns noteA to lane 6 ---
        if position == 6:
            self.image = pygame.image.load(resource_path("assets/noteA.png"))
            self.rect = self.image.get_rect()
            self.rect.move_ip(position_f, -100)
   
    def update(self, time):
        try:
            self.difference = self.strum - time
        
        except:
            self.difference = self.strum

        # --- move: compute pixels from time remaining ---
        time_left = self.difference
        self.rect.centery = strum_position - (time_left / 1000.0) * pixels_per_second
    
        if not self.hit and not self.miss and self.rect.centery > 520:
            self.miss = True
            self.difference = -1000000

# --- Combo counter ---
def combo_count(amount):
    font = pygame.font.SysFont("Roboto", 40)
    text = font.render( f"Combo: {amount}", True, white)
    screen.blit(text, (20, 20))

# --- Multiplier counter ---
def multiplier_count(amount):
    font = pygame.font.SysFont("Roboto", 40)
    text = font.render( f"{amount}x", True, white)
    screen.blit(text, (20, 50))

# --- Score counter ---
def score_count(score_amount):
    font = pygame.font.SysFont("Roboto", 40)
    text = font.render(f"{score_amount}", True, white)
    screen.blit(text, (630, 20))


def initialize(audio_file_name):
    print('Loading...')

    audio_path = resource_path(os.path.join(songs_folder, audio_file_name))
    print("Trying to load:", audio_path)
    print("Exists?", os.path.isfile(audio_path))

    try:
        beatmap, ending_time = beatarray(audio_path)
        print("Number of beats loaded:", len(beatmap))
    except Exception as e:
        print('Unable to read audio file:', e)
        main_menu()
        return

    game_loop(audio_path, beatmap, ending_time)

# --- Displays a  "Congratulations" screen with the final score ---
# --- Waits for player to press ENTER before returning to the main menu ---
def congratulations_screen(final_score):
    # --- sets background image ---
    screen.blit(background, (0, 0))
    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 48)

    text1 = font_big.render("Congratulations!", True, (255, 215, 0))  # gold color
    text2 = font_small.render(f"Your Final Score: {final_score}", True, (255, 255, 255))
    text3 = font_small.render("Press ENTER to return to menu", True, (200, 200, 200))

    # --- center text ---
    rect1 = text1.get_rect(center=(screen_width // 2, screen_height // 3))
    rect2 = text2.get_rect(center=(screen_width // 2, screen_height // 2))
    rect3 = text3.get_rect(center=(screen_width // 2, screen_height // 1.5))

    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    screen.blit(text3, rect3)

    pygame.display.flip()

    # --- Wait for user input ---
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


# --- Runs the game ---
def game_loop(file_name, beatmap, ending_time):
    global start_time, music_started
    start_time = None
    music_started = False # --- resets each game
    clock = pygame.time.Clock()

    running = True

    pygame.mixer.music.load(resource_path(file_name))
    pygame.mixer.music.set_volume(0.1)

    combo = 0
    score = 0
    multiplier = 1

    keypress1 = keypress2 = keypress3 = False
    keypressone = keypresstwo = keypressthree = False

    # --- Sprite groups for each lane ---
    notesA = pygame.sprite.Group()
    notesB = pygame.sprite.Group()
    notesC = pygame.sprite.Group()
    notesD = pygame.sprite.Group()
    notesE = pygame.sprite.Group()
    notesF = pygame.sprite.Group()

    # --- Adds the respective notes for the game ---
    note_dict = {
        1: notesA.add,
        2: notesB.add,
        3: notesC.add,
        4: notesD.add,
        5: notesE.add,
        6: notesF.add,
    }


    for idx, beat in enumerate(beatmap):
        timing = beat['time']
        position = beat['position']
        note_dict[position] 
        note = Note(idx, timing, position)

        if position in note_dict:
            note_dict[position](note)
        
        # --- Debug: confirm spawn ---
        else:
            print(f"Spawned Note {note.idnum} at time={timing}, position={position}")

    print('Loading Done!')

    current = 0
    previousframetime = 0
    lastplayheadposition = 0
    mostaccurate = 0

    while True:
        # --- Sets a timestap if game has started ---
        if start_time is None:
            start_time = pygame.time.get_ticks()

        # --- Checks if  delay has passed ---
        elapsed = pygame.time.get_ticks() - start_time
        
        # --- sets background image ---
        screen.blit(background, (0, 0))

        if elapsed < ready_delay:
            ready_text = font.render("Get Ready!", True, (255, 255, 255))
            rect = ready_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(ready_text, rect)
        else:
            # --- Only after delay should notes be generated and fall ---
            if not music_started:
                pygame.mixer.music.play()
                clock = pygame.time.Clock()
                music_started = True

            # --- event handling for when a button is pressed in-game ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: 
                        keypress1 = True
                        
                    elif event.key == pygame.K_2:
                        keypress2 = True
                        
                    elif event.key == pygame.K_3:
                        keypress3 = True
                        
                    elif event.key == pygame.K_KP1:
                        keypressone = True
                        
                    elif event.key == pygame.K_KP2:
                        keypresstwo = True
                        
                    elif event.key == pygame.K_KP3:
                        keypressthree = True
                        

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_1: keypress1 = False
                    if event.key == pygame.K_2: keypress2 = False
                    if event.key == pygame.K_3: keypress3 = False
                    if event.key == pygame.K_KP1: keypressone = False
                    if event.key == pygame.K_KP2: keypresstwo = False
                    if event.key == pygame.K_KP3: keypressthree = False

            # --- timing --- 
            current += clock.get_time()
            if current >= ending_time:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                congratulations_screen(score)
                main_menu()

            mostaccurate += current - previousframetime
            previousframetime = current
            songtime = pygame.mixer.music.get_pos()
            if songtime != lastplayheadposition:
                mostaccurate = (mostaccurate + songtime) / 2
                lastplayheadposition = songtime

            # ---  multiplier logic --- 
            if combo < 10:
                multiplier = 1
            elif 10 <= combo < 20:
                multiplier = 2
            elif 20 <= combo < 30:
                multiplier = 3
            else:
                multiplier = 4

            # --- draw UI --- 
            combo_count(combo)
            multiplier_count(multiplier)
            score_count(score)

            if keypress1: screen.blit(pressed, (position_a, 494))
            if keypress2: screen.blit(pressed, (position_b, 494))
            if keypress3: screen.blit(pressed, (position_c, 494))
            if keypressone: screen.blit(pressed, (position_d, 494))
            if keypresstwo: screen.blit(pressed, (position_e, 494))
            if keypressthree: screen.blit(pressed, (position_f, 494))

            # --- Draw notes ---
            for group in (notesA, notesB, notesC, notesD, notesE, notesF):
                group.draw(screen)
            screen.blit(strum, (0, 0))

            # --- move notes --- 
            for group in (notesA, notesB, notesC, notesD, notesE, notesF):
                for note in group:
                    distance = strum_position - (note.strum / speed - mostaccurate / speed) + visual_latency
                    # note.move(distance)
                    #print(f"Note {note.idnum} | y={note.rect.centery} | diff={note.difference} | hit={note.hit} | miss={note.miss}")

            # --- update groups --- 
            notesA.update(mostaccurate)
            notesB.update(mostaccurate)
            notesC.update(mostaccurate)
            notesD.update(mostaccurate)
            notesE.update(mostaccurate)
            notesF.update(mostaccurate)

            lane_keys = [
                (keypress1, notesA),
                (keypress2, notesB),
                (keypress3, notesC),
                (keypressone, notesD),
                (keypresstwo, notesE),
                (keypressthree, notesF),
            ]

            for key_pressed, group in lane_keys:
                if key_pressed:
                    for note in group:
                        delta = abs(mostaccurate - note.strum)
                        if delta <= hit_window and not note.hit and not note.miss:
                            note.hit = True
                            note.kill()
                            combo += 1
                            score += 100 * multiplier
                            break

            # --- score + cleanup ---
            def process_lane(group):
                nonlocal combo
                for note in list(group):  
                    if note.miss:
                        combo = 0
                        note.kill()

            for g in (notesA, notesB, notesC, notesD, notesE, notesF):
                process_lane(g)

            # --- flip screen --- 
            pygame.display.update()
            clock.tick(frames_per_second)


if __name__ == '__main__':
    try:
        main_menu()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
       
               


