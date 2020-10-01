import os

# Import other modules from pygame_cards if needed.
from pygame_cards import game_app, controller, enums, card_holder, deck, card

class position:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class slot:
    def __init__(self,x,y,card):
        self.pos = position()
        self.card = card


def draw_empty_card_pocket(holder, screen):
    """ Renders empty card pocket at the position of CardHolder object
    :param holder: CardsHolder object
    :param screen: Screen object to render onto
    """
    if len(holder.cards) == 0:
        rect = (holder.pos.x, holder.pos.y,
                card_holder.CardsHolder.card_json["size"][0],
                card_holder.CardsHolder.card_json["size"][1])
        pygame.draw.rect(screen, (77, 77, 77), rect, 2)


#class Foundation(card_holder.CardsHolder):


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
        cards_pos = self.settings_json["cards"]["position"]
        self.nCards = self.settings_json["gui"]["num_cards"]
        self.custom_dict["deck"] = deck.Deck(type_=enums.DeckType.short,
                                             pos=deck_pos, offset=deck_offset)
        #tmp = Card(hearts,two,(deck_pos[0],deck_pos[1]))
        #self.tmp_card = tmp
        pos = (cards_pos[0],cards_pos[1])
        card_size = self.settings_json["card"]["size"]
        self.slots = [0] * self.nCards
        self.current_card_index = 0
        pos = (cards_pos[0] + (0 * (card_size[0] + 20)), cards_pos[1])
        self.slots[0] = card_holder.CardsHolder(pos, (0, 0))
        self.add_rendered_object((self.custom_dict["deck"], self.slots[0]))
        for i in range(1, self.nCards):
            offset = (i * (card_size[0]+20), 0)
            pos = (cards_pos[0] + (i * (card_size[0]+20)),cards_pos[1])
            self.slots[i] = card_holder.CardsHolder(pos, (0,0))
#            self.add_rendered_object((self.custom_dict["deck"], self.slots[i]))
            #self.add_rendered_object((self.custom_dict["deck"], self.slots[i]))
            #self.add_rendered_object((self.tmp_card, self.slots[i]))
            #self.slots[i] = slot(deck_pos[0] + (i*card_size[0]),deck_pos[1],None)

        for i in range(1,self.nCards,2):
            self.add_rendered_object((self.slots[i], self.slots[i+1]))

        # All game objects should be added to self objects list
        #  with add_object method in order to be rendered.
        #self.add_rendered_object((self.custom_dict["deck"], self.custom_dict["stack"]))
        #self.add_rendered_object((self.custom_dict["deck"],self.slots))

        # Create Restart button
        self.gui_interface.show_button(self.settings_json["gui"]["restart_button"],
                                       self.restart_game, "Restart")
        self.gui_interface.show_button(self.settings_json["gui"]["higher_button"],
                                       self.higher_clicked, "Higher")
        self.gui_interface.show_button(self.settings_json["gui"]["lower_button"],
                                       self.lower_clicked, "Lower")


    def start_game(self):
        """ Put game initialization code here.
            For example: dealing of cards, initialization of game timer etc.
            This method is triggered by GameApp.execute().
        """

        # Shuffle cards in the deck
        self.current_card_index = 1
        self.custom_dict["deck"].shuffle()
        for i in range(0, self.nCards):
            pass
            card_ = self.custom_dict["deck"].pop_top_card()
            self.slots[i].add_card(card_)

        _card = self.slots[0].pop_top_card()
        _card.flip()
        self.slots[0].add_card(_card)


    def process_mouse_event(self, pos, down, double_click):
        """ Put code that handles mouse events here.
            For example: grab card from a deck on mouse down event,
            drop card to a pile on mouse up event etc.
            This method is called every time mouse event is detected.
            :param pos: tuple with mouse coordinates (x, y)
            :param down: boolean, True for mouse down event, False for mouse up event
            :param double_click: boolean, True if it's a double click event
        """
#        if down and self.custom_dict["deck"].is_clicked(pos):
        if down and self.custom_dict["deck"].is_clicked(pos):
            card_ = self.custom_dict["deck"].pop_top_card()
            if isinstance(card_, card.Card):
                card_.flip()
                #self.custom_dict["stack"].add_card(card_)

    def restart_game(self):
        """ Put code that cleans up any current game progress and starts the game from scratch.
            start_game() method can be called here to avoid code duplication. For example,
            This method can be used after game over or as a handler of "Restart" button.
        """
        #self.custom_dict["stack"].move_all_cards(self.custom_dict["deck"])
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
        del self.custom_dict["deck"]
        #del self.custom_dict["stack"]

    def higher_clicked(self):
        pass
        if self.current_card_index < self.nCards:
            _card = self.slots[self.current_card_index].pop_top_card()
            _card.flip()
            self.slots[self.current_card_index].add_card(_card)
            self.current_card_index += 1

    def lower_clicked(self):
        pass
        if self.current_card_index < self.nCards:
            _card = self.slots[self.current_card_index].pop_top_card()
            _card.flip()
            self.slots[self.current_card_index].add_card(_card)
            self.current_card_index += 1


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
