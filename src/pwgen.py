#!/usr/bin/python

'''
pwgen.py

Pseudo-random password generator.
'''

__title__     = 'pwgen'
__author__    = 'Odmar Miranda'
__version__   = '00.05.00'
__date__      = '2020-09-07'
__description__ = 'Módulo para geração de senhas pseudo-aleatórias.'
__long_description__ = '''\n
Este módulo gera senhas pseudo-aleatórias de comprimento variável de
acordo com os parâmetros recebidos.
\n'''

__license__   = 'GNU GPLv3 http://www.gnu.org/licenses'
__copyright__ = '\u00A9 2014, 2020 Odmar Miranda'


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Revisions
# Version-  ---Date---  --------------------Comments--------------------
# 0.1.0     2012-07-17  - First version.
# 0.2.0     2014-01-28  - Added the characters '! *?' to the valid
#                         character set.
#                       - 'Gerar' function has been renamed to
#                         'Generate' and its parameters have been
#                         changed.  The function now also allows to
#                         define the type of characters used to generate
#                         the password.
#                       - VALIDOS constant has been replaced by
#                         constants: SYMBOLS, DIGITS, UPPER_LETTERS and
#                         LOWER_LETTERS.
#                       - Validation routines for the input parameters
#                         of 'Generate' function were introduced.
#                       - The screen displayed by the program when the
#                         module is directly executed was modified.
# 0.3.0     20140201    - The '+' character has been added to the
#                         character set of the SYMBOLS constant.
#                       - The 'content' parameter of 'Generate' function
#                         has been eliminated and the 'pattern'
#                         parameter is used instead.
#                       - Validation of 'pattern' parameter has been
#                         included.
#                       - The definition of valid characters for
#                         password formation has been changed.
#                       - 'valid' variable has been renamed to
#                         'valid_chars'.
#                       - The screen displayed by the program when the
#                         module is directly executed was modified.
# 0.3.1     20140201    - Fixed error in the validation of the 'pattern'
#                         parameter.
# 000400    20140212    - New versioning scheme was adopted.
#                       - Module renamed from 'genpass.py' to
#                         'pwgen.py'.
#                       - 'GetEntropy ()' function included to assess
#                         the strength of the generated password.  The
#                         function applies the formula presented in
#                         NIST's Electronic Authentication Guideline
#                         (item A.1).
#                       - 'Generate' function now returns entropy.
# 0.5.0     2020-09-07  - Updated to Python 3 and above.
#                       - New version numbering scheme adopted.

# imports ---------------------------------------------------------------------
import math
import random

# classes ---------------------------------------------------------------------

# contansts -------------------------------------------------------------------
SYMBOLS = '!#$%&*+?@'
DIGITS = '0123456789'
UPPER_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOWER_LETTERS = 'abcdefghijklmnopqrstuvwxyz'

# functions -------------------------------------------------------------------
def Generate(length=8, pattern=15):
    '''Returns a pseudo-random password of the defined length.

Returned password will consist of the characters defined by the
'pattern' parameter and will be sized according to the 'size'
parameter.

Parameters:
length  (int) - Password length to be generated.  By default, 8
                characters.
                Length must be greater than or equal to 4 and less
                than or equal to 64.
pattern (int) - Value whose binary representation indicates which
                characters will be used in forming the password.  By
                default, all characters will be used.
                The 'pattern' value must be less than or equal to 15,
                which is equivalent to a 4-bit binary number.
                The parameter value is interpreted as follows:
                  - bit 1 - enables the use of lowercase letters.
                  - bit 2 - enables the use of uppercase letters.
                  - bit 3 - enables the use of digits.
                  - bit 4 - enables the use of special characters and
                            punctuation marks.
                For example:
                Decimal  Binary  Characters used in the password
                ------------------------------------------------
                15       1111    all characters
                7        0111    digits, upper and lower case
                6        0110    digits and capital letters
                3        0011    upper and lowercase
Return:
password (string) - pseudo-random password.
entropy  (int)    - password strength, measured in bits.
'''
    # Length parameter validation
    if not isinstance(length, int):
        raise TypeError('O comprimento deve ser um número inteiro.')
    elif length < 4:
        raise ValueError('O comprimento deve ser maior ou igual a 4.')
    elif length > 64:
        raise ValueError('O comprimento deve ser menor ou igual a 64.')
    
    # Pattern parameter validation
    if not isinstance(pattern, int):
        raise TypeError('O padrão deve ser um número inteiro.')
    elif pattern < 1:
        raise ValueError('O padrão deve ser maior ou igual a 1.')
    elif pattern > 15:
        raise ValueError('O padrão deve ser menor ou igual a 15.')
    
    # Character set definition
    # Use binary math
    valid_chars = ''
    if pattern & 1:
        valid_chars += LOWER_LETTERS
    pattern >>= 1
    if pattern & 1:
        valid_chars += UPPER_LETTERS
    pattern >>= 1
    if pattern & 1:
        valid_chars += DIGITS
    pattern >>= 1
    if pattern & 1:
        valid_chars += SYMBOLS
    
    # Password generation
    characters = []
    for i in range(length):
        characters.append(random.choice(valid_chars))
    password = ''.join(characters)
    entropy = GetEntropy(len(valid_chars), length)
    return (password, entropy)

def GetEntropy(nchars, psize):
    '''Assess password strength.'''
    
    return int(math.log(nchars**psize, 2))

# main ------------------------------------------------------------------------
if __name__ == '__main__':
    print (80*'-')
    print (f'''
{__title__} - {__description__}
{__version__}

Uso:
    import pwgen
    senha, entropia = pwgen.Generate(spam, eggs)

Obs.: spam é o tamanho da senha e eggs é o padrão de caracteres.
      spam deve ser maior ou igual a 4 e menor ou igual a 64.
      eggs deve ser maior ou igual a 1 e menor ou igual a 15.
      eggs é interpretado conforme sua representação binária.
          bit 1 - habilita o uso de letras minúsculas.
          bit 2 - habilita o uso de letras maiúsculas.
          bit 3 - habilita o uso de dígitos.
          bit 4 - habilita o uso de símbolos e sinais de pontuação.
      Por exemplo:
          Decimal  Binário  Caracteres usados na senha
          ------------------------------------------------
          7        0111     dígitos, maiúsculas e minúsculas
          6        0110     dígitos e maiúsculas
          3        0011     maiúsculas e minúsculas
''')
    print (80*'-')
    print ('\nInício do auto-teste.')
    print ('\nGerando 10 senhas pseudo-aleatórias de 8 caracteres.')
    for j in range(10):
        print (j+1,'\t- ', Generate()[0])
    print ('\nFim do auto-teste.\n')
