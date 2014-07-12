import re

class multiline_parser(object):
    """ 
    A simple style of parser where each value captured can be completely described by a single regex that may span multiple lines,
    but can still be neatly expressed with a regular expression. 
    
    The variable is still named 'line_captures' which is confusing. Sorry. 
    
    Multiple values are allowed. Only the first line that matches the regular expression is included.
    
    The data to be captured must be passed in in a structure that looks like the below. Return keys is always an array
    even if it contains just one element. 
    
    
    line_captures = [


        ...
        ]
        
        
        Parsing is not sped up or optimized in any way. Every regex that hasn't been found is checked in every line. 
        Best practice is to put them in the approximate order they are likely to appear.
        
        For more sensitive parsing, look at nested_line_parser.
        
    """
    
    line_captures = None
    
    def __init__(self, line_captures):
        self.line_captures = line_captures
    
    def get_keys(self, default_array=None):
        """ return just the keys -- suitable for constructing a header row. """
        capture_keys = []
        for line_capture in self.line_captures:
            capture_keys = capture_keys + line_capture['return_keys']
        
        # Deal with defaults--which could be existing keys or new ones.
        if default_array:
            for val in default_array:
                if val not in capture_keys:
                    capture_keys.append(val)
                    
        return capture_keys
    
    def process_file(self, filename, default_dict=None):
        # defaults dict can be default values for things that we're trying to capture--
        # or supplementary data that gets added to every row. 
        
        # reset values:
        for capture in self.line_captures:
            capture['found'] = False
            capture['results'] = None

        print "\nReading %s" % (filename)
        infile = open(filename, "r")
        wholefile =  infile.read()
        for capture_attempt in self.line_captures:
            if not capture_attempt['found']:
                result = re.search(capture_attempt['regex'], wholefile)
                if result:
                    capture_attempt['found'] = True

                    results = []
                    for i in range(1,capture_attempt['num_values']+1):
                        results.append(result.group(i))
                    capture_attempt['results'] = results

        
        return_dict = {}
        if default_dict:
            return_dict = default_dict
            
        for capture in self.line_captures:
            if capture['debug']:
                if capture['found']:
                    print "Got %s : '%s'" % (capture['name'], capture['results'])
                else:
                    print "**Missing %s" % (capture['name'])
            if capture['found']:
                for i in range(0,capture['num_values']):
                    return_key = capture['return_keys'][i]
                    return_value = capture['results'][i]
                    return_dict[return_key] = return_value
        
                
        return return_dict
