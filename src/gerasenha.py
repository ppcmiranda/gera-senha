#!/usr/bin/python3

"""
gerasenha.py

Parameterizable password generator.

This program generates pseudo-random passwords of variable length
according to parameters defined by the user.

Available classes:
- PasswordGenerator: Show the interface.

Usage:
python3 gerasenha.py
"""

__title__ = 'Gerador de Senhas'
__author__ = 'Odmar Miranda'
__version__ = '2.0.0'
__date__ = '2020-09-05'
__description__ = 'Gerador parametrizável de senhas.'
__long_description__ = '''\n
Este programa gera senhas pseudo-aleatórias de tamanho variável de
acordo com parâmetros definidos pelo usuário.  Para isso, utiliza
o módulo 'pwgen'.
\n'''
__license__ = 'GNU GPLv3 http://www.gnu.org/licenses'
__copyright__ = '\u00A9 2014, 2020 Odmar Miranda'
__release__ = '2020-09-07'

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
# 0.1.0     2014-01-28  - First version.
# 0.2.0     2014-02-09  - Minor code improvements:
#                         - GUI style definitions have been removed from
#                           code to an external file (basic_style.txt)
#                           as much as possible.
#                         - references to the object of the 'Label'
#                           class are no longer maintained, so these
#                           objects are created and positioned in a
#                           single operation.
#                         - some unnecessary, useless or redundant
#                           options have been removed.
#                         - the 'entry_Password' text box has been
#                           removed from the tab order.
#                         - the 'spinbox_Length' selector no longer
#                           accepts editing of its value via the
#                           keyboard, so the value can only be
#                           changed using the up and down arrows with
#                           the mouse.
#                         - the 'button_Clear' button, for clearing the
#                           generated password, has been removed and
#                           therefore the 'ClearPassword' and
#                           'ClearButtonHandler' methods have also been
#                           removed.
#                         - the 'button_Exit' button for program
#                           termination has been removed and therefore
#                           the 'ExitButtonHandler' method has also been
#                           removed.
#                         - the 'sys' module is no longer used to close
#                           the program.
#                         - the 'App' class has been renamed to
#                           'PasswordGenerator'.
# 0.3.0     2014-02-12  - The selection of the generated password size
#                         is made by a slider.  As a result, the
#                         following changes were made:
#                         - the 'spinbox_Length' selector has been
#                           deleted.
#                         - the label previously associated with the
#                           selector has been eliminated.
#                         - the function 'SetLength' has been modified
#                           in order to receive the parameter 'length'.
#                         - the 'SetLength' function also calls the
#                           'GeneratePassword' function, so that a new
#                           password is generated whenever the slider is
#                           moved and for the same reason, the program
#                           already starts generating a password of the
#                           standard size, using all available
#                           characters.
#                         - the use of special characters is no longer
#                           set as default.
# 010000    2014-02-12  - A new versioning scheme was adopted.
#                       - Included the 'entropy' attribute to receive
#                         and store the password strength.
#                       - 'ShowEntropy' function is included to display
#                         password robustness in the interface.
#                       - Robustness is shown in a row of buttons,
#                         highlighted as appropriate.
#                       - The scale adopted follows the suggestion of
#                         Tyler Akins, presented at
#                         'http://rumkin.com/tools/password/passchk.php'.
#                       - The language used in the interface has been
#                         unified, so all information presented to the
#                         user is in Portuguese.
# 010100    2014-02-14  - Changes in the status of the checkboxes will
#                         automatically generate a new password.
#                       - The scale no longer displays a label.
#                       - The label for the password strength buttons
#                         has been removed.
#                       - The way of creating the button line has been
#                         modified.  As a consequence, the
#                         'ShowEntropy' function has also been changed.
#                       - Updated the name of the password generator
#                         module, which was renamed to 'pwgen', instead
#                         of 'genpass'.
# 2.0.0     2020-09-05  - New version numbering scheme adopted.
#                       - Program update do Python 3.
#                       - Complete GUI revision to use ttk widgets.
#                       - 'basic_style.txt' file renamed to
#                         'option_db.txt'.
#                       - Some widgets was renamed.

# imports --------------------------------------------------------------------
import tkinter as tk
import tkinter.messagebox

from tkinter import ttk

import pwgen

# constants ------------------------------------------------------------------
ABOUT = '''
Este programa é um software livre: você pode
redistribuí-lo ou modificá-lo dentro dos termos
da Licença Pública Geral GNU como publicada
pela Fundação do Software Livre (FSF), tanto
na versão 3 da Licença quanto em qualquer
versão posterior.
'''

# classes --------------------------------------------------------------------
class Application():
    '''Application main window.'''
    
    def __init__(self):
        '''Initialize interface objects.'''

        self.root = tk.Tk()
        self.root.title(__title__)
        self.root.option_add('*tearOff', tk.FALSE)
        self.build_interface()
        self.root.resizable(False, False)
        self.generate_first()

    def build_interface(self):
        '''Build and display application interface.'''
        
        # Read default style for tkinter widgets from external file.
        self.root.option_readfile('option_db.txt')
        # Get default style for ttk widgets.
        self.style = ttk.Style()
        # Configure custom style for ttk widgets.
        self.style.configure('TLabel', anchor='e')
        self.style.configure('PW.TLabel', relief='sunken', anchor='w')
        self.style.configure('Tool.TButton', relief='flat')

        # Loads images.
        self.exit_img = tk.PhotoImage(file='assets/exit.png')
        self.info_img = tk.PhotoImage(file='assets/info.png')
        self.help_img = tk.PhotoImage(file='assets/help.png')
                
        # Main containers.
        self.toolbar_frame = ttk.Frame(self.root)
        self.toolbar_frame.grid(row=0,
                                column=0,
                                padx=5,
                                pady=5,
                                sticky='wens'
                                )
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1,
                             column=0,
                             padx=5,
                             pady=5,
                             sticky='wens'
                             )
        
        # Toolbar buttons.
        self.help_button = ttk.Button(self.toolbar_frame,
                                      style='Tool.TButton',
                                      command = self.show_help,
                                      image = self.help_img
                                     )
        self.help_button.pack(side='left')
        self.about_button = ttk.Button(self.toolbar_frame,
                                       style='Tool.TButton',
                                       command = self.show_info,
                                       image = self.info_img
                                      )
        self.about_button.pack(side='left')
        self.exit_button = ttk.Button(self.toolbar_frame,
                                      style='Tool.TButton',
                                      command = self.exit,
                                      image = self.exit_img
                                     )
        self.exit_button.pack(side='left')
        
        # Main widgets.
        # GUI labels.
        ttk.Label(self.main_frame, text='Usar:').grid(row=0,
                                                      column=0,
                                                      sticky='e'
                                                     )
        ttk.Label(self.main_frame, text='Tamanho:').grid(row=1,
                                                         column=0,
                                                         sticky='e'
                                                        )
        ttk.Label(self.main_frame, text='Senha:').grid(row=2,
                                                       column=0,
                                                       sticky='e'
                                                      )
        # GUI configuration buttons and associated variables.
        self.symbols_value = tk.IntVar()
        self.digits_value = tk.IntVar()
        self.upper_value = tk.IntVar()
        self.lower_value = tk.IntVar()
        self.symbols_check = ttk.Checkbutton(self.main_frame,
                                             text='Símbolos',
                                             command=self.generate_pw,
                                             onvalue=8,
                                             variable=self.symbols_value
                                            )
        self.digits_check = ttk.Checkbutton(self.main_frame,
                                            text='Dígitos',
                                            command=self.generate_pw,
                                            onvalue=4,
                                            variable=self.digits_value
                                           )
        self.upper_letters_check = ttk.Checkbutton(self.main_frame,
                                                   text='Maiúsculas',
                                                   command=self.generate_pw,
                                                   onvalue=2,
                                                   variable=self.upper_value
                                                  )
        self.lower_letters_check = ttk.Checkbutton(self.main_frame,
                                                   text='Minúsculas',
                                                   command=self.generate_pw,
                                                   onvalue=1,
                                                   variable=self.lower_value
                                                  )
        self.symbols_check.grid(row=0, column=1, sticky='we', padx=5)
        self.digits_check.grid(row=0, column=2, sticky='we', padx=5)
        self.upper_letters_check.grid(row=0, column=3, sticky='we', padx=5)
        self.lower_letters_check.grid(row=0, column=4, sticky='we', padx=5)
        # GUI configuration spinbox and initial setting.
        self.length_setting = ttk.Spinbox(self.main_frame,
                                          command=self.generate_pw,
                                          from_=4.0,
                                          to=64.0,
                                          width=2
                                         )
        self.length_setting.grid(row=1, column=1, sticky='w', padx=5)
        # GUI robustness display bar.
        self.robustness_bar = ttk.Progressbar(self.main_frame,
                                              orient='horizontal',
                                              mode='determinate',
                                              maximum=5,
                                              value=0.0,
                                             )
        self.robustness_bar.grid(row=1,
                                 column=2,
                                 columnspan=2,
                                 sticky='we',
                                 padx=5
                                )
        # GUI command button.
        self.generate_button = ttk.Button(self.main_frame,
                                          text='Nova',
                                          command = self.generate_pw,
                                         )
        self.generate_button.grid(row=1, column=4, sticky='we', padx=5, pady=5)
        # GUI password display.
        self.pw_display = ttk.Label(self.main_frame,
                                    style='PW.TLabel',
                                    padding=5
                                   )
        self.pw_display.grid(row=2,
                             column=1,
                             columnspan=4,
                             sticky='we',
                             padx=5,
                             pady=5
                            )

        # Bind events to corresponding handlers.
        self.help_button.bind('<Return>', self.show_help)
        self.about_button.bind('<Return>', self.show_info)
        self.exit_button.bind('<Return>', self.exit)
        self.generate_button.bind('<Return>', self.generate_pw)
        
    # Event handlers.
    def generate_pw(self, event=None):
        '''Use 'pwgen' module to generate password and update GUI.'''
        
        pattern = self.symbols_value.get() + \
                  self.digits_value.get() + \
                  self.upper_value.get() + \
                  self.lower_value.get()

        if pattern > 0:
            length = int(self.length_setting.get())
            try:
                password, entropy = pwgen.Generate(length, pattern)
            except (TypeError, ValueError):
                pass
            # Update GUI
            self.pw_display.configure(text=password)
            self.ShowEntropy(entropy)
        
    def exit(self, event=None):
        '''Close the application.'''
        self.root.destroy()

    def show_info(self, event=None):
        '''Show application info.'''
        
        title = '{0} - Sobre'.format(__title__)
        msg = '{0}\n\nVersão: {1} - Liberada em: {2}\n\n{3}\n{4}'
        message = msg.format(__description__, __version__, __release__,
                             __copyright__, ABOUT
                             )
        tk.messagebox.showinfo(title, message)

    def show_help(self, event=None):
        '''Show application help.'''
        
        # Configure help window
        help = tk.Toplevel(self.root)
        help.transient(self.root)
        help.title('{0} - Ajuda'.format(__title__))
        # Insert widgets
        text = tk.Text(help, height=16, width=64, padx=5, pady=5)
        text.pack()
        close_button = ttk.Button(help, text='Fechar', command=help.destroy)
        close_button.pack()
        # Load help file
        try:
            with open('help.txt', 'r', encoding='UTF-8') as f:
                for line in f:
                    text.insert(tk.END, line)
        except IOError:
            text.insert(tk.END, 'Nenhuma ajuda disponível.')
        text.config(state='disabled')
        # Show help window
        help.mainloop()
        
    # Helper functions
    def ShowEntropy(self, entropy):
        '''Display password robustness on GUI graphically.
        
        Uses the criteria defined by Tyler Akins at
        <http://rumkin.com/tools/password/passchk.php> to
        define password robustness.
        '''
        
        if entropy < 28:
            self.robustness_bar.configure(value=1.0)
        elif entropy >= 28 and entropy < 36:
            self.robustness_bar.configure(value=2.0)
        elif entropy >= 36 and entropy < 60:
            self.robustness_bar.configure(value=3.0)
        elif entropy >= 60 and entropy < 128:
            self.robustness_bar.configure(value=4.0)
        else:
            self.robustness_bar.configure(value=5.0)

        
    def generate_first(self):
        '''Generate first password at start-up using default parameters.'''
        
        self.symbols_value.set(0)
        self.digits_value.set(4)
        self.upper_value.set(2)
        self.lower_value.set(1)
        self.length = 8
        self.length_setting.set(8)
        
        self.generate_pw()
        
    def run(self):
        '''Run the application's main loop.'''
        
        self.root.mainloop()

# main trap ------------------------------------------------------------------
if __name__ == '__main__':
    Application().run()
