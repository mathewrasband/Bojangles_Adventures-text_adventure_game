GOTO = "go to "
def render_introduction():
    '''
    Create the message to be displayed at the start of your game.

    Returns:
        str: The introductory text of your game to be displayed.
    '''
    " . . . "
    return (" == Bojangles Search for the Ruby Monkey ==\n" +
                "             = By Mathew Rasband =                     \n")

def create_world():
    '''
    Creates a new version of the world in its initial state.

    Returns:
        World: The initial state of the world
    '''
    return {
        'map': create_map(),
        'player': create_player(),
        'status': "playing"
    }
def create_map():
    '''
    Creates a map of the world.
    
    Returns the location in the map.
    '''
    return {
        "meadow" : {
                "neighbors" : ["forest", "mountains", "cliffs"],
                "about" : "You look around there is a forest to the west, mountains \n to the north, and a river to the west.",
                "stuff" : []},
        "forest" : {
                "neighbors" : ["clearing", "desert", "meadow", "dense forest"],
                "about" : "Large beautiful trees tower above you. You can see a clearing to the \n west, a desert to the north, and a dense forest to the south.",
                "stuff" : []},
        "dense forest" : {
                "neighbors" : ['forest'],
                "about" : "The trees here are too thick to carry on return north where the forest \n is passable.",
                "stuff": []},
        "clearing" : {
                "neighbors" : ['forest'],
                "about" : "A shaft of light shines through the clearing to a sword sticking out of the ground.",
                "stuff" : ["sword"]},
        "desert" : {
                "neighbors" : ["forest", "mountains"],
                "about" : " The sun beats down on you in what appears to be endless sand to the north \n and west. There is a range of mountains to the east and the forest to the south.",
                "stuff" : []},
        "mountains": {
                "neighbors" : ["desert", "river", "meadow"],
                "about": "Massive snowcapped peaks tower above. Up a pass there appears to be an \n orge if you proceed forward. The desert is to your east, the river is to the west, \n and the meadow is to the south.",
                "stuff" : ["key", "ogre"]},
        "river" : {
                "neighbors" : ["mountains", "waterfall", "cliffs"],
                "about" : "It is raging with white capped rapids. There appears to be a waterfall to the \n north, cliffs to the south and the mountains to the east.",
                "stuff" : []},
        "waterfall" : {
                "neighbors" : ["cave", "river"],
                "about" : "There appears to be a cave behind the waterfall. Back to the south the river continues.",
                "stuff" : []},
        "cave" : {
                "neighbors" : ["waterfall"],
                "about" : "There appears to be a chest. If you have a key you can probably open up \n the chest. To get out go back towards the waterfall.",
                "stuff" : ["chest", "rope"]},
        "cliffs" : {
                "neighbors" : ["meadow", "river"],
                "about" : "Looking over the edge you  at the cliffs bottom can see the Ruby Monkey \n sparkling in the light. You can try to rappel down the cliffs to get the Ruby Monkey. \n The river is to the north and the meadows are to the east.",
                "stuff" : []},
        }
            
def create_player():
    '''
    Creates the player and inventory
    
    Returns the status of the player and their inventory.
    '''
    return {
        'location': 'meadow',
        'inventory': [],
    }

def render_location(world):
    '''
    Allows the player to know where they are in the world.
    
    Returns a statement about where you are in the world
    '''
    location = world['player']['location']
    here = world['map'][location]
    about = here['about']
    return ("You are at the " + location + ".\n" + about)

def render_player(world):
    '''
    Allows the player to see what they have.
    
    Returns: state about what you currently have in your inventory
    '''
    player = world['player']
    inventory = player['inventory']
    if len(inventory) <1:
        return "You have nothing on your person."
    else:
        holding = " You are holding a " + ', '.join(inventory)
    return holding

def render(world):
    '''
    Consumes a world and produces a string that will describe the current state
    of the world. Does not print.

    Args:
        world (World): The current world to describe.

    Returns:
        str: A textual description of the world.
    '''
    return (render_location(world) +
            render_player(world))

def get_options(world):
    '''
    Consumes a world and produces a list of strings representing the options
    that are available to be chosen given this state.

    Args:
        world (World): The current world to get options for.

    Returns:
        list[str]: The list of commands that the user can choose from.
    '''
    location = world['player']['location']
    here = world['map'][location]
    
    commands = ["quit"]
    
    if location == 'clearing':
        if len(here['stuff']) > 0:
            commands.append("grab "+here['stuff'][0])
            return commands
    
    if location == "mountains":
        if 'ogre' in here["stuff"]:
            commands.append("fight ogre")
        else:
            if len(here['stuff']) > 0:
                commands.append('grab ' + here['stuff'][0])
            
    if location == "cave":
        if "chest" in here["stuff"]:
            commands.append("open chest")
        else:
            if len(here["stuff"]) > 0:
                commands.append("grab " + here['stuff'][0])

    if location == "cliffs":
        if 'rope' in world['player']['inventory']:
            commands.append('rappel down cliff')
            
    if location == "cliffs":
        commands.append('climb down cliff')
    
    for neighbor in here["neighbors"]:
        commands.append("go to " + neighbor)
    return commands

def update(world, command):
    '''
    Consumes a world and a command and updates the world according to the
    command, also producing a message about the update that occurred. This
    function should modify the world given, not produce a new one.

    Args:
        world (World): The current world to modify.

    Returns:
        str: A message describing the change that occurred in the world.
    '''
    location = world['player']['location']
    here = world['map'][location]
    
    if command == "quit":
        world['status'] = 'quit'
        return "\nYou quit the game"
    
    if command == 'grab sword':
        here['stuff'].remove('sword')
        world['player']['inventory'].append('sword')
        return "\nYou now have a sword this could come in handy! "
    
    if command == 'fight ogre':
        if 'sword' in world["player"]["inventory"]:
            here["stuff"].remove("ogre")
            return "\nYou have killed the ogre! It looks like it dropped a key. "
        else:
            world['status'] = 'lost'
            return ("\nYou tried to fight the ogre with no weapons. \n" +
                        "It bonked you on the noggin with its club! \n" +
                        "You succumb to your injury and perish..... \n")
        
    if command == 'grab key':
        here['stuff'].remove('key')
        world['player']['inventory'].append('key')
        return "\nThis key could prove beneficial. "
            
    if command == "open chest":
        if "key" in world["player"]["inventory"]:
            here["stuff"].remove('chest')
            return "There is a large bundle of rope here."
        else:
            return "\nIt appears to be locked maybe if I had a key. "
        
    if command == "grab rope":
        here['stuff'].remove('rope')
        world['player']['inventory'].append('rope')
        return "\nThis rope looks nice and strong. "
    
    if command == "rappel down cliff":
        world['player']['inventory'].append('Ruby Monkey')
        world['status'] = 'won'
        return ("\nYou successfully rappelled down the cliff with the rope. \n" +
                    "Sitting on a pedestal you find the Ruby Monkey. \n" +
                    "You reach out a take it congratulations you have the Ruby Monkey. \n")
    
    if command == "climb down cliff":
        world['status'] = 'lost'
        return ("\nYou start climbing down the cliff. \n" +
                    "You hand hold breaks off. You start falling \n" +
                    "into empty space. You do not survive the fall. \n")
    
    if command[:len(GOTO) ] == GOTO:
        new_location = command[len(GOTO):]
        if new_location in here['neighbors']:
            world['player']['location'] = new_location
            return "\nYou went to the " + new_location

    return "Unknown command: "+command
    
def render_ending(world):
    '''
    Create the message to be displayed at the end of your game.

    Args:
        world (World): The final world state to use in describing the ending.

    Returns:
        str: The ending text of your game to be displayed.
    '''
    if world['status'] == 'won':
        return ("\n             You win!! \n" +
                    "Bojangles has found the Ruby Monkey. His hopes and dreams have been realized.  \n" +
                    "Thank you for helping guide him in his journey.")
    elif world['status'] == 'lost':
        return "You lose!"
    elif world['status'] == 'quit':
        return 
    

    
def choose(options):
    '''
    Consumes a list of commands, prints them for the user, takes in user input
    for the command that the user wants (prompting repeatedly until a valid
    command is chosen), and then returns the command that was chosen.

    Note:
        Use your answer to Programming Problem #42.3

    Args:
        options (list[str]): The potential commands to select from.

    Returns:
        str: The command that was selected by the user.
    '''
    print("You can: \n")
    for option in options:
        print(option)
        response = 0
    while response not in options:
        response = input("\nWhat will you do? ")
    return response

############# Main Function ##############
# Do not modify anything below this line #
##########################################
def main():
    '''
    Run your game using the Text Adventure console engine.
    Consumes and produces nothing, but prints and indirectly takes user input.
    '''
    print(render_introduction())
    world = create_world()
    while world['status'] == 'playing':
        print(render(world))
        options = get_options(world)
        command = choose(options)
        print(update(world, command))
    print(render_ending(world))

if __name__ == '__main__':
    main()
