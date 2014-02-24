'''
Formatters for Package PyTabular
--------------------------------
'''

def format_int(val):
    '''formats an integer

    Parameters
    ----------    
    val : scalar type
        value to formatted
    
    Returns
    -------
    val : str
        formatted value
    '''
    
    val = int(val)

    if type(val) not in [type(0), type(0L)]:
	
        raise TypeError("Parameter must be an integer.")
		
    if val < 0:
	
        return '-' + format_int(-val)
		
    result = ''
	
    while val >= 1000:
	
        val, r = divmod(val, 1000)
		
        result = ",%03d%s" % (r, result)
		
    return "%d%s" % (val, result)

def format_digits(digits=3):
    '''formatter creator for significant digits
    
    Parameters
    ----------
    digits : int
        number of significant digits
    
    Returns
    -------
    f : function
        function to formal a value to `digits` significant digits
    '''
    if not isinstance(digits, (int, long)):
        raise ValueError('received {} for digits, expected int'.format(type(digits)))
    
    def f(val):
        '''formats value to {} significant digits
        
        Parameters
        ----------
        val : scalar type
            value to format
        
        Returns
        -------
        val : str
            formatted value
        '''.format(digits)
        
        val = float(val)
        
        return '%0.{}f'.format(digits) % val
        
    return f
    
def format_stars(side='left', levels=[0.1,0.05,0.01], formatter=str):
    '''formatter creator for significance stars
    
    Parameters
    ----------
    levels : list
        list for which to apply significance stars
    side : str
        'left' to apply on leftside of value, 'right' to apply
        on right side
    
    Returns
    -------
    f : function
        function to star value
    '''
    levels=[0.1,0.05,0.01]

    if side not in ['left', 'right']:
        raise ValueError('expected left or right for side, recieved {}'.format(side))
    
    levels.sort(reverse=True)

    def f(val):
        '''formats val with significance stars
        
        Parameters
        ----------
        val : scalar type
            scalar type conformable to numeric
        
        Returns
        -------
        val : str
            formatted value
        '''
        
        val = float(val)
        
        stars=0        
        for i,level in enumerate(levels):
            if val <= level:
                stars = i + 1
            else:
                break
        
        if side == 'left':
            return '{}{}'.format('*'*stars, formatter(val))
        else:
            return '{}{}'.format(formatter(val), '*'*stars)
    
    return f