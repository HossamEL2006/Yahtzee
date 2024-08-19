
from pygame.locals import *
import time
import random
import pygame
pygame.init()


class Dice():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.number = None
        self.isLocked = False
        self.color = 'white'
        self.number = 6
        self.change_position()
        self.update()

    def roll(self):
        self.number = random.randint(1, 6)
        self.change_position()
        self.update()

    def draw(self):
        DS.blit(self.image, self.rect)

    def update(self):
        self.update_image()
        self.update_rect()

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.collideRect = self.rect.copy()
        self.collideRect.w += dicePadding
        self.collideRect.h += dicePadding
        self.collideRect.center = self.rect.center

    def update_image(self):
        if self.isLocked == False:
            self.color = 'white'
        else:
            self.color = 'black'
        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
            f'src/assets/dices/{self.color}/{self.number}.png'), (diceSize, diceSize)), self.rotate)

    def change_position(self):
        self.x = random.randint(boardPadding, boardSize - boardPadding - diceSize)
        self.y = random.randint(boardPadding, boardSize - boardPadding - diceSize)
        self.rotate = random.randint(0, 360)


class Result():
    def __init__(self, dices):
        self.dices = dices
        _resultInList = []
        for i in self.dices:
            _resultInList.append(str(i.number))
        _resultInList.sort()
        self.resultInString = "".join(_resultInList)
        self.numberOfEachNumber = [self.resultInString.count(str(i)) for i in range(1, 7)]
        self.sum = 0
        for dice in dices:
            self.sum += dice.number

    def aces(self): return self.resultInString.count('1') * 1

    def twos(self): return self.resultInString.count('2') * 2

    def threes(self): return self.resultInString.count('3') * 3

    def fours(self): return self.resultInString.count('4') * 4

    def fives(self): return self.resultInString.count('5') * 5

    def sixes(self): return self.resultInString.count('6') * 6

    def three_of_a_kind(self): return self.sum if (
        3 in self.numberOfEachNumber or 4 in self.numberOfEachNumber or 5 in self.numberOfEachNumber) else 0

    def four_of_a_kind(self): return self.sum if (
        4 in self.numberOfEachNumber or 5 in self.numberOfEachNumber) else 0

    def full_house(
        self): return 25 if 3 in self.numberOfEachNumber and 2 in self.numberOfEachNumber else 0

    def small_straight(self): return 30 if ('1' in self.resultInString and '2' in self.resultInString and '3' in self.resultInString and '4' in self.resultInString) or (
        '2' in self.resultInString and '3' in self.resultInString and '4' in self.resultInString and '5' in self.resultInString) or ('3' in self.resultInString and '4' in self.resultInString and '5' in self.resultInString and '6' in self.resultInString) else 0

    def large_straight(
        self): return 40 if '12345' in self.resultInString or '23456' in self.resultInString else 0

    def yahtzee(self): return 50 if 5 in self.numberOfEachNumber else 0

    def chance(self): return self.sum


class ScoreSheet():
    def __init__(self):
        self.dictOfScore = {
            "Aces": "",
            "Twos": "",
            "Threes": "",
            "Fours": "",
            "Fives": "",
            "Sixes": "",
            "Total": "",
            "Bonus": "",
            "Upper Sum": "",
            "Three Of A Kind": "",
            "Four Of A Kind": "",
            "Full House": "",
            "Small Straight": "",
            "Large Straight": "",
            "YAHTZEE !": "",
            "Chance": "",
            "Lower Sum": "",
            "Final Sum": "",
        }
        self.update_sum_and_total()

    def mark(self, result: Result, toMark):
        global phase, dices
        if self.dictOfScore[toMark] == "":
            if self.dictOfScore['YAHTZEE !'] != "" and self.dictOfScore['YAHTZEE !'] >= 50 and result.yahtzee() == 50:
                self.dictOfScore['YAHTZEE !'] += 100
            dictOfFonctions = {
                "Aces": result.aces,
                "Twos": result.twos,
                "Threes": result.threes,
                "Fours": result.fours,
                "Fives": result.fives,
                "Sixes": result.sixes,
                "Three Of A Kind": result.three_of_a_kind,
                "Four Of A Kind": result.four_of_a_kind,
                "Full House": result.full_house,
                "Small Straight": result.small_straight,
                "Large Straight": result.large_straight,
                "YAHTZEE !": result.yahtzee,
                "Chance": result.chance
            }
            self.dictOfScore[toMark] = dictOfFonctions[toMark]()
            phase = 0
            dices.clear()
            self.update_sum_and_total()

    def update_sum_and_total(self):
        self.dictOfScore["Total"] = self._sum(upperSection)
        if self.dictOfScore["Total"] >= 63:
            self.dictOfScore["Bonus"] = 35
        else:
            self.dictOfScore['Bonus'] = 0
        self.dictOfScore["Upper Sum"] = self._sum(['Total', 'Bonus'])
        self.dictOfScore["Lower Sum"] = self._sum(lowerSection)
        self.dictOfScore["Final Sum"] = self._sum(['Upper Sum', 'Lower Sum'])

    def _sum(self, liste):
        _sum = 0
        for i in liste:
            if not self.dictOfScore[i] == '':
                _sum += self.dictOfScore[i]
        return _sum


class ScoreButton():
    def __init__(self, mark, x, y, isAButton=True):
        self.isAButton = isAButton
        self.mark = mark
        self.rect1 = pygame.Rect(
            2*margin + boardSize + x *
            (scoreButtonRect1Size[0] + 2 * margin + scoreButtonRect2Size[0]),
            margin + y * (scoreButtonRect1Size[1] + margin),
            scoreButtonRect1Size[0],
            scoreButtonRect1Size[1]
        )
        self.surface1 = morganChalk.render(self.mark, True, BLACK)
        self.surface1Rect = self.surface1.get_rect()
        self.surface1Rect.center = self.rect1.center
        self.rect2 = pygame.Rect(
            3*margin + boardSize +
            scoreButtonRect1Size[0] + x * (scoreButtonRect1Size[0] +
                                           2 * margin + scoreButtonRect2Size[0]),
            margin + y * (scoreButtonRect1Size[1] + margin),
            scoreButtonRect2Size[0],
            scoreButtonRect2Size[1]
        )
        self.update()

    def update(self):
        self.surface2 = morganChalk.render(str(scoreSheet.dictOfScore[self.mark]), True, BLACK)
        self.surface2Rect = self.surface2.get_rect()
        self.surface2Rect.center = self.rect2.center

    def draw(self):
        pygame.draw.rect(DS, WHITE, self.rect1)
        pygame.draw.rect(DS, BLACK, self.rect1, 1)
        DS.blit(self.surface1, self.surface1Rect)
        pygame.draw.rect(DS, WHITE, self.rect2)
        pygame.draw.rect(DS, BLACK, self.rect2, 1)
        DS.blit(self.surface2, self.surface2Rect)


def roll_dices():
    if "" in scoreSheet.dictOfScore.values():
        global phase, result
        _lockedDices = []
        for dice in dices:
            if dice.isLocked == True:
                _lockedDices.append(dice)
        if phase == 0:
            for i in range(5):
                dices.append(Dice())
        if not len(_lockedDices) == 5 and not phase == 3:
            phase += 1
            _restart = True
            for dice in dices:
                if dice.isLocked == False:
                    dice.roll()
            while _restart:
                _restart = False
                for dice in dices:
                    if dice.isLocked == False:
                        dice.change_position()
                        dice.update()
                for dice in dices:
                    _listForOtherDice = dices.copy()
                    _listForOtherDice.remove(dice)
                    for i in _listForOtherDice:
                        if dice.collideRect.colliderect(i.collideRect):
                            _restart = True
            result = Result(dices)


diceSize = 40
dicePadding = 20
margin = 5
boardSize = 320
boardPadding = 10
generateButtonSize = (boardSize, 75)
scoreButtonRect1Size = (150, 40)
scoreButtonRect2Size = (40, 40)
textSize = 20

upperSection = ['Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes']
lowerSection = ['Three Of A Kind', 'Four Of A Kind', 'Full House',
                'Small Straight', 'Large Straight', 'YAHTZEE !', 'Chance']

W, H = margin * 6 + boardSize + 2 * \
    (scoreButtonRect1Size[0] + scoreButtonRect2Size[0]), 3 * \
    margin + boardSize + generateButtonSize[1]
HW, HH = W/2, H/2
AREA = W * H

CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("YAHTZEE")
pygame.display.set_icon(pygame.image.load('src/assets/icon.png'))

FPS = 30

RUNNING = True

result = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_GREEN = (25, 116, 39)
GRAY_4 = (68, 68, 68)

phase = 0

board = pygame.Rect(margin, margin, boardSize, boardSize)

morganChalk = pygame.font.Font('src/assets/fonts/Morgan Chalk.ttf', textSize)
jackpot = pygame.font.Font('src/assets/fonts/Jackpot.ttf', textSize)

generateButtonRect = pygame.Rect(margin, boardSize + 2 * margin,
                                 generateButtonSize[0], generateButtonSize[1])
generateButtonSurface = morganChalk.render(f"roll {phase} / 3", True, BLACK)

scoreSheet = ScoreSheet()

dices = []
scoreButtons = []

scoreButtons.append(ScoreButton('Aces', 0, 0))
scoreButtons.append(ScoreButton('Twos', 0, 1))
scoreButtons.append(ScoreButton('Threes', 0, 2))
scoreButtons.append(ScoreButton('Fours', 0, 3))
scoreButtons.append(ScoreButton('Fives', 0, 4))
scoreButtons.append(ScoreButton('Sixes', 0, 5))
scoreButtons.append(ScoreButton('Total', 0, 6, False))
scoreButtons.append(ScoreButton('Bonus', 0, 7, False))
scoreButtons.append(ScoreButton('Upper Sum', 0, 8, False))
scoreButtons.append(ScoreButton('Three Of A Kind', 1, 0))
scoreButtons.append(ScoreButton('Four Of A Kind', 1, 1))
scoreButtons.append(ScoreButton('Full House', 1, 2))
scoreButtons.append(ScoreButton('Small Straight', 1, 3))
scoreButtons.append(ScoreButton('Large Straight', 1, 4))
scoreButtons.append(ScoreButton('YAHTZEE !', 1, 5))
scoreButtons.append(ScoreButton('Chance', 1, 6))
scoreButtons.append(ScoreButton('Lower Sum', 1, 7, False))
scoreButtons.append(ScoreButton('Final Sum', 1, 8, False))

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == MOUSEBUTTONDOWN:
            if generateButtonRect.collidepoint(event.pos):
                roll_dices()
            for dice in dices:
                if dice.rect.collidepoint(event.pos):
                    if dice.isLocked == False:
                        dice.isLocked = True
                    else:
                        dice.isLocked = False
            for scoreButton in scoreButtons:
                if scoreButton.isAButton == True and scoreButton.rect2.collidepoint(event.pos) and not phase == 0:
                    scoreSheet.mark(result, scoreButton.mark)
    for dice in dices:
        dice.update()
    for scoreButton in scoreButtons:
        scoreButton.update()
    DS.fill(BLACK)
    DS.fill(GRAY_4)
    pygame.draw.rect(DS, BOARD_GREEN, board)
    pygame.draw.rect(DS, BLACK, board, 1)
    pygame.draw.rect(DS, WHITE, generateButtonRect)
    pygame.draw.rect(DS, BLACK, generateButtonRect, 1)
    generateButtonSurface = jackpot.render(f"roll {phase} / 3", True, BLACK)
    generateButtonSurfaceRect = generateButtonSurface.get_rect()
    generateButtonSurfaceRect.center = generateButtonRect.center
    DS.blit(generateButtonSurface, generateButtonSurfaceRect)
    for dice in dices:
        dice.draw()
    for scoreButton in scoreButtons:
        scoreButton.draw()
    pygame.display.flip()
    CLOCK.tick(FPS)
