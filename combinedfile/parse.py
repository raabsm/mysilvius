# Parser, based on John Aycock's SPARK examples

from spark import GenericParser
from spark import GenericASTBuilder
from ast import AST
#this is a comment
class GrammaticalError(Exception):
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string

class CoreParser(GenericParser):
    def __init__(self, start):
        GenericParser.__init__(self, start)

    def typestring(self, token):
        return token.type

    def error(self, token):
        raise GrammaticalError(
            "Unexpected token `%s' (word number %d)" % (token, token.wordno))
    def p_chained_commands(self, args):
        '''
            chained_commands ::= single_command
            chained_commands ::= single_command chained_commands
        '''
        if(len(args) == 1):
            return AST('chain', None, [ args[0] ])
        else:
            args[1].children.insert(0, args[0])
            return args[1]

    def p_single_command(self, args):
        '''
            single_command ::= letter
            single_command ::= sky_letter
            single_command ::= number_rule
            single_command ::= movement
            single_command ::= character
            single_command ::= editing
            single_command ::= modifiers
            single_command ::= english
            single_command ::= word_sentence
            single_command ::= word_phrase
            single_command ::= electricity
            single_command ::= pinsetup
        '''
        return args[0]

    def p_movement(self, args):
        '''
            movement ::= up     repeat
            movement ::= down   repeat
            movement ::= left   repeat
            movement ::= right  repeat
        '''
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('movement', [ args[0] ])
            ])
        else:
            return AST('movement', [ args[0] ])

    def p_repeat(self, args):
        '''
            repeat ::=
            repeat ::= number_set
        '''
        if len(args) > 0:
            return args[0]
        else:
            return None
    def p_pinsetup(self,args):
        '''
            pinsetup ::= signal number_set
        '''   
        return AST('pinsetup', [ args[1] ]) 

    def p_electricity(self, args):
        '''
            electricity ::= light _action
        ''' 
        return AST('elec', [ chr(ord('0') + args[1]) ])
    #chr(ord is just a way of adding two ints and converting to str
    def p__action(self, args):
        '''
            _action ::= off
            _action ::= on
            _action ::= status
        '''
        value = {
            'off'    : 0,
            'on'     : 1,
            'status' : 2
        }
        return value[args[0].type]
    def p_number_rule(self, args):
        '''
            number_rule ::= number number_set
            number_rule ::= number thousand_number_set
            number_rule ::= number million_number_set
            number_rule ::= number billion_number_set
        '''
        return AST('char', [ str(args[1]) ])

    def p_number_set(self, args):
        '''
            number_set ::= _firstnumbers
            number_set ::= _tens 
            number_set ::= _tens _ones
            number_set ::= _hundreds
            number_set ::= _hundreds _firstnumbers
            number_set ::= _hundreds _tens
            number_set ::= _hundreds _tens _ones
        '''
        total = 0
        for x in args:
            total += x
        return total 

    def p_thousand_number_set(self, args):
        '''
            thousand_number_set ::= number_set _thousands
            thousand_number_set ::= number_set _thousands number_set
        '''
        total = args[0] * args[1]
        if len(args)>2: total+=args[2]
        return total 
    def p_million_number_set(self, args):
        '''
            million_number_set ::= number_set _millions 
            million_number_set ::= number_set _millions number_set
            million_number_set ::= number_set _millions thousand_number_set
        '''
        total = args[0] * args[1]
        if len(args)>2: total+=args[2]
        return total 
    def p_billion_number_set(self, args):
        '''
            billion_number_set ::= number_set _billions 
            billion_number_set ::= number_set _billions number_set
            billion_number_set ::= number_set _billions thousand_number_set
            billion_number_set ::= number_set _billions million_number_set
        ''' 
        total = args[0] * args[1]
        if len(args)>2: total+=args[2]
        return total 
    def p__firstnumbers(self, args):
        '''
            _firstnumbers ::= zero
            _firstnumbers ::= one
            _firstnumbers ::= two
            _firstnumbers ::= three
            _firstnumbers ::= four
            _firstnumbers ::= five
            _firstnumbers ::= six
            _firstnumbers ::= seven
            _firstnumbers ::= eight
            _firstnumbers ::= nine
            _firstnumbers ::= ten
            _firstnumbers ::= eleven
            _firstnumbers ::= twelve
            _firstnumbers ::= thirteen
            _firstnumbers ::= fourteen
            _firstnumbers ::= fifteen
            _firstnumbers ::= sixteen
            _firstnumbers ::= seventeen
            _firstnumbers ::= eighteen
            _firstnumbers ::= nineteen
        '''
        # doesn't work right now
        #for v in value:
        #    self.__doc__ += "number ::= " + v
        value = {
            'zero'      : 0,
            'one'       : 1,
            'two'       : 2,
            'three'     : 3,
            'four'      : 4,
            'five'      : 5,
            'six'       : 6,
            'seven'     : 7,
            'eight'     : 8,
            'nine'      : 9,
            'ten'       : 10,
            'eleven'    : 11,
            'twelve'    : 12,
            'thirteen'  : 13,
            'fourteen'  : 14,
            'fifteen'   : 15,
            'sixteen'   : 16,
            'seventeen' : 17,
            'eighteen'  : 18,
            'nineteen'  : 19,
        }
        return value[args[0].type]
    def p__tens(self, args):
        '''
            _tens ::= twenty
            _tens ::= thirty
            _tens ::= forty
            _tens ::= fifty
            _tens ::= sixty
            _tens ::= seventy
            _tens ::= eighty
            _tens ::= ninety 
        '''
        value = {
            'twenty'   : 20,
            'thirty'   : 30,
            'forty'    : 40,
            'fifty'    : 50,
            'sixty'    : 60,
            'seventy'  : 70,
            'eighty'   : 80,
            'ninety'   : 90
        }
        return value[args[0].type]
    def p__hundreds(self, args):
        '''
            _hundreds ::= one hundred
            _hundreds ::= two hundred
            _hundreds ::= three hundred
            _hundreds ::= four hundred
            _hundreds ::= five hundred
            _hundreds ::= six hundred
            _hundreds ::= seven hundred
            _hundreds ::= eight hundred
            _hundreds ::= nine hundred
        '''
        value = {
            'one'   : 100,
            'two'   : 200,
            'three' : 300,
            'four'  : 400,
            'five'  : 500,
            'six'   : 600,
            'seven' : 700,
            'eight' : 800,
            'nine'  : 900
        }
        return value[args[0].type]
    def p__thousands(self, args):
        '''
            _thousands ::= thousand
        '''
        return 1000
    def p__millions(self, args):
        '''
            _millions ::= million
        '''
        return 1000000
    def p__billions(self, args):
        '''
            _billions ::= billion
        '''
        return 1000000000
    def p__ones(self, args):
        '''
            _ones ::= one
            _ones ::= two
            _ones ::= three
            _ones ::= four
            _ones ::= five
            _ones ::= six
            _ones ::= seven
            _ones ::= eight
            _ones ::= nine
        '''

        value = {
            'one'       : 1,
            'two'       : 2,
            'three'     : 3,
            'four'      : 4,
            'five'      : 5,
            'six'       : 6,
            'seven'     : 7,
            'eight'     : 8,
            'nine'      : 9
        }
        return value[args[0].type]
    def p_sky_letter(self, args):
        '''
            sky_letter ::= sky letter
        '''
        ast = args[1]
        ast.meta[0] = ast.meta[0].upper()
        return ast

    def p_letter(self, args):
        '''
            letter ::= arch
            letter ::= bravo
            letter ::= charlie
            letter ::= delta
            letter ::= eco
            letter ::= echo
            letter ::= fox
            letter ::= golf
            letter ::= hotel
            letter ::= india
            letter ::= julia
            letter ::= kilo
            letter ::= line
            letter ::= mike
            letter ::= november
            letter ::= oscar
            letter ::= papa
            letter ::= queen
            letter ::= romeo
            letter ::= sierra
            letter ::= tango
            letter ::= uniform
            letter ::= victor
            letter ::= whiskey
            letter ::= whisky
            letter ::= xray
            letter ::= expert
            letter ::= yankee
            letter ::= zulu
        '''
        if(args[0].type == 'expert'): args[0].type = 'x'
        return AST('char', [ args[0].type[0] ])

    def p_character(self, args):
        '''
            character ::= act
            character ::= colon
            character ::= semicolon
            character ::= single quote
            character ::= double quote
            character ::= equal
            character ::= space
            character ::= tab
            character ::= bang
            character ::= hash
            character ::= dollar
            character ::= percent
            character ::= carrot
            character ::= ampersand
            character ::= star
            character ::= late
            character ::= rate
            character ::= minus
            character ::= underscore
            character ::= plus
            character ::= backslash
            character ::= dot
            character ::= dit
            character ::= slash
            character ::= question
            character ::= comma
        '''
        value = {
            'act'   : 'Escape',
            'colon' : 'colon',
            'semicolon' : 'semicolon',
            'single': 'apostrophe',
            'double': 'quotedbl',
            'equal' : 'equal',
            'space' : 'space',
            'tab'   : 'Tab',
            'bang'  : 'exclam',
            'hash'  : 'numbersign',
            'dollar': 'dollar',
            'percent': 'percent',
            'carrot': 'caret',
            'ampersand': 'ampersand',
            'star': 'asterisk',
            'late': 'parenleft',
            'rate': 'parenright',
            'minus': 'minus',
            'underscore': 'underscore',
            'plus': 'plus',
            'backslash': 'backslash',
            'dot': 'period',
            'dit': 'period',
            'slash': 'slash',
            'question': 'question',
            'comma': 'comma'
        }
        return AST('raw_char', [ value[args[0].type] ])

    def p_editing(self, args):
        '''
            editing ::= slap        repeat
            editing ::= scratch     repeat
        '''
        value = {
            'slap'  : 'Return',
            'scratch': 'BackSpace'
        }
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('raw_char', [ value[args[0].type] ])
            ])
        else:
            return AST('raw_char', [ value[args[0].type] ])

    def p_modifiers(self, args):
        '''
            modifiers ::= control single_command
            modifiers ::= alt single_command
            modifiers ::= alternative single_command
        '''
        value = {
            'control' : 'ctrl',
            'alt' : 'alt',
            'alternative' : 'alt'
        }
        if(args[1].type == 'mod_plus_key'):
            args[1].meta.insert(0, value[args[0].type])
            return args[1]
        else:
            return AST('mod_plus_key', [ value[args[0].type] ], [ args[1] ] )

    def p_english(self, args):
        '''
            english ::= word ANY
        '''
        return AST('sequence', [ args[1].extra ])

    def p_word_sentence(self, args):
        '''
            word_sentence ::= sentence word_repeat
        '''
        if(len(args[1].children) > 0):
            args[1].children[0].meta = args[1].children[0].meta.capitalize()
        return args[1]

    def p_word_phrase(self, args):
        '''
            word_phrase ::= phrase word_repeat
        '''
        return args[1]

    def p_word_repeat(self, args):
        '''
            word_repeat ::= raw_word
            word_repeat ::= raw_word word_repeat
        '''
        if(len(args) == 1):
            return AST('word_sequence', None,
                [ AST('null', args[0]) ])
        else:
            args[1].children.insert(0, AST('null', args[0]))
            return args[1]

    def p_raw_word(self, args):
        '''
            raw_word ::= ANY
            raw_word ::= zero
            raw_word ::= one
            raw_word ::= two
            raw_word ::= three
            raw_word ::= four
            raw_word ::= five
            raw_word ::= six
            raw_word ::= seven
            raw_word ::= eight
            raw_word ::= nine
        '''
        if(args[0].type == 'ANY'):
            return args[0].extra
        return args[0].type

class SingleInputParser(CoreParser):
    def __init__(self):
        CoreParser.__init__(self, 'single_input')
        self.sleeping = False

    def p_sleep_commands(self, args):
        '''
            sleep_commands ::= go to sleep
            sleep_commands ::= start listening
        '''
        if args[-1].type == 'sleep':
            self.sleeping = True
            print 'Going to sleep.'
        else:
            self.sleeping = False
            print 'Waking from sleep'
        return AST('')

    def p_single_input(self, args):
        '''
            single_input ::= END
            single_input ::= sleep_commands END
            single_input ::= chained_commands END
        '''
        if len(args) > 0 and not self.sleeping:
            return args[0]
        else:
            return AST('')

def parse(parser, tokens):
    return parser.parse(tokens)
