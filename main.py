import pygame
import math
import random

# Initialise Pygame
pygame.init()

# Setup display
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Educational Hangman Game!")

# Button variables
RADIUS = round((WIDTH - HEIGHT) / 26)
GAP = round(WIDTH / 52)
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = round(HEIGHT - HEIGHT / 4)

# Draw letters inside buttons
A = 65 
for i in range(26):
      x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
      y = starty + ((i // 13) * (GAP + RADIUS * 2))
      letters.append([x, y, chr(A + i), True])

# Colour variables
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (125, 125, 125)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Load fonts
LETTER_FONT = pygame.font.SysFont('comicsans', round(RADIUS), 1)
WORD_FONT = pygame.font.SysFont('comicsans', round(WIDTH / 30))
TITLE_FONT = pygame.font.SysFont('comicsans', round(WIDTH / 26))
SUBTITLE_FONT = pygame.font.SysFont('comicsans',round(WIDTH / 78))
BUTTON_FONT = pygame.font.SysFont('ariel', round(WIDTH / 22))

# Load hangman images
images = []
image_directory = "assets/"

for i in range(10):
      image = pygame.image.load(image_directory + "hangman" + str(i) + ".png")
      image = pygame.transform.scale(image, (image.get_width() * WIDTH / 1000, image.get_height() * WIDTH / 1000))
      images.append(image)

# Game variables
hangman_status = 0
words = ["NULL"]
word = random.choice(words)
guessed = []
difficulty = 0
current_state = "menu"

# Stat variables
win_amount = 0
lose_amount = 0

# Draw title function
def draw_title():
      text = TITLE_FONT.render("H A N G M A N   G A M E", 1, BLACK)
      text_x = WIDTH/2 - text.get_width()/2
      text_y = 20
      win.blit(text, (text_x, text_y))
      pygame.draw.line(win, BLACK, (text_x, text_y + text.get_height() + 10), (text_x + text.get_width(), text_y + text.get_height() + 10), 5)

      # Draw credit text if in menu
      if current_state == "menu":
            subtext = SUBTITLE_FONT.render("By: Kaleb Vong 11SENG1", 1, BLACK)
            win.blit(subtext, ((text_x + text.get_width()) / 1.7, text_y + text.get_height() + 20))
      
      # Display chosen difficulty when in game
      elif current_state == "game":
            subtext = SUBTITLE_FONT.render("Difficulty: ", 1, BLACK)
            win.blit(subtext, ((text_x + text.get_width()) / 1.75, text_y + text.get_height() + 20))
            if difficulty == 0:
                  subtext2 = SUBTITLE_FONT.render("EASY MODE", 1, GREEN)
                  win.blit(subtext2, ((text_x + text.get_width()) / 1.48, text_y + text.get_height() + 20))
            elif difficulty == 1:
                  subtext2 = SUBTITLE_FONT.render("MEDIUM MODE", 1, YELLOW)
                  win.blit(subtext2, ((text_x + text.get_width()) / 1.48, text_y + text.get_height() + 20))
            elif difficulty == 2:
                  subtext2 = SUBTITLE_FONT.render("HARD MODE", 1, RED)
                  win.blit(subtext2, ((text_x + text.get_width()) / 1.48, text_y + text.get_height() + 20))

# Select word function
def choose_word():
      global word

      # select word list corresponding to difficulty to choose random word from
      if difficulty == 0:
            with open('word_lists/easy.txt', 'r') as file:
                  words = [line.strip() for line in file]
      elif difficulty == 1:
            with open('word_lists/medium.txt', 'r') as file:
                  words = [line.strip() for line in file]
      elif difficulty == 2:
            with open('word_lists/hard.txt', 'r') as file:
                  words = [line.strip() for line in file]

      # Modify global word variable with selected word
      word = random.choice(words)

# Draw function
def draw():
      global word
      win.fill(WHITE)
      draw_title()

      # Display stats
      stats()

      # Draw main word
      display_word = ""
      for letter in word:
            if letter in guessed:
                  display_word += letter + " "
            else:
                  display_word += "_ "
      text = WORD_FONT.render(display_word, 1, BLACK)
      win.blit(text, (WIDTH / 2.2, HEIGHT / 3))

      # Draw clickable buttons
      for letter in letters:
            x, y, ltr, visible = letter
            if visible:
                  pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
                  text = LETTER_FONT.render(ltr, 1, BLACK)
                  win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

      win.blit(images[hangman_status], (WIDTH / 4.5, HEIGHT / 5.5))
      
      # Draw back button
      back = pygame.image.load("assets/back.png")
      back = pygame.transform.scale(back, (WIDTH / 10, HEIGHT / 8))
      win.blit(back, (20, 20))

      pygame.display.update()

# End screen function
def display_message(message):
      pygame.time.delay(1000)
      win.fill(WHITE)
      text = WORD_FONT.render(message, 1, BLACK)
      win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
      pygame.display.update()
      pygame.time.delay(3000)

# Menu function
def menu():
      win.fill(WHITE)
      draw_title()
      stats()

      # Draw buttons
      pygame.draw.rect(win, GRAY, (WIDTH / 6, HEIGHT / 3.5, round(WIDTH / 1.5), round(HEIGHT / 10)), width=0)
      pygame.draw.rect(win, GRAY, (WIDTH / 6, HEIGHT / 2.2, round(WIDTH / 1.5), round(HEIGHT / 10)), width=0)
      pygame.draw.rect(win, GRAY, (WIDTH / 6, HEIGHT / 1.6, round(WIDTH / 1.5), round(HEIGHT / 10)), width=0)

      # Label buttons
      text = BUTTON_FONT.render("P L A Y", 1, WHITE)
      win.blit(text, ((WIDTH / 1.65) - (WIDTH / 6), (HEIGHT / 3.5) + 40))
      text2 = BUTTON_FONT.render("DIFFICULTY:", 1, WHITE)
      win.blit(text2, ((WIDTH / 1.65) - (WIDTH / 3.5), (HEIGHT / 2.2) + 40))
      text3 = BUTTON_FONT.render("Q U I T", 1, WHITE)
      win.blit(text3, ((WIDTH / 1.65) - (WIDTH / 6), (HEIGHT / 1.6) + 40))

      # Set default difficulty
      diff_name("E A S Y", GREEN)

      # Update display
      pygame.display.update()

# Display difficulty function
def diff_name(difficulty_name, color):
      pygame.draw.rect(win, GRAY, (WIDTH / 1.91, HEIGHT / 2.2, round(WIDTH / 6), round(HEIGHT / 10)), width=0)
      text = BUTTON_FONT.render(difficulty_name, 1, color)
      win.blit(text, ((WIDTH / 1.65) - (WIDTH / 12), (HEIGHT / 2.2) + 40))
      pygame.display.update()

# Display stats function
def stats():
      # import stat variables
      global win_amount, lose_amount

      # Draw wins and losses message
      text = SUBTITLE_FONT.render("W I N S : ", 1, BLACK)
      win.blit(text, (WIDTH / 2.9, HEIGHT / 1.1))

      text2 = SUBTITLE_FONT.render("L O S S E S : ", 1, BLACK)
      win.blit(text2, (WIDTH / 1.8, HEIGHT / 1.1))
      
      # Draw number of wins and losses
      text = SUBTITLE_FONT.render(str(win_amount), 1, GREEN)
      win.blit(text, (WIDTH / 2.43, HEIGHT / 1.1))

      text = SUBTITLE_FONT.render(str(lose_amount), 1, RED)
      win.blit(text, (WIDTH / 1.55, HEIGHT / 1.1))

# Main function
def main():
      # import variables
      global hangman_status, difficulty, word, guessed, current_state

      # import stats
      global win_amount, lose_amount

      # Main game variables
      FPS = 60
      clock = pygame.time.Clock()
      run = True
      shown_warning = 0

      # Menu variables
      menu()
      current_state = "menu"

      # Draw bounding boxes for menu buttons
      quit_rect = pygame.Rect(WIDTH / 6, HEIGHT / 1.6, round(WIDTH / 1.5), round(HEIGHT / 10))
      diff_rect = pygame.Rect(WIDTH / 6, HEIGHT / 2.2, round(WIDTH / 1.5), round(HEIGHT / 10))
      play_rect = pygame.Rect(WIDTH / 6, HEIGHT / 3.5, round(WIDTH / 1.5), round(HEIGHT / 10))

      # Draw bounding box for back button
      back_rect = pygame.Rect(20, 20, WIDTH / 10, HEIGHT / 8)

      # Setup main game loop
      while run:
            clock.tick(FPS)

            # Detect for quit
            for event in pygame.event.get():
                  if event.type == pygame.QUIT:
                        run = False

                  # Detect left click
                  if event.type == pygame.MOUSEBUTTONDOWN:
                        m_x, m_y = pygame.mouse.get_pos()
                        if current_state == "menu":
                              # Quit button functionality
                              if quit_rect.collidepoint(m_x, m_y):
                                    run = False
                              # Difficulty button functionality
                              if diff_rect.collidepoint(m_x, m_y):
                                    difficulty += 1
                                    if difficulty > 2:
                                          difficulty = 0
                                    # Display difficulty on button corresponding to variable value
                                    if difficulty == 0:
                                          diff_name("E A S Y", GREEN)
                                    elif difficulty == 1:
                                          diff_name("M E D I U M", YELLOW)
                                    elif difficulty == 2:
                                          diff_name("H A R D", RED)
                              # Play button functionality
                              if play_rect.collidepoint(m_x, m_y):
                                    current_state = "game"
                                    choose_word()
                                    draw()

                        # Game button functionality
                        elif current_state == "game":
                              for letter in letters:
                                    x, y, ltr, visible = letter
                                    if visible:
                                          dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                                          if dis < RADIUS:
                                                letter[3] = False
                                                guessed.append(ltr)
                                                if ltr not in word:
                                                      hangman_status += 1
                              draw()

                              # Back button functionality
                              if back_rect.collidepoint(m_x, m_y):
                                    if shown_warning == 1:
                                          # increase lose amounts variable
                                          lose_amount += 1

                                          # Go back on second click
                                          guessed = []
                                          difficulty = 0
                                          hangman_status = 0
                                          for letter in letters:
                                                letter[3] = True
                                          current_state = "menu"
                                          menu()

                                          # Reset shown warning variable
                                          shown_warning = 0

                                    # Display warning on first click
                                    if shown_warning == 0 and current_state == "game":
                                          text = SUBTITLE_FONT.render("WARNING! Going back will count as a LOSS", 1, RED)
                                          win.blit(text, (20, 220))
                                          text = SUBTITLE_FONT.render("Click again to continue anyways...", 1, GRAY)
                                          win.blit(text, (20, 260))
                                          pygame.display.update()
                                          shown_warning += 1

                              # Reset warning status when clicking anywhere
                              if shown_warning == 1 and not back_rect.collidepoint(m_x, m_y):
                                    shown_warning = 0

            # Draw endscreen when won or lost
            won = True
            for letter in word:
                  if letter not in guessed:
                        won = False
                        break

            if won:
                  # Display win message
                  display_message("You WON!")

                  # increase win amounts variable
                  win_amount += 1

                  # Reset game variables
                  guessed = []
                  difficulty = 0
                  hangman_status = 0
                  for letter in letters:
                        letter[3] = True
                  current_state = "menu"
                  menu()

            if hangman_status == 9:
                  # Display lose message
                  display_message("You LOST!")

                  # increase lose amounts variable
                  lose_amount += 1

                  # Reset game variables
                  guessed = []
                  difficulty = 0
                  hangman_status = 0
                  for letter in letters:
                        letter[3] = True
                  current_state = "menu"
                  menu()


main()
pygame.quit()