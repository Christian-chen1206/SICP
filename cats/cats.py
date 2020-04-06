"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    sum=-1
    for paragraph in paragraphs:
        if select(paragraph):
            sum+=1
            if sum==k:
                return paragraph
    return ''


    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def f(paragraphs):
        for i in topic:
            for paragraph in split(remove_punctuation(paragraphs)):
                if i==lower(paragraph):
                    return True
        return False
    return f
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if typed_words==[] or reference_words==[]:
        return 0.0
    i=0
    sum=0
    while i<len(typed_words):
        if i>=len(reference_words):
            return sum/len(typed_words)*100
        if typed_words[i]==reference_words[i]:
            sum+=1

        i+=1
    return sum/len(typed_words)*100

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    if typed=="":
        return 0.0
    return (len(typed)/5)/(elapsed/60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    flag=False
    diff=limit
    word=""
    for valid_word in reversed(valid_words):
        if valid_word==user_word:
            return valid_word
        elif diff_function(user_word,valid_word,limit)<=diff:
            word=valid_word
            flag=True
            diff=diff_function(user_word,valid_word,limit)
    if flag:
        return word
    else:
        return user_word

    # END PROBLEM 5


def sphinx_swap(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6  
    def helper(begin, end, limits, now):
        if now>limits:
            return limits+1
        if len(begin)==1 or len(end)==1:
            return (begin[0]!=end[0])+abs(len(begin)-len(end))
        else:
            now+=(begin[0]!=end[0])
            return helper(begin[1:],end[1:],limits,now)+(begin[0]!=end[0])
    return helper(start,goal,limit,0)
    # END PROBLEM 6


def feline_fixes(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    def helper(begin,end,limits,now):

        if now>limits:# Fill in the condition
            # BEGIN
            return now
        if begin == end:
            return 0
        elif len(begin) == 0 or len(end) == 0:
            return max(len(begin), len(end))
        elif begin[0] == end[0]:
            return helper(begin[1:], end[1:], limits,now)
        else:
            add_diff = helper(begin, end[1:], limits,now+1) + 1
            remove_diff = helper(begin[1:], end,limits,now+1) + 1
            substitute_diff = helper(begin[1:], end[1:], limits,now+1) + 1
        return min(add_diff, remove_diff, substitute_diff)
    return helper(start,goal,limit,0)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'


###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    i=0
    while i<len(typed):
        if typed[i]!=prompt[i]:
            send(dict(id=id,progress=(i/len(prompt))))
            print(i/len(prompt))
            return None
        else:
            i+=1
    send(dict(id=id,progress=(i/len(prompt))))
    print((i/len(prompt)))
    return None
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    all_time=[]
    for times in times_per_player:
        i=0
        time=[]
        while i<len(times)-1:
            time.append(times[i+1]-times[i])
            i+=1
        all_time.append(time)
    class Game():
        def __init__(self,words,all_time):
            self.a,self.b=words,all_time  
        def __repr__(self):
            return 'Game {} {}'.format(self.a, self.b)
        def __getitem__(self, index):
            a=([self.a]+[self.b])
            return a[index]

    game=Game(words,all_time)
    return game
    # END PROBLEM 9
def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])

def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.
    Returns:
        a list of lists containing which words each player typed fastest
    """
    players = range(len(all_times(game)))  # An index for each player
    words = range(len(all_words(game)))    # An index for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    players_list=[[] for player in players]
    for word in words:
        now_min=time(game,0,word)
        index=0
        for player in players:
            if time(game,player,word)<now_min or (player==0 and time(game,player,word)==now_min):
                now_min=time(game,player,word)
                index=player

        players_list[index].append(word_at(game,word))
                
    return players_list 
    # END PROBLEM 10




enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)