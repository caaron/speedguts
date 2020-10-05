import os
import pygame
# Import other modules from pygame_cards if needed.
from pygame_cards import game_app, controller, enums, card_holder, deck, card, gui
from random import shuffle

class position:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class slot:
    def __init__(self,x,y,card):
        self.pos = position()
        self.card = card


class State:
    """ Enums for state machine """
    INIT = 0
    START = 3
    PLAY = 4
    TIMER_ON = 5
    END = 6

def draw_empty_card_pocket(holder, screen):
    """ Renders empty card pocket at the position of CardHolder object
    :param holder: CardsHolder object
    :param screen: Screen object to render onto
    """
    if len(holder.cards) == 0:
        rect = (holder.pos[0], holder.pos[1],
                card_holder.CardsHolder.card_json["size"][0],
                card_holder.CardsHolder.card_json["size"][1])
        pygame.draw.rect(screen, (77, 77, 77), rect, 2)


class Discards(card_holder.CardsHolder):

    def render(self, screen):
        draw_empty_card_pocket(self, screen)


class Upcards(card_holder.CardsHolder):

    def move_all_cards(self, other, back_side_up=True):
        """ Moves all cards to other cards holder.
        :param other: instance of CardsHolder where cards will be moved.
        :param back_side_up: True if cards should be flipped to back side up, False otherwise.
        """
        if isinstance(other, CardsHolder):
            while len(self.cards) != 0:
                card_ = self.pop_top_card()
                if card_ is not None:
                    if card_.back_up != back_side_up:
                        card_.flip()
                    other.add_card(card_)


class MyGameController(controller.Controller):
    """ Main class that controls game logic and handles user events.

        Following methods are mandatory for all classes that derive from Controller:
            - build_objects()
            - start_game()
            - process_mouse_events()

        Also these methods are not mandatory, but it can be helpful to define them:
            - execute_game()
            - restart_game()
            - cleanup()

        These methods are called from higher level GameApp class.
        See details about each method below.
        Other auxiliary methods can be added if needed and called from the mandatory methods.
    """

    def build_objects(self):
        """ Create permanent game objects (deck of cards, players etc.) and
        GUI elements in this method. This method is executed during creation of GameApp object.
        """

        deck_pos = self.settings_json["deck"]["position"]
        deck_offset = self.settings_json["deck"]["offset"]
        self.nCards = self.settings_json["gui"]["num_cards"]
        self.deck = deck.Deck(type_=enums.DeckType.full, pos=deck_pos, offset=deck_offset)
        card_size = self.settings_json["card"]["size"]
        upcards_pos = self.settings_json["upcards"]["position"]
        upcards_offset = self.settings_json["upcards"]["offset"]
        self.upcards = card_holder.CardsHolder(pos=upcards_pos, offset=upcards_offset)

        discards_pos = self.settings_json["discards"]["position"]
        discards_offset = self.settings_json["discards"]["offset"]
        self.discards = Discards(pos=discards_pos, offset=discards_offset)

        self.tmpdeck = card_holder.CardsHolder(pos=(0,0))

        self.current_card_index = 0
        self.bank_index = 0
        self.add_rendered_object((self.deck, None))
        self.add_rendered_object((self.upcards, self.discards))

        # All game objects should be added to self objects list
        #  with add_object method in order to be rendered.

        # Create Restart button
        self.gui_interface.show_button(self.settings_json["gui"]["restart_button"],
                                       self.restart_game, "Restart")
        self.gui_interface.show_button(self.settings_json["gui"]["higher_button"],
                                       self.higher_clicked, "Higher")
        self.gui_interface.show_button(self.settings_json["gui"]["bank_button"],
                                       self.bank_clicked, "Bank")
        self.gui_interface.show_button(self.settings_json["gui"]["lower_button"],
                                       self.lower_clicked, "Lower")

        #self.gui_interface.show_label(self.settings_json["gui"]["count_label"], "Count:0")
        self.show_count()
        self.state = State.INIT


    def start_game(self):
        """ Put game initialization code here.
            For example: dealing of cards, initialization of game timer etc.
            This method is triggered by GameApp.execute().
        """

        # Shuffle cards in the deck
        self.current_card_index = 1
        self.bank_index = 0
        self.deck.shuffle()
        card_ = self.deck.pop_top_card()
        card_.flip()
        self.upcards.add_card(card_)

    def show_count(self):
        tmp = "Count:%i" % (self.current_card_index)
        self.gui_interface.show_label(self.settings_json["gui"]["count_label"], tmp, timeout=0)

    def process_mouse_event(self, pos, down, double_click):
        """ Put code that handles mouse events here.
            For example: grab card from a deck on mouse down event,
            drop card to a pile on mouse up event etc.
            This method is called every time mouse event is detected.
            :param pos: tuple with mouse coordinates (x, y)
            :param down: boolean, True for mouse down event, False for mouse up event
            :param double_click: boolean, True if it's a double click event
        """
#        if down and self.deck.is_clicked(pos):
        if down and self.deck.is_clicked(pos):
            card_ = self.deck.pop_top_card()
            if isinstance(card_, card.Card):
                card_.flip()
                #self.custom_dict["stack"].add_card(card_)

    def restart_game(self):
        """ Put code that cleans up any current game progress and starts the game from scratch.
            start_game() method can be called here to avoid code duplication. For example,
            This method can be used after game over or as a handler of "Restart" button.
        """
        self.upcards.move_all_cards(self.deck)
        self.discards.move_all_cards(self.deck)
        self.start_game()

    def execute_game(self):
        """ This method is called in an endless loop started by GameApp.execute().
        IMPORTANT: do not put any "heavy" computations in this method!
        It is executed frequently in an endless loop during the app runtime,
        so any "heavy" code will slow down the performance.
        If you don't need to check something at every moment of the game, do not define this method.

        Possible things to do in this method:
             - Check game state conditions (game over, win etc.)
             - Run bot (virtual player) actions
             - Check timers etc.
        """
        pass

    def cleanup(self):
        """ Called when user closes the app.
            Add destruction of all objects, storing of game progress to a file etc. to this method.
        """
        del self.deck
        del self.upcards
        del self.discards
        del self.tmpdeck

    def disable_buttons(self):
        pass

    def enable_buttons(self):
        pass

    def start_timer(self, ms=500):
        #start timer, not event driver, must poll
        pass

    def show_bad_card_then_reset(self):
        # start a timer to show the bad card, timeout, then move
        # all cards from upcards back to deck
        # need state machine that is updated in execute_game, calls en/disable buttons
        self.move_all_but_bottom_card(self.upcards,self.deck)
        pass
    
    def move_all_but_bottom_card(self,src,dst,doShuffle=True):
        while (len(src.cards) > 1):
            _card = src.pop_top_card()
            _card.flip()
            self.tmpdeck.add_card(_card)
        if doShuffle == True:
            shuffle(self.tmpdeck.cards)
        self.tmpdeck.move_all_cards(dst)

    def higher_clicked(self):
        pass
        if self.current_card_index < self.nCards:
            new_card = self.deck.pop_top_card()
            new_card.flip()
            up_card = self.upcards.pop_top_card()
            self.upcards.add_card(up_card)  # put that card back
            self.upcards.add_card(new_card)  # put on new card
            if new_card.rank > up_card.rank:
                self.current_card_index += 1
            else:
                self.show_bad_card_then_reset()
            self.show_count()

    def lower_clicked(self):
        pass
        if self.current_card_index < self.nCards:
            new_card = self.deck.pop_top_card()
            new_card.flip()
            up_card = self.upcards.pop_top_card()
            self.upcards.add_card(up_card)  # put that card back
            self.upcards.add_card(new_card)  # put on new card
            if new_card.rank < up_card.rank:
                self.current_card_index += 1
            else:
                self.show_bad_card_then_reset()
            self.show_count()

    def bank_clicked(self):
        self.bank_index = self.current_card_index
        # set a timer to disable buttons
        self.show_bad_card_then_reset()

def main():
    """ Entry point of the application. """

    # JSON files contains game settings like window size, position of game and gui elements etc.
    json_path = os.path.join(os.getcwd(), 'settings.json')

    # Create an instance of GameApp and pass a path to setting json file
    # and an instance of custom Controller object. This will initialize the game,
    # build_objects() from Controller will be called at this step.
    speedguts = game_app.GameApp(json_path=json_path, game_controller=MyGameController())

    # Start executing the game. This will call start_game() from Controller,
    # then will be calling execute_game() in an endless loop.
    speedguts.execute()

if __name__ == '__main__':
    main()
