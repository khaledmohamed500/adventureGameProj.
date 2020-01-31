

import time
import random
from game_state import GameState as gs
from monster import Monster as mn

pause = 1


def print_sleep(text_to_print, seconds):
    """Print text to the console and wait a specified number of seconds.
    print_sleep will print to the console text that has been passed in.
    It will then wait the number of seconds passed in by the user.
    Args:
    text_to_print - (string) text that will be printed to the console.
    seconds - (int) the number of seconds to wait before exiting the funciton.
    Returns:
    none
    """
    print(text_to_print)
    time.sleep(seconds)


def present_choice(choices):
    """Present the user a list of choices.
    present_choice prints a list of choices to the screen and waits for user
    input. The prompt is repeated until the user inputs one of the choices in
    the list. Once a valid choice has been made, the choice is returned.
    Args:
    choices - (list of strings) a list of items that will be printed to the
              screen. Each item in the list must be a string.
    Returns
    A string containing the user's choice.
    """
    while True:
        prompt = '(Please enter ' + choices[0]
        for choice in choices[1:]:
            prompt += ' or ' + choice
        prompt += ')'

        print(prompt)
        answer = input()
        if answer in choices:
            break

    return answer


def battle_system(game, monster):
    """Handle battles between the player and monsters."""
    print_sleep('*** BATTLE!!!! ***', pause)
    while True:
        print_sleep('Your Health: {}'.format(game.health), pause)
        print_sleep(monster.display_stats(), pause)
        print('*' * 25)
        print('Press 1 to attack the {}.'.format(monster.monster_type))
        print('Press 2 to cowardly run away.')
        print('*' * 25)
        answer = present_choice(['1', '2'])
        if answer == '1':
            hit_chance = random.randint(1, 100)
            if hit_chance < (100 - monster.dexterity + 2 * game.experience):
                damage = random.randint(30, 70) + 2*game.experience
                print_sleep('You landed a hit with {} damage!'
                            .format(damage), pause)
                print_sleep('Your experience has increased.', pause)
                game.increase_experience()
                monster.take_damage(damage)
                if not monster.still_alive():
                    print_sleep('You\'ve slain the {}!\n'
                                .format(monster.monster_type), pause * 3)
                    game.location = 'throne_room'
                    break
            else:
                print_sleep('You missed!', pause)

        elif answer == '2':
            dash_chance = random.randint(1, 100)
            if dash_chance < (100 - monster.dexterity + 2 * game.experience):
                print_sleep('Phew, that was close! You successfully escaped\n',
                            pause * 3)
                print_sleep('Your experience has increased.', pause)
                game.increase_experience()
                game.location = 'field'
                break
            else:
                print_sleep('Oh no! The {} blocked your escape!'
                            .format(monster.monster_type), pause)

        print_sleep('The {} attacks you!'.format(monster.monster_type), pause)
        defend_chance = random.randint(1, 100)
        if defend_chance < (100 - monster.dexterity + 2 * game.experience):
            print_sleep('The {} missed!'.format(monster.monster_type), pause)
            print_sleep('Your experience has increased.', pause)
            game.increase_experience()
        else:
            print_sleep('You\'ve been hit!', pause)
            print_sleep('The {} did {} damage'
                        .format(monster.monster_type, monster.strength), pause)
            game.take_damage(monster.strength)
            if not game.still_alive():
                print_sleep('You\'ve died!\n', pause * 3)
                break


def open_field(game):
    """The starting location of the game."""

    print_sleep('You are in an open field.', pause)
    print_sleep('There is a large, ominous castle up ahead. There is a quaint '
                'town to your right', pause)
    print('*' * 25)
    print('Press 1 to go to the castle.')
    print('Press 2 to go to the town.')
    print('*' * 25)
    answer = present_choice(['1', '2'])
    if answer == '1':
        location = 'castle'
    elif answer == '2':
        location = 'town'

    game.location = location
    game.game_over = False


def castle(game):
    """Handle the castle area of the game.
    The castle is where the user will face Timmy the terrible and his
    henchmen."""
    print_sleep('You are at the gate of a large castle.', pause)
    if 'Stake' not in game.inventory:
        print_sleep('You notice a wooden stake laying in the grass to your '
                    'side. That may come it handy for killing vampires!',
                    pause)
        print('*' * 25)
        print('Press 1 to go pick up the stake.')
        print('Press 2 to leave the stake. Who knows where its been!')
        print('*' * 25)
        answer = present_choice(['1', '2'])
        if answer == '1':
            game.inventory.append('Stake')

    print_sleep('You enter through the gate into the main hall.', pause)
    random_monster = random.randint(1, 3)
    switcher = {
        1: {'monster_type': 'Werewolf',
            'description': ('Strong and fast, the Werewolf is one of the '
                            'deadliest monsters in the realm. Only the most '
                            'experienced warriors dare fight one.'),
            'health': 100,
            'strength': 35,
            'dexterity': 30},
        2: {'monster_type': 'Ogre',
            'description': ('Strong and resilient, the Ogre can crush a man '
                            'in a single blow and can withstand a beating. '
                            'However if you dodge this lumbering beast\'s '
                            'clumsy strikes, you may have a chance.'),
            'health': 200,
            'strength': 100,
            'dexterity': 15},
        3: {'monster_type': 'Bunny',
            'description': ('These cute little balls of pure evil don\'t '
                            'look like much of a threat. One solid whack '
                            'will take them out. That is if you can keep up '
                            'with the speedy little critters.'),
            'health': 5,
            'strength': 1,
            'dexterity': 70}
    }
    monster = mn(switcher[random_monster])

    print_sleep('Your blood curdles as you sense the presence of evil '
                'lurking in the shadows.', pause)
    print_sleep('Rushing out to greet you is one of Timmy\'s henchmen. '
                'It\'s a {}!'.format(monster.monster_type), pause)
    print_sleep(monster.description, pause)

    battle_system(game, monster)

    del monster


def throne_room(game):
    """Handle the throne room area game play."""
    print_sleep('\nYou enter a dark throne room. A large blood red throne '
                'sits in the middle of the room.', pause)
    print_sleep('A glint of shimmering light catches your eye to your right. '
                'You approach a large ornate mirror. You feel drawn to it.\n'
                'Enraptured, you gaze at your visage in the reflection.',
                pause)
    print_sleep('You are familiar enough with magical objects to realize '
                'the mirror is enchanted with dark magic. However you can\'t '
                'seem to break free of it\'s spell as you continue to gaze '
                'at your own reflection.', pause)
    print_sleep('It\'s then that you feel the clawed hand grasp your '
                'shoulder. Your heart nearly stops pounding as you are '
                'gripped by fear from the sense of ice cold breath on the '
                'back of your neck.', pause)
    print_sleep('The reflection in the mirror does not betray the presence '
                'of any other being though.\nIt\'s not until you feel the '
                'pressure of the needle like teeth on your neck that you '
                'are able to finally wrest yourself free of the mirror\'s '
                'enchancements.', pause * 2)

    if 'garlic' in game.inventory:
        print_sleep('\nYou feel the life drain out of your body as Timmy\'s '
                    'sinks into your neck. Timmy grabs the garlic tied '
                    'around your neck as your near lifeless body crumples to '
                    'the floor', pause)
        print_sleep('"Did you honestly think something as paltry as a clove '
                    'of garlic would keep you safe from ME? BWA HA HA. '
                    'Foolish human."', pause * 2)
        print_sleep('Timmy\'s diabolical, mocking laughter is the last '
                    'thing you hear as you slip into unconciousness.', pause)
        print_sleep('\nThank you for playing. Unfortunately you make a '
                    'better Vampire meal than a hero!', pause)
    elif 'turnip' in game.inventory:
        print_sleep('\nYou tense yourself waiting for the vampire to sink '
                    'his fangs into your neck. You\'ve already resigned '
                    'yourself to this fate.', pause * 2)
        print_sleep('But to your surprise, you feel Timmy free you from his '
                    'his grip. You stumble back, warily regarding your '
                    'wouldbe executioner.', pause)
        print_sleep('"Is that a turnip around your neck?" asks Timmy.', pause)
        print_sleep('You clutch the vegetable tied around your neck. '
                    'You bring yourself to nod meekly.', pause * 2)
        print_sleep('Timmy reaches out for it longingly. "May I have it?" '
                    'he asks.', pause)
        print('*' * 25)
        print('Press 1 hand Timmy the turnip.')
        print('Press 2 to defy the dark lord.')
        print('*' * 25)
        answer = present_choice(['1', '2'])
        if answer == '1':
            print_sleep('Timmy takes the turnip in his hands and gently '
                        'caresses it as he breathes in its scent.', pause)
            print_sleep('"My mother used to feed me turnip\'s as a child." '
                        'Timmy says with a forlorn look on his face.', pause)
            if 'Stake' in game.inventory:
                print('*' * 25)
                print('Press 1 to stab Timmy with the stake while he\'s '
                      'distracted.')
                print('Press 2 to do nothing.')
                print('*' * 25)
                answer = present_choice(['1', '2'])
            else:
                answer = '2'
            if answer == '1':
                print_sleep('As Timmy seems focused on the turnip, you '
                            'quickly jump to your feet and rush at him '
                            'with the stake', pause)
                print_sleep('Timmy effortlessly disarms you and grabs you by '
                            'the throat.', pause)
                print_sleep('"Trecherous human!" bellows the vampire.', pause)
                print_sleep('The world quickly fades to black as Timmy '
                            'crushes your neck it his vice like grip.', pause)
                print_sleep('\nThank you for playing. Unfortunately you make '
                            'a better Vampire meal than a hero!', pause)
            elif answer == '2':
                print_sleep('"Perhaps I\'ve misunderstood you humans." '
                            'says Timmy.', pause)
                print_sleep('"Tell the town\'s people that as long as they '
                            'regularly bring me turnips, they will enjoy '
                            'my protection."', pause)
                print_sleep('\n*** YOU WIN ***\n', pause * 2)
                print_sleep('Note only did you rescue the town from the '
                            'wrath of the vampire, under his protection '
                            'the town went on to enjoy centuries of peace '
                            'and become a major centre of economic activity.',
                            pause)

        elif answer == '2':
            print_sleep('You see the rage build in Timmy\'s face.', pause)
            print_sleep('"How dare you defy me!!!"', pause)
            print_sleep('The last thing you see is Timmy\'s beastly form '
                        'charging at you at unbelievable speed before '
                        'everything goes black.', pause * 2)
            print_sleep('\nThank you for playing. Unfortunately you make a '
                        'better Vampire meal than a hero!', pause)
    else:
        print_sleep('\nYou feel the life drain out of your body as Timmy\'s '
                    'sinks into your neck. You feel the blood flowing out '
                    'of your neck as your near lifeless body crumples to '
                    'the floor', pause)
        print_sleep('"Did you honestly think a mere mortal like yourself '
                    'could challenge the all mighty Timmy? BWA HA HA. '
                    'Foolish human."', pause * 2)
        print_sleep('Timmy\'s diabolical, mocking laughter is the last '
                    'thing you hear as you slip into unconciousness.', pause)
        print_sleep('\nThank you for playing. Unfortunately you make a '
                    'better Vampire meal than a hero!', pause)

    game.game_over = True


def town(game):
    """Handle the town area game play.
    In the town, the user can rest at the inn to recuperate their health,
    or aquire items at the market.
    """
    location = 'town'
    print_sleep('You enter a quiet, subdued town', pause)

    if not game.been_to_town:
        print_sleep('You are greeted by an official looking individual.',
                    pause)
        print_sleep('"Thank the gods you came. I am the mayor of this town. '
                    'If you can rid of Timmy the Terrible, we will pay you '
                    '100 gold."', pause)
        print_sleep('"Feel free to rest in the inn if you need to '
                    'recuperate."', pause)
        print_sleep('"You may help yourself to anything useful to your quest '
                    'in the market."', pause)
        game.been_to_town = True

    print('*' * 25)
    print('Press 1 to go to the inn.')
    print('Press 2 to go to the market.')
    print('Press 3 to leave the town.')
    print('*' * 25)
    answer = present_choice(['1', '2', '3'])
    if answer == '1':
        print_sleep('What a great sleep! Your health is back to 100.', pause)
        game.health = 100
    elif answer == '2':
        market(game)
    elif answer == '3':
        location = 'field'

    game.location = location


def market(game):
    """Handle the market area game play.
    The market is where the user can acquire items that may help them on
    their quest.
    """
    if {'turnip', 'garlic'}.intersection(game.inventory):
        print_sleep('"We are all sold out now. Sorry! '
                    'Please save our town!"', pause)
    else:
        print_sleep('"Brave warrior, '
                    'help yourself to whatever you fancy."', pause)
        print_sleep('"We have the juiciest turnips, and the '
                    'strongest garlic.', pause)
        print('*' * 25)
        print('Press 1 to go to take a turnip.')
        print('Press 2 to go to take some garlic.')
        print('Press 3 to leave the market.')
        print('*' * 25)
        answer = present_choice(['1', '2', '3'])
        if answer == '1':
            print_sleep('You have added a turnip to your inventory!', pause)
            game.inventory.append('turnip')
        if answer == '2':
            print_sleep('You have added garlic to your inventory!', pause)
            game.inventory.append('garlic')
        if answer != '3':
            print_sleep('Your experience has increased.', pause)
            game.increase_experience()


def opening_scene():
    """Present the text for the opening scene."""
    print('\n\n\n')
    print(' ' * 20 + '*' * 60)
    print(' ' * 20 + '**{:^56}**'.format('Adventure Game: Timmy the Terrible'))
    print(' ' * 20 + '**{:^56}**'.format('Developed by: khaled mohamed'))
    print(' ' * 20 + '**{:^56}**'.format('For: Udacity IPND'))
    print(' ' * 20 + '*' * 60)
    print_sleep('\n\n\n', 2)

    print_sleep('Welcome young warrior! The local town needs your help. '
                'They are being terrorized by Timmy the Terrible!', pause)
    print_sleep('Although you are an experience monster hunter, this will be '
                'your biggest challenge yet. Timmy the Terrible is an '
                'ancient, powerful vampire.', pause)


def main():
    game = gs()

    opening_scene()
    game.display_stats()
    while not game.game_over:
        switcher = {
            'field': open_field,
            'castle': castle,
            'town': town,
            'throne_room': throne_room
        }
        switcher[game.location](game)

    del game


if __name__ == '__main__':
    while True:
        main()

        print('\n')
        print('*' * 25)
        print('Would you like to play again? (Y/n)')
        print('*' * 25)
        answer = present_choice(['Y', 'n'])
        if answer == 'n':
            break