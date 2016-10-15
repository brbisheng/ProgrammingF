# The level "easy". Question is stored as a one-element list
# Its corresponding answers are stored as a 5-element list.
# The number of blanks will be used frequently, so I define a variable to store it.

easy_question_li = ["***Excerpts from 'The Conquest of Happiness'***: "
                    "Animals are __1__ so long as they have __2__ "
                    "and enough to __3__. "
                    "Human beings, one feels, __4__ to be, " 
                    "but in the __5__ world they are not, " 
                    "at least in a great majority of cases."]
easy_answers_li = ["happy", "health", "eat", "ought", "modern"]
nb_easy = len(easy_answers_li)

# The level "medium". Question is stored as a one-element list
# Its corresponding answers are stored as a 6-element list.

medium_question_li = ["***Excerpts from 'The Conquest of Happiness'***: " 
                      "It is held that drink and petting are the gateways to __1__, "
                      "so people get __2__ quickly, and try not to __3__ "
                      "how much their partners __4__ them. "
                      "After a sufficient amount of drink, "
                      "men begin to weep, and to lament " 
                      "how __5__ they are, morally, of the __6__ of their mothers."]

medium_answers_li = ["joy", "drunk", "notice", "disgust", "unworthy", "devotion"]
nb_medium = len(medium_answers_li)

# The level "hard". Question is stored as a one-element list
# Its corresponding answers are stored as an 8-element list.

hard_question_li = ["***Excerpts from 'The Theory of Moral Sentiments'***: " 
                    "We suffer more, it has already been observed, " 
                    "when we fall from a __1__ to a __2__ situation, " 
                    "than we ever enjoy when we rise from a __3__ to a __4__. "
                    "Security, therefore, is the first and the principal object of prudence. "
                    "It is __5__ to expose our health, our fortune, our rank, or reputation, "
                    "to any sort of hazard. It is rather __6__ than enterprising, "
                    "and more anxious to __7__ the advantages which we already possess, "
                    "than forward to prompt us to the acquisition of still __8__ advantages."]
hard_answers_li = ["better", "worse", "worse", "better", "averse", "cautious", "preserve", "greater"]
nb_hard = len(hard_answers_li)


# In[ ]:

def define_game_difficulty():
    """Users choose the game level.
    
    Inputs: 
        None.
    
    Outputs: 
        1. the paragraph to be filled (as a one-element list of strings)
        2. the corresponding answers (as a list of strings)
        3. the difficulty level (as a string)
            
    """
    level = raw_input("***Please select the game difficulty: 'easy', 'medium', or 'hard'***\n"
                      "***'1': 'easy'; '2': 'medium', or '3': 'hard'." 
                         "Your choice: ")
    # returns as tuple
    # A tuple could store different types of variables
        
    if level.lower().find('1') == 0 or level.lower().find('e') == 0:
        return easy_question_li, easy_answers_li, 'easy', nb_easy

    
    elif level.lower().find('2') == 0 or level.lower().find('m') == 0:
        return medium_question_li, medium_answers_li, 'medium', nb_medium
    
    elif level.lower().find('3') == 0 or level.lower().find('h') == 0:
        return hard_question_li, hard_answers_li, 'hard', nb_hard
    
    else:
        print "\nPlease enter a valid game level by typing 1, 2 or 3."
        return define_game_difficulty()


# Now I define a helper function which will be used to check whether the \
# input index is a valid one.

def check_input_index(valid_nu_li):
    """This function will be used later to check whether the input index \
    is valid.

    Input:
        1. the list "remaining" which contains index of blanks to be filled
    Output:
        1. a valid number (as a string)

    """
    global blank_to_fill_nb

    while True:
        
        blank_to_fill_nb = raw_input("***Please input the index of blank: ")
        try:
            int(blank_to_fill_nb)
        except:
            print "***please input a valid value from the following set: " + str(valid_nu_li)
        else:
            if int(blank_to_fill_nb) not in valid_nu_li:
                print "***please input a valid value from the following set: " + str(valid_nu_li)
            else:
                break
    return blank_to_fill_nb

# Now I define another helper function to check whether the guess of user\
# is correct.

def check_guess(correct_answer):
    """This helper function will be used later to check whether the input guess \
    corresponds to the correct one.

    Input:
        1. the correct answer (as a string)
    Output:
        1. user's guess (as a string)
        2. the accumulated mistakes the users have made (as an integer)

    """

    global your_guess
    while True:
        your_guess = raw_input("***Please input your guess: ") 
        if your_guess != correct_answer:
            print "Not correct, Please try again!"
            global error_count
            error_count += 1
        else:
            break
    return your_guess, error_count




# Instead of following the linear order such as "1, 2, 3 ..." to fill in the blanks, 
# I allow the users to select which blank to fill. 
# Mainly for this reason, the function has more than 18 lines.

def filling_the_blanks(question = easy_question_li, answers = easy_answers_li, nb_of_blanks = nb_easy):
    
    """ Users are required to fill in the blanks. I write some simple codes to     make sure that the users enter valid choices when selecting which blank to fill.
    
    Input: 1. the paragraph to be filled. (as a list of one element)
           2. the corresponding answers. (as a list)
           3. the number of blanks to be filled.(as an integer)
           
    output: 1. the correctly filled paragraph (as a list of one element)
            2. the number of errors the user has made (as an integer)
    
    One feature:
    I allow the users to choose the blank they would like to fill in any order.
    
    """
    # I make a copy of the question_list so that any fill-in-blank does not
    # make any modification on the original question_list.
    
    question_copy = list(question)
    
    # I remind the user of the question.
    
    print question_copy
    
    # I define a list to keep track of the indices of blanks which have 
    # not been filled. I call this variable remaining. 
    # Here I initialize it as a list of integers from 1 to number_of_blanks.
    
    remaining = range(1,nb_of_blanks+1)
    
    # My idea is that, whenever one blank is correctly filled, I will \
    # remove the the index of that blank out of the remaining list. \
    # I use the following while loop to accomplish this idea.
    # The following variable ensures that the loop keeps going as long as the list is not empty.
    min_len = 0
    while len(remaining) > min_len:
        
        # The following function checks whether the index chosen by the users \
        # is valid: it must be one number in the remaining list.

        check_input_index(remaining)
                    
        # If the index chosen is valid, I use it to identify the blank to be filled.
        
        blank_to_fill = "__" + str(blank_to_fill_nb) + "__"    
        
        # The following function checks whether the guess of user is correct.
        # If not correct, then the number of errors made will be updated.

        check_guess(answers[int(blank_to_fill_nb)-1])
                
        # If correct, the user is celebrated.
        
        print "****Your guess is correct!****"
        
        # I now identify the position of that blank to be filled.
        # Then I replace the blank by the correct guess of the user.
        # At last I make the user visualize how the question looks like now.
        
        posi =question_copy[0].find(blank_to_fill)
        question_copy[0] = question_copy[0][:posi] + your_guess + question_copy[0][posi+5:]
        print question_copy
       
        # I remove the index of the correctly filled blank out of the remaining list. 
        
        remaining.pop(remaining.index(int(blank_to_fill_nb)))

    print "***Well Done!" + " The errors you have made: " + str(error_count)
    return question_copy


# In[ ]:
# I create and initialize the following global variable to count total wrong guesses.
error_count = 0
def game():
    """By executing this function, we could the full game.
    It will first ask the users to choose the game level.
    Users will then fill in the blanks following the instructions.
    At last, users are asked whether they would like to play again.
    Inputs:
        None.
    Outputs:
        None.
    """
    print "***Welcome to my world of Mad_Lib!***"
    question_li, answers_li, game_level, nb_of_blanks = define_game_difficulty()
    
    print "***You have chosen the game level " + game_level + "\n" + "***Good luck!"
    
    filling_the_blanks(question_li, answers_li, nb_of_blanks)
    
    playagain = raw_input("***Would you love to play again? If Yes, simply type 'y',"
                          " otherwise, you could type anything to quit the game.***")
    
    # By defining the following variable, I set the position of "y" equal to 0. \
    # Any "y" at this position will be recognized as "Yes".

    y_pos = 0

    # If "Yes", the game will continue; otherwise, the game will be ended.
    
    if playagain.lower().find("y") == y_pos:
        # I could reset the variable to zero. So that the count will be initialized 
        # global error_count
        # error_count = 0
        return game()
    else:
        print "***Great, thanks a lot! Goodbye, and see you next time!***"
        # I reset the variable to zero.
        global error_count
        error_count = 0
    


# In[ ]:

game()
