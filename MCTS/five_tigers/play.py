import pygame
import sys,os
import time

import five_tigers as ft

# for pack to .exe file
if getattr(sys, 'frozen', False):
  cur_path = sys._MEIPASS
else:
  cur_path = os.path.dirname(__file__)

FONT_PATH = os.path.join(cur_path, 'resources\OpenSans-Regular.ttf')

pygame.init()
size = width, height = 900, 600

# Colors
orange = (174, 130, 44)
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

mediumFont = pygame.font.Font(FONT_PATH, 32)
largeFont = pygame.font.Font(FONT_PATH, 50)
moveFont = pygame.font.Font(FONT_PATH, 60)

user = None
ai_turn = False
mcts = ft.MCTS()
game = ft.Fiver_tigers() 
board = game.board
sign2player = {ft.X:1, ft.O:-1}


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(orange)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Five-Tigers", True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 60)
        screen.blit(title, titleRect)

        # Draw buttons
        playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 60)
        playX = mediumFont.render("Play first", True, orange)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, black, playXButton)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 60)
        playO = mediumFont.render("Play second", True, orange)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, black, playOButton)
        screen.blit(playO, playORect)
        
        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ft.X
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ft.O

    else:

        # Draw game board
        tile_size = 80
        tile_origin = (width / 2 - (2.5 * tile_size),
                    height / 2 - (2.5 * tile_size))
        line_origin = (width / 2 - (2 * tile_size),
                    height / 2 - (2 * tile_size))
        tiles = []
        for i in range(5):
            row = []
            for j in range(5):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                if i != 4 and j != 4:
                    lines = pygame.Rect(
                        line_origin[0] + j * tile_size,
                        line_origin[1] + i * tile_size,
                        tile_size, tile_size
                    )
                    pygame.draw.rect(screen, black, lines, 3)

                if board[i][j] != ft.EMPTY:
                    if board[i][j] == ft.X:
                        pygame.draw.circle(screen, black, rect.center, 30, 0)
                    elif board[i][j] == ft.O:
                        pygame.draw.circle(screen, white, rect.center, 30, 0)

                row.append(rect)
            tiles.append(row)

        game_over = game.left == 0
        player = ft.player2sign[game.player]

        # Show title
        if game_over:
            winner = game.winner
            if winner == 0:
                title = f"Game Over: Tie."
            else:
                if ft.player2sign[game.winner] == user:
                    title = f"Game Over: Human wins."
                else:
                    title = f"Game Over: AI wins."
        elif user == player:
            if user == ft.X:
                title = f"Play as black"
            elif user == ft.O:
                title = f"Play as white"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, black)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 40)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                if game.left < 15:
                    time.sleep(1)
                action = mcts.search(game.state)
                game.move(action)
                board = game.board
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(5):
                for j in range(5):
                    if (board[i][j] == ft.EMPTY and tiles[i][j].collidepoint(mouse)):
                        game.move((i,j))
                        board = game.board

        if game_over:
            # draw button
            againButton = pygame.Rect(width / 3, height - 70, width / 3, 60)
            again = mediumFont.render("Play Again", True, orange)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, black, againButton)
            screen.blit(again, againRect)

            # draw scores
            scores = largeFont.render("scores:", True, black)
            scoresRect = scores.get_rect()
            scoresRect.center = (100, 220)
            scoresRect.x = 25
            screen.blit(scores, scoresRect)

            aiscores = largeFont.render(f"AI: {game.scores[1-int((1-sign2player[user])/2)]}", True, black)
            aiscoresRect = aiscores.get_rect()
            aiscoresRect.center = (100, 300)
            aiscoresRect.x = 25
            screen.blit(aiscores, aiscoresRect)

            huscores = largeFont.render(f'Human: {game.scores[int((1-sign2player[user])/2)]}', True, black)
            huscoresRect = huscores.get_rect()
            huscoresRect.center = (100, 380)
            huscoresRect.x = 25
            screen.blit(huscores, huscoresRect)

            # detect click
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    game = ft.Fiver_tigers() 
                    board = game.board
                    ai_turn = False

    pygame.display.flip()
