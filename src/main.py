#!/usr/bin/python


# Title: PyLly Dalc
# Synopsis: A python based rally car weight distribution calculator
# Version: v0.01
# Website: http://code.google.com/p/pylly-dalc/
# Date: 10/07/2012
# Author: thims (Tomm Smith)
# Contact: root.packet@gmail.com

import sys
import gtk
import gtk.glade
import pango


glade_file = 'weight_distribution_calculator.glade'




class distCalc:
    def __init__(self, FL, FR, RL, RR):
        """ Initialize the default environment of our class upon instantiation. 
            Args:
                @FL - Front Left Weight
                @FR - Front Right Weight
                @RL - Rear Left Weight
                @RR - Rear Right Right

            
            Return Status:
                - 0 upon failure
                - Upon success a tuple data structure is returned

        """
        
        # Misc variables to make life easier
        self.FL = FL
        self.FR = FR
        self.RL = RL
        self.RR = RR
        self.total_weight = self.FL + self.FR + self.RL + self.RR

        # Data Struct declaration
        self.weights = {'front' : {'left' : {'perc' : 0, 'weight' : self.FL},
                                        'right' : {'perc' : 0, 'weight' : self.FR},
                        'total' : {'perc' : 0, 'weight' : self.FL + self.FR}
                                          },
                                'rear'  : {'left' : {'perc' : 0, 'weight' : self.RL},
                                            'right' : {'perc' : 0, 'weight' : self.RR},
                        'total' : {'perc' : 0, 'weight' : self.RL + self.RR}
                                           },
                                'sides'  : {'left' : {'perc' : 0, 'weight' : self.FL + self.RL},
                                             'right' : {'perc' : 0, 'weight' : self.FR + self.RR}
                                            },
                                'cross' : {'perc' : 0, 'weight' : self.RL + self.FR}
                               }


    #### Local functions ####
    def dist_perc(self, weight):
        """ return the distributed percentage of said provided weight """
        perc = (weight / float(self.total_weight)) * 100
        perc_rnd = "%.1F" % perc

        return perc_rnd


    #### Tools to said parent Object ####
    def calculate_weights(self):
        """ Calculate the weight distributed and percentage of the 8 single points around the car
            Points:
                - Front Left
                - Front Right
                - Rear Left
                - Rear Right
                - Left Side
                - Right Side
                - Front
                - Rear
        """
        # Front
        self.weights['front']['left']['perc'] = self.dist_perc(self.weights['front']['left']['weight'])
        self.weights['front']['right']['perc'] = self.dist_perc(self.weights['front']['right']['weight'])
        self.weights['front']['total']['perc'] = self.dist_perc(self.weights['front']['total']['weight'])

        # Rear
        self.weights['rear']['left']['perc'] = self.dist_perc(self.weights['rear']['left']['weight'])
        self.weights['rear']['right']['perc'] = self.dist_perc(self.weights['rear']['right']['weight'])
        self.weights['rear']['total']['perc'] = self.dist_perc(self.weights['rear']['total']['weight'])

        # Sides
        self.weights['sides']['left']['perc'] = self.dist_perc(self.weights['sides']['left']['weight'])
        self.weights['sides']['right']['perc'] = self.dist_perc(self.weights['sides']['right']['weight'])

        # Cross weight
        self.weights['cross']['perc'] = self.dist_perc(self.weights['cross']['weight'])

        return 0




class parentGUI:
    def __init__(self):
        # Define our glade file location
        global glade_file
        path = sys.argv[0]
        path = path[0:-len(path.split('/')[-1])] 

        glade_file = path + glade_file
  
        self.parentGUI = gtk.glade.XML(glade_file, "parentWin")

        self.aboutDlg = aboutDlg()
        
        # Set the title
        gtk.Window(gtk.WINDOW_TOPLEVEL).set_title("Rally DistCalc")

        # GUI Signals
        sigs = {'on_text_entry' : self.sanitize_input, 
            'on_help_about_pressed' : self.aboutDlg.show_dlg,
            'on_calculate_pressed' : self.calculate_pressed,
            'on_file_close_clicked' : gtk.main_quit,
            'gtk_main_quit' : gtk.main_quit}
        self.parentGUI.signal_autoconnect(sigs)


    

    #### Parent GUI Action and Events ####
    def calculate_pressed(self, obj):
        """ We need to calculate and generate our data in many steps so for error
            handling we will use this function to collect all steps of the process.
        """
        self.validate_input()
        self.get_weight_input()
        self.calculate_distribution()
        self.generate_output()


    #### Dialogs ####    
    def show_invChar_dlg(self):
        self.invDlgTree = gtk.glade.XML(glade_file, 'invalidInputDlg')
        self.invDlg = self.invDlgTree.get_widget('invalidInputDlg')
        self.invDlg.run()
        self.invDlg.destroy()
        
        return True


    def show_missChar_dlg(self):
        self.misDlgTree = gtk.glade.XML(glade_file, 'missingInputDlg')
        self.missDlg = self.misDlgTree.get_widget('missingInputDlg')
        self.missDlg.run()
        self.missDlg.destroy()

        return True



    
    #### Input Functions ####
    def sanitize_input(self, obj, data, null, pointer):
        """ Sanitize the users input as they enter it to ensure that the inpust is a
            numeric value. Only numeric values are accepted, floating points are not 
            supported.

            ToDo:
            - Floating Point Entries
        """
        
        try:
            int(data)

            return True

        except ValueError:
            # Prevent a loop situation caused from the event handler being called 
            # after we clear the invalid input
            if data == '':
                return False
            else:
                # Get our full input text, truncate the last string character
                # entered and open the dialog box
                full_text = obj.get_text()
                obj.set_text(full_text[0:len(full_text) - 1])
    
                self.show_invChar_dlg()
                return False


    def validate_input(self):
        """ Validate the user supplied input fields and ensure there are no blanks. 

            Return:
                True - Upon sucess
                False - Upon Failure
        """
        input_flds = ['fl_weight_inp', 'fr_weight_inp', 'rl_weight_inp', 'rr_weight_inp']

        for i in range(len(input_flds)):
            obj = self.parentGUI.get_widget(input_flds[i])
            if obj.get_text() == '':
                self.show_missChar_dlg()
                raise NameError('Invalid input in text fields.')
            else:
                continue

        return True
                
    
    def get_weight_input(self):
        """ Get the input in the text input fields, validate it and return it 
            as a list if validation went well. 

            ToDo:
                - error handling
        """
        self.input_weights = {'FL' : 0,
                              'FR' : 0,
                              'RL' : 0,
                              'RR' : 0
                             }
         
        self.input_weights['FL'] = int(self.parentGUI.get_widget('fl_weight_inp').get_text())
        self.input_weights['FR'] = int(self.parentGUI.get_widget('fr_weight_inp').get_text())
        self.input_weights['RL'] = int(self.parentGUI.get_widget('rl_weight_inp').get_text())
        self.input_weights['RR'] = int(self.parentGUI.get_widget('rr_weight_inp').get_text())
        
        return 0


    #### Data Output ####
    def calculate_distribution(self):
        """ Calculate the weight distribution and return a list of the results following said structure.
          
            Stucture: 
        """
        # Instantiate our calculator
        self.weightCalc = distCalc(self.input_weights['FL'], self.input_weights['FR'], 
                        self.input_weights['RL'], self.input_weights['RR'])

        # Get our standard weight distributions (Everything but cross weight)
        self.weightCalc.calculate_weights()

        # Store our calculated weights and destroy our object
        self.weights = self.weightCalc.weights
        del self.weightCalc


    def get_tView_buf(self):
        self.tView = self.parentGUI.get_widget('diagram_display')
        self.tViewBuf = self.tView.get_buffer()

        font = pango.FontDescription("monospace 10")
        self.tView.modify_font(font)
    
        return self.tViewBuf

                
    def generate_output(self):
        """ Build our ASCII diagram for our textView tree
            Template Structure:
                <A-Z><N> - variable width number allocated in groups of two (0-1)
                vsd       - Dynamic variable space allocation identifier. Allocate specified space and dynamically
                            compensate for the space in the template taken for the {vsd} identifier. (eg. crude filler
                                                                                                          for dynamic columns)
                            The behaviour of this will depend upon the 
                            max_digit_length value and the placement of the {vs} between other variables. 
                            Each loop will store the size of the inserted digits and if {vs} is found appropriate
                            space will be allocated, if not its neglected completely (outside of updating the value).
                vss       - Allow a slot for space to be staticlly allocated, however do not compensate for the space taken by 
                            {vss} character string, simply exclude it.

                Variable Notes:
                    - space allocation will only be applied to <a-z>0 strings. > 0 is a fixed width by default

            Weight: '1234 Lbs.'
            Percen: '23.4%'

            a - rear left
            b - front left
            c - left
            d - rear
            e - cross weight
            f - front
            g - right
            h - rear right
            i - front right 

            
            Issues:
                - Template algorithm structure causes issues when a dyanmic varying space allocation slot 
                  is places on the left side of the template. It will through the entire template out of 
                  sync if said character space needs to be greater then the allocated space from the left 
                  side to the begining of the image.
        """

        # Accepted maximum number size in digits. (eg. Max number <= 9999 would be 4 digits)
        max_digit_length = 4

        # Vairable Map - An index that will map our values to the defined template variables
        var_map = {'a' : (self.weights['rear']['left']['weight'], self.weights['rear']['left']['perc']),
                   'b' : (self.weights['front']['left']['weight'], self.weights['front']['left']['perc']),
                   'c' : (self.weights['sides']['left']['weight'], self.weights['sides']['left']['perc']),
                   'd' : (self.weights['rear']['total']['weight'], self.weights['rear']['total']['perc']),
                   'e' : (self.weights['cross']['weight'], self.weights['cross']['perc']),
                   'f' : (self.weights['front']['total']['weight'], self.weights['front']['total']['perc']),
                   'g' : (self.weights['sides']['right']['weight'], self.weights['sides']['right']['perc']),
                   'h' : (self.weights['rear']['right']['weight'], self.weights['rear']['right']['perc']),
                   'i' : (self.weights['front']['right']['weight'], self.weights['front']['right']['perc'])
                }

        # Output Diagram Skeleton
        ###############################################################################
        #### !!!! NOTE: DO NOT CHANGE ANY OF THE SPACING IN THE BELOW TEMPLATE !!!!####
        ###############################################################################
        data_template = """
             {a0} Lbs.        {vsd}         {b0} Lbs.
              {a1}%                          {b1}%
            --------       (left)          --------
            |      |      {c0} Lbs. {vsd}  |      |
            |      |       {c1}%           |      |
            --------  ------------------   --------   -----
              -||----/       \          \_____||_____/     \ 
              |               \                             \ 
  (Rear)      |                \                             -|   (Front)
  {d0} Lbs.{vss}   |          {e0} Lbs. - {e1}%    {vsd}           |   {f0} Lbs.
   {d1}%      |                  \                           -|    {f1}%
              |                   \      _____  _____       /
              -||----\             \    /     ||     \     /             
            --------  ------------------   --------   -----
            |      |       {g0} Lbs.{vsd}  |      |
            |      |        {g1}%          |      |
            --------       (Right)         --------
             {h0} Lbs.     {vsd}            {i0} Lbs.
              {h1}%                          {i1}%"""

        
        output_diagram = ''
        # Control if we are processing a template character
        template_len = len(data_template)
        in_brackets = False
        char_pos = 0
        space_alloc = 0

        # Populate our values to our template
        #for char_pos in range(len(data_template)):
        while char_pos <= template_len:
            # An array temporarily containing the value characters of the template variable
            templ_var_vals = []
 
            if template_len <= char_pos:
                break
   
            # Watch for our begining variable opening bracket ({)
            if data_template[char_pos] == "{":
                in_brackets = True
                char_pos += 1


            if in_brackets:
                template_str = ""
                
                while True: # We will break internally
                    # aquire the data between {}
                    if data_template[char_pos] == "}":
                        in_brackets = False
                        
                        # collect our information into a single string
                        for i in range(len(templ_var_vals)):
                            template_str += str(templ_var_vals[i])
                        
                        break
                        
                    else:
                        # Test if our character is an integar or character and convert
                        try:
                            conv = int(data_template[char_pos])
                        except:
                            conv = data_template[char_pos]

                        templ_var_vals.append(conv)
                        char_pos += 1 
                        continue


                ### process our built identifying value ###
                output_data = ""

                # Deal with our variable space allocation identifier
                if template_str == "vsd" or template_str == "vss":
                    if template_str == "vsd":
                        vs_char_cnt = range(space_alloc + 5)            
                    elif template_str == "vss":
                        vs_char_cnt = range(space_alloc)

                    for i in vs_char_cnt:
                        output_data += ' '                        

                # Default to processing an identifying variable string (eg. A string of 2 character. [a-z][0-9])
                else:
                    try:
                        template_val = var_map[templ_var_vals[0]][templ_var_vals[1]]

                        # Store data size for space allocation only on {[a-z]0} variables
                        # FIXME: This situations allows for an error if len(template_val) > max_digit_len
                        if templ_var_vals[1] == 0: 
                            space_alloc = max_digit_length - len(str(template_val))

                        output_data = str(template_val)
        
                    except KeyError:
                        raise NameError("The template configuration contains variables that are not valid.")
        


                # Append our data
                output_diagram += output_data
                # Move to next character step
                char_pos += 1
            
            # we simply append the data
            else:
                output_diagram += data_template[char_pos]
                char_pos += 1

            
                
                
        # Place our template system in the textView 
        buffer = self.get_tView_buf()
        buffer.set_text(output_diagram) 




# A child GUI class to deal with our about box
class aboutDlg:
    def __init__(self):
        global glade_file
        self.aboutDlg = gtk.glade.XML(glade_file, "aboutDlg")
        self.aboutDlgInf = gtk.glade.XML(glade_file, "aboutDlg_information")

        self.dlgWdg = self.aboutDlg.get_widget("aboutDlg")
        self.dlgInfoWdg = self.aboutDlgInf.get_widget("aboutDlg_information")

        ## Our Signals ##
        # Signals attached to our about Dlg box
        signal_dict = {"on_aboutDlg_info_clicked" : self.show_dlg_info,
                        "on_aboutDlg_close_clicked" : self.hide_dlg}
        self.aboutDlg.signal_autoconnect(signal_dict)

        # Signals attached to our about Dlg information Dlg
        signal_dict = {"on_aboutDlg_additional_information_close_clicked" : self.hide_dlg_info}
        self.aboutDlgInf.signal_autoconnect(signal_dict)


    def show_dlg(self, null):
        self.dlgWdg.show()


    def hide_dlg(self, null):
        self.dlgWdg.hide()
                    

    def show_dlg_info(self, null):
        self.dlgInfoWdg.show()


    def hide_dlg_info(self, null):
        self.dlgInfoWdg.hide()                
        


if __name__ == '__main__':
    parent = parentGUI()
    gtk.main()
