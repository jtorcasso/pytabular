'''
Tabular Classes for PyTabular Package
-------------------------------------

Superclasses:

- TabularBase
- Tabular2D
- Tabular1D

Classes for User:

- TabularCell
- Tabular
- Table
- LongTable

Issues:

-   Should use regular expressions to handle LateX special characters when
    initializing TabularCell instances

'''

from __future__ import print_function, division

__docformat__ = 'restructeredtext'

__version__ = '0.1.3'

# Standard Library
import warnings

# Third Party
import numpy as np

# Local packages
from formatting import *
from operators import *

def version():
    print(__version__)

def hstack(*args):
    '''stacks tabular objects horizontally
    
    Parameters
    ----------
    args : tuple
        tabular objects, t1, t2, ...
    
    Returns
    -------
    tab : tabular instance
        a new table
    '''
    tables = []
    for tab in args:
        if isinstance(tab, TabularRow):
            content = tab.content.reshape((1,-1))
        elif isinstance(tab, TabularColumn):
            content = tab.content.reshape((-1,1))
        elif isinstance(tab, (Tabular, Table, LongTable, Tabular2D)):
            content = tab.content
        elif isinstance(tab, Tabular1D):
            if tab.orientation == 0:
                content = tab.content.reshape((1,-1))
            else:
                content = tab.content.reshape((-1,1))
        else:
            raise ValueError('expected tabular instance')
        
        shape = content.shape
        cells = np.array([c.content for c in content.flatten()])
        tables.append(cells.reshape(shape))
        
    
    return Tabular(np.hstack(tables))

def vstack(*args):
    '''stacks tabular objects vertically
    
    Parameters
    ----------
    args : tuple
        tabular objects, t1, t2, ...
    
    Returns
    -------
    tab : tabular instance
        a new table
    '''
    tables = []
    for tab in args:
        if isinstance(tab, TabularRow):
            content = tab.content.reshape((1,-1))
        elif isinstance(tab, TabularColumn):
            content = tab.content.reshape((-1,1))
        elif isinstance(tab, (Tabular, Table, LongTable, Tabular2D)):
            content = tab.content
        elif isinstance(tab, Tabular1D):
            if tab.orientation == 0:
                content = tab.content.reshape((1,-1))
            else:
                content = tab.content.reshape((-1,1))
        else:
            raise ValueError('expected tabular instance')
        
        shape = content.shape
        cells = np.array([c.content for c in content.flatten()])
        tables.append(cells.reshape(shape))
    
    return Tabular(np.vstack(tables))

class TabularBase(object):
    '''base tabular object

    Parameters
    ----------
    content : scalar type
        str, int, float, long

    '''

    def __init__(self, content):
         self.original_content = content
         self.content = self._handle_content(content)


    def _handle_content(self, content):
         '''handles contents

         Parameters
         ----------
         content : scalar type
             content of tabular element

         Notes
         -----
         Must write for inherited classes
         '''
         
         raise NotImplementedError

    def set_attr(self, **kwargs):
         '''sets attributes

         kwargs : keyword arguments
             attributes to set
         '''

         for attr in kwargs:
             setattr(self, attr, kwargs[attr])

    def get_attr(self, attr='all'):
         '''returns attribute(s) of the table element

         Parameters
         ----------
         attr : str
             attribute of the table element
         '''
         if attr == 'all':
             return {a:getattr(self,a) for a in dir(self) if hasattr(self,a)}
         return getattr(self, attr)

    def set_content(self, content):
         '''sets content of tabular element

         Parameters
         ----------
         content : scalar type
             content to replace with
         '''
         self.content = self._handle_content(content)

    def as_tex(self):
        '''render the tabular element as text

        Notes
        -----
        Must implement in subclass
        '''

        raise NotImplementedError
    
    def __str__(self):
        return self.as_tex()

class TabularCell(TabularBase):
    '''cell of a table

    ** Attributes **
    shape : ()
        empty tuple
    ndim : int
        0
    rows : int
        number of rows represented by cell (think multirow)
    columns : int
        number columns represented by cell (think multicolumn)
    rotation : int or None
        None if not rotated, int between 0 and 90 degrees
    underline : bool
        True to underline, false otherwise
    bold : bool
        True to bold, false otherwise
    emph : bool
        True to emphasize (italics), false otherwise
    alignment : None
        None to retain alignment of outer environment, else specify 
        a string (e.g. 'c', 'l' or 'r')
    formatter : function
        Default is str, specify a function
        which takes a scalar type and outputs a string
    fontsize : int or None
        None to retain fontsize of outer environment, else specify 
        a string (e.g. 'small', 'tiny')
    phantom : bool
        If True, the tabular element will not produce any string
    hline : bool
        If True, places horizontal line below cell
    loc : tuple
        (row, col) coordinates in table
    '''

    def __init__(self, content, loc):
        self.loc = loc
        TabularBase.__init__(self, content)
        self.shape = ()
        self.ndim = 0
        self.rows = 1
        self.columns = 1
        self.rotation = None
        self.underline = False
        self.bold = False
        self.emph = False
        self.alignment = None
        self.formatter = str
        self.fontsize = None
        self.mergedrow = False
        self.mergedcol = False
        self.lines = None
        self.narrow = None
        self.space_above = None
        self.space_below = None
        self.color = None
        
    def _handle_content(self, content):
        '''handles content

        Parameters
        ----------
        content : scalar type
            content of cell

        '''
        accepted = (str, long, float, int, basestring, np.generic)
        if not isinstance(content, accepted):
            msg = 'content must be scalar type, received {}'.format(type(content))
            raise ValueError(msg)
        
        if isinstance(content, unicode):
            content = str(content)
        special_chars = ['&', '%', '#', '_', '{', '}', '$', '\\', '~', '^']
        
        if isinstance(content, str):
            content = content.strip()
            
            for char in special_chars:
                if char in content:
                    msg = 'Special character "{}" found in cell {},'.format(char, self.loc)
                    msg += '\nspecial characters may cause LateX errors, use remove_character() to remove'
                    warnings.warn(msg, UserWarning)
            
        self.isnull = content == ''        
            
        return content
    
    def remove_character(self, char=None):
        '''remove characters form a cell
        
        Parameters
        ----------
        char : str, list of strings
            characters to remove from cell, if None, uses list of 
            special characters
        '''
        if isinstance(self.content, str):
            
            if char is None:
                special_chars = ['&', '%', '#', '_', '{', '}', '$', '\\', '~', '^']
            else:
                special_chars = list(char)
                
            content = self.content
            for char in special_chars:
                content = content.replace(char, '')
            
            self.set_content(content)

    def set_rotation(self, angle):
         '''sets rotation

         Parameters
         ----------
         angle : int
             0 to 360
         '''

         if (angle >= 0) & (angle <= 360):
             self.rotation = angle
         else:
             raise ValueError('received {}, angle must be between 0 and 360'.format(angle))

    def set_underline(self, underline=True):
         '''set to underline

         Parameters
         ----------
         underline : bool
             True to underline
         '''
         
         if not underline in [True, False]:
             raise ValueError('received {}, expected boolean'.format(type(underline)))
         self.underline = underline

    def set_bold(self, bold=True):
         '''set to bold

         Parameters
         ----------
         bold : bool
             True to bold
         '''
         if not bold in [True, False]:
             raise ValueError('received {}, expected boolean'.format(type(bold)))
         self.bold = bold

    def set_emph(self, emph=True):
        '''set to emph

        Parameters
        ----------
        emph : bool
            True to emph
        '''
        if not emph in [True, False]:
            raise ValueError('received {}, expected boolean'.format(type(emph)))
        self.emph = emph

    def set_alignment(self, alignment):
        '''sets alignment of tabular element

        Parameters
        ----------
        alignment : str
            alignment string in LateX
            ex: 'c', 'l', or 'r'
        '''
        if not isinstance(alignment, str):
            raise ValueError('received {}, expected str'.format(type(alignment)))

        self.alignment = alignment

    def set_formatter(self, formatter):
        '''sets function to format content

        Parameters
        ----------
        formatter : function
            function to format the content, must return a string
        '''
        if not hasattr(formatter, '__call__'):
            raise ValueError('received {}, expected callable'.format(type(formatter)))

        self.formatter = formatter

    def set_fontsize(self, fontsize):
        '''sets fontsize

        Parameters
        ----------
        fontsize : str
            font size for tabular element
        '''

        sizes = ['tiny', 'scriptsize', 'footnotesize', 'small', 
        'normalsize', 'large', 'Large', 'LARGE', 'huge', 'Huge']

        if (fontsize not in sizes) and (fontsize is not None):
            raise ValueError('{} not a valid fontsize'.format(fontsize))

        self.fontsize = fontsize
    
    def set_digits(self, digits=3):
        '''gives value 'digits' signficant digits
        
        Parameters
        ----------
        digits : int
            number of significant digits
        '''
        self.set_formatter(format_digits(digits))
    
    def set_stars(self, side='left', levels=[0.1, 0.05, 0.01]):
        '''sets cell to display significance stars
        
        Parameters
        ----------
        side : str
            'left' to apply on leftside of value, 'right' to apply
            on right side
        levels : list
            list for which to apply significance stars
        '''
        
        self.set_formatter(format_stars(side, levels, self.formatter))

    def set_mergedrow(self, mergedrow=True):
        '''means cell is merged into another row

        Parameters
        ----------
        mergedrow : bool
            True to hide element
        '''

        if not mergedrow in [True, False]:
            raise ValueError('received {}, expected boolean'.format(type(mergedrow)))

        self.mergedrow = mergedrow
    
    def set_mergedcol(self, mergedcol=True):
        '''means cell is merged into another col

        Parameters
        ----------
        mergedcol : bool
            True to hide element
        '''

        if not mergedcol in [True, False]:
            raise ValueError('received {}, expected boolean'.format(type(mergedcol)))

        self.mergedcol = mergedcol
    
    def set_space_below(self, space):
        '''set the spacing after the cell in row
        
        Parameters
        ----------
        space : str, int, float
            spacing to place after row (ex. '1cm')
            
        Notes
        -----
        if numeric type give for `space`, assumes unit is 'cm'
        '''
        
        if isinstance(space, (int, float)):
            space = '{}cm'.format(space)
        elif not isinstance(space, str):
            raise ValueError('space must be str, int or float')
        
        self.space_below = space

    def set_space_above(self, space):
        '''set the spacing before the cell in row
        
        Parameters
        ----------
        space : str, int, float
            spacing to place after row (ex. '1cm')
            
        Notes
        -----
        if numeric type give for `space`, assumes unit is 'cm'
        '''
        
        if isinstance(space, (int, float)):
            space = '{}cm'.format(space)
        elif not isinstance(space, str):
            raise ValueError('space must be str, int or float')
        
        self.space_above = space
    
    def set_color(self, color, opacity=50):
        '''sets color of a cell
        
        Parameters
        ----------
        color : str
            name of a color, some examples include: 
            white, black, red, green, blue, cyan, magenta, yellow, gray
        opacity : int
            int in [0,100]
        '''
        
        default = ['white', 'black', 'red', 'green', 
                   'blue', 'cyan', 'magenta', 'yellow', 'gray']        
        
        if not isinstance(color, str):
            raise ValueError('received {} for color, expected str'.format(type(color)))
        if color not in default:
            warnings.warn('color not in default, check name')
        if not isinstance(opacity, int):
            raise ValueError('received {} for opacity, expect int'.format(type(opacity)))
        if (opacity > 100) | (opacity < 0):
            raise ValueError('opacity should be between 0 and 100')
        
        self.color = '{}!{}'.format(color, opacity)

    def _set_rows(self, rows):
        '''sets number of rows for multirow

        Parameters
        ----------
        rows : int
            number of rows
        '''
        self.rows = rows

    def _set_columns(self, columns):
        '''sets number of columns for multicolumn

        Parameters
        ----------
        columns : int
            number of columns
        '''
        self.columns = columns
    
    def set_lines(self, lines=1, narrow=None):
        '''adds lines around cell
        
        Parameters
        ----------
        lines : int
            number of horizontal lines below cell
            if None, assures no line is printed
        narrow : str
            'r', 'l', 'lr', or 'rl'
        '''
        if (lines is not None) & (not isinstance(lines, int)):
            raise ValueError('received {}, expected int'.format(type(lines)))
        if narrow not in [None, 'r', 'l', 'lr', 'rl']:
            raise ValueError('narrow incorrectly specified')
        
        self.lines = lines
        self.narrow = narrow
        
    def as_tex(self):
        '''render the tabular element as text

        Returns
        -------
        val : str
            string which LateX will recognize in tabular environment
        '''
        columns = self.columns
        rows = self.rows
        
        align = 'c' if self.alignment is None else self.alignment
        color = self.color
        fontsize = self.fontsize        
        
        if self.isnull:
            val = ''
            if color is not None:
                val = '\\cellcolor{{{}}}{{}}'.format(color)
            if (columns > 1) | ('|' in align):
                return '\\mc{{{}}}{{{}}}{{{}}}'.format(columns, align, val)
            return val

        val = self.formatter(self.content)

        if color is not None:
            val = '\\cellcolor{{{}}}{{{}}}'.format(color, val)
        
        if fontsize is not None:
            val = '\\{}{{{}}}'.format(fontsize, val)
        
        environments = {'\\textbf{':self.bold, '\\emph{':self.emph, 
                '\\uline{':self.underline}

        for env in environments:
            if environments[env]:
                val = env + val + '}'

        if self.rotation is not None:
            val = '\\rotatebox{{{}}}{{{}}}'.format(self.rotation, val)
            
        if rows > 1:
            val = '\\mr{{{}}}{{*}}{{{}}}'.format(rows, val)        
        if (self.alignment is not None) | (columns > 1):
            val = '\\mc{{{}}}{{{}}}{{{}}}'.format(columns, align, val)
            

        return val

class Tabular2D(TabularBase):
    '''2-dimensional tabular

    Notes
    -----
    To be used as a superclass for TabularRow and TabularColumn
    Also can be directly accessed by slicing a Table

    Must write over any methods in TabularBase which should 
    operate on a per cell basis

    '''

    def __init__(self, content, rowfragment=True, colfragment=True):
        TabularBase.__init__(self, content)
        self.rowfragment = rowfragment
        self.colfragment = colfragment

    def _handle_content(self, content):
        '''handles content

        Parameters
        ----------
        content : 2-d like
            np.ndarray, list of lists, contain data
            for a table

        '''
        
        try:
            content = np.array(content, dtype=object)
        except ValueError:
            print('Cannot cast content as array')

        if content.ndim == 1:
            content = content.reshape((1,-1))

        if content.ndim != 2:
            raise ValueError('Content must be conformable to 2-d array')
        
        if not isinstance(content[0,0], TabularCell):
            
            for i in range(content.shape[0]):
                  for j in range(content.shape[1]):
                      content[i,j] = TabularCell(content[i,j], (i,j))

        self.shape = content.shape
        return content
    
    def remove_character(self, char=None):
        '''removes characters from cell

        Parameters
        ----------
        char : str, list of strings
            characters to remove from cell, if None, uses list of 
            special characters
        '''
        cells = self.content.flatten()
        for cell in cells:
            cell.remove_character(char)   
        
        
    def set_rotation(self, angle):
         '''sets rotation

         Parameters
         ----------
         angle : int
             0 to 90
         '''
         cells = self.content.flatten()
         for cell in cells:
             cell.set_rotation(angle)


    def set_underline(self, underline=True):
         '''set to underline

         Parameters
         ----------
         underline : bool
             True to underline
         '''
         cells = self.content.flatten()
         for cell in cells:
             cell.set_underline(underline)

    def set_bold(self, bold=True):
         '''set to bold

         Parameters
         ----------
         bold : bool
             True to bold
         '''
         cells = self.content.flatten()
         for cell in cells:
             cell.set_bold(bold)

    def set_emph(self, emph=True):
        '''set to emph

        Parameters
        ----------
        emph : bool
            True to emph
        '''
        cells = self.content.flatten()
        for cell in cells:
            cell.set_emph(emph)

    def set_alignment(self, alignment):
        '''sets alignment of tabular element

        Parameters
        ----------
        alignment : str
            alignment string in LateX
            ex: 'c', 'l', or 'r'
        '''
        cells = self.content.flatten()
        for cell in cells:
            cell.set_alignment(alignment)

    def set_formatter(self, formatter):
        '''sets function to format content

        Parameters
        ----------
        formatter : function
            function to format the content, must return a string
        '''
        cells = self.content.flatten()
        for cell in cells:
            cell.set_formatter(formatter)

    def set_fontsize(self, fontsize):
        '''sets fontsize

        Parameters
        ----------
        fontsize : str
            font size for tabular element
        '''

        cells = self.content.flatten()
        for cell in cells:
            cell.set_fontsize(fontsize)

    def set_mergedrow(self, mergedrow=True):
        '''sets cells to mergedrow

        Parameters
        ----------
        mergedrow : bool
            True to hide element
        '''

        cells = self.content.flatten()
        for cell in cells:
            cell.set_mergedrow(mergedrow)

    def set_mergedcol(self, mergedcol=True):
        '''sets cells to mergedcol

        Parameters
        ----------
        mergedcol : bool
            True to hide element
        '''

        cells = self.content.flatten()
        for cell in cells:
            cell.set_mergedcol(mergedcol)

    def set_lines(self, lines=1, narrow=None):
        '''adds a horizontal line below the cell
        
        Parameters
        ----------
        lines : int
            number of horizontal lines below cell
        narrow : str
            'r', 'l', or 'lr'
        '''
        
        cells = self.content.flatten()
        for cell in cells:
            cell.set_lines(lines, narrow)
        
    def set_digits(self, digits=3):
        '''gives value 'digits' signficant digits
        
        Parameters
        ----------
        digits : int
            number of significant digits
        '''
        cells = self.content.flatten()
        for cell in cells:
            cell.set_digits(digits)
    
    def set_stars(self, side='left', levels=[0.1,0.05,0.01]):
        '''sets cell to display significance stars
        
        Parameters
        ----------
        side : str
            'left' to apply on leftside of value, 'right' to apply
            on right side
        levels : list
            list for which to apply significance stars

        '''
        cells = self.content.flatten()
        for cell in cells:
            cell.set_stars(side, levels)

    def set_space_above(self, space):
        '''set the spacing before a cell in a row
        
        Parameters
        ----------
        space : str, int, float
            spacing to place after row (ex. '1cm')
            
        Notes
        -----
        if numeric type give for `space`, assumes unit is 'cm'
        '''
        
        cells = self.content.flatten()
        for cell in cells:
            cell.set_space_above(space)

    def set_space_below(self, space):
        '''set the spacing after a cell in a row
        
        Parameters
        ----------
        space : str, int, float
            spacing to place after row (ex. '1cm')
            
        Notes
        -----
        if numeric type give for `space`, assumes unit is 'cm'
        '''
        
        cells = self.content.flatten()
        for cell in cells:
            cell.set_space_below(space)

    def set_color(self, color, opacity=50):
        '''sets color of cells
        
        Parameters
        ----------
        color : str
            name of a color, some examples include: 
            white, black, red, green, blue, cyan, magenta, yellow, gray
        opacity : int
            int in [0,100]
        '''
        
        cells = self.content.flatten()
        for cell in cells:
            cell.set_color(color, opacity)

    def merge(self, force=False):
        '''merges the Tabular2D
        
        Parameters
        ----------
        force : bool
            if True, forces merge over non-null cells, purges these cells
        '''
        
        if self.content[0,0].mergedrow | self.content[0,0].mergedcol:
            raise MergeError('attempting merge cells that are already merged')
            
        rows = self.content.shape[0]
        cols = self.content.shape[1]
        self.content[0,0]._set_rows(rows)
        self.content[0,0]._set_columns(cols)
        
        if force:
            for c in self.flatten()[1:]:
                c.set_content('')
        if not np.all([c.isnull for c in self.flatten()[1:]]):
            raise MergeError('cannot multirow merge on nonnull cells')
        for i,cell in enumerate(self.flatten()):
            if i == 0:
                continue
            if i < self.content.shape[1]:
                cell.set_mergedrow()
                cell._set_rows(rows)
            elif i%self.content.shape[1] == 0:
                cell.set_mergedcol()
                cell._set_columns(cols)
            else:
                cell.set_mergedcol()
                cell.set_mergedrow()

    def __getitem__(self, val):
        '''slices from Tabular2D

        Parameters
        ----------
        val : tuple
            may be single ints/slices or a tuple
            of two of them or lists
        '''

        newcontent = self.content[val]
        if newcontent.shape == ():
            return newcontent
        elif newcontent.shape == self.content.shape:
            return self
        elif newcontent.ndim == 2:
            tab = Tabular2D(newcontent)
            if not self.rowfragment:
                tab.colfragment = newcontent.shape[0] < self.content.shape[0]
            if not self.colfragment:
                tab.rowfragment = newcontent.shape[1] < self.content.shape[1]
            return tab
        else:
            if isinstance(val, int) & (not self.rowfragment):
                return TabularRow(newcontent)
            elif isinstance(val, int):
                return Tabular1D(newcontent, 0)
            elif isinstance(val, tuple):
                if len(val)==1:
                    if (len(newcontent) < self.content.shape[1]) | (self.rowfragment):
                        return Tabular1D(newcontent, 0)
                    return TabularRow(newcontent)
                elif isinstance(val[0], int):
                    if (len(newcontent) < self.content.shape[1]) | (self.rowfragment):
                        return Tabular1D(newcontent, 0)
                    return TabularRow(newcontent)
                elif isinstance(val[1], int):
                    if (len(newcontent) < self.content.shape[0]) | (self.colfragment):
                        return Tabular1D(newcontent, 1)
                    return TabularColumn(newcontent)
        raise ValueError('invalid slice: {}'.format(val))

    def __setitem__(self, key, value):
        self.content[key] = value

    def __len__(self):
        return len(self.content)
    
    def flatten(self):
        '''returns 1-d tabular of content
        '''
        
        return Tabular1D(self.content.flatten())
        

class Tabular1D(Tabular2D):
    '''1-dimensional tabular
    
    Parameters
    ----------
    orientation : int
        0 if horizontal, 1 if vertical
    '''
    def __init__(self, content, orientation=0):
        Tabular2D.__init__(self, content)
        self.orientation = orientation
        self.rowfragment = True
        self.colfragment = True

    def _handle_content(self, content):
        '''handles content

        Parameters
        ----------
        content : np.ndarray
            dtype = object, filled with TabularCell instances
        '''

        if content.ndim != 1:
            raise ValueError('content must be 1-dimensional')
        self.ndim = content.ndim
        self.shape = content.shape
        return content

    def merge(self, force=False):
        '''merges the 1-d tabular
        
        Parameters
        ----------
        force : bool
            if True, forces merge over non-null cells, purges these cells
        '''

        if self.content[0].mergedrow | self.content[0].mergedcol:
            raise MergeError('attempting merge cells that are already merged')        
        
        if force:
            for c in self[1:]:
                c.set_content('')
        
        if self.orientation == 0:
            if not np.all([c.isnull for c in self[1:]]):
                raise MergeError('cannot multirow merge on nonnull cells')
            self.content[0]._set_columns(len(self.content))
            self[1:].set_mergedrow()
        else:
            if not np.all([c.isnull for c in self[1:]]):
                raise MergeError('cannot multirow merge on nonnull cells')
            self.content[0]._set_rows(len(self.content))
            self[1:].set_mergedcol()


    def __getitem__(self, val):
        '''slices from Tabular1D

        Parameters
        ----------
        val : tuple
            may be single ints/slices or a tuple
            of two of them or lists
        '''

        newcontent = self.content[val]
        if newcontent.shape == ():
            return newcontent
        if newcontent.shape == self.content.shape:
            return self
        else:
            return Tabular1D(newcontent)

class TabularRow(Tabular1D):
    '''tabular for a row

    '''
    def __init__(self, content):
        Tabular1D.__init__(self, content)
        self.orientation = 0
        self.rowfragment = False
        self.suppress = {'fonts':False}

    def merge(self, force=False):
        '''merges the row
        
        Parameters
        ----------
        force : bool
            if True, forces merge over non-null cells, purges these cells
        '''

        if self.content[0].mergedrow | self.content[0].mergedcol:
            raise MergeError('attempting merge cells that are already merged')
        if force:
            for c in self[1:]:
                c.set_content('')
        if not np.all([c.isnull for c in self[1:]]):
            raise MergeError('cannot multicolumn merge on nonnull cells')
        self.content[0]._set_columns(len(self.content))
        self[1:].set_mergedrow()
        
    def _handle_rowspace(self):
        '''handles horizontal spacing between rows
        '''
        
        space_below = list(set([c.space_below for c in self]))
        space_above = list(set([c.space_above for c in self]))
        
        return space_above[0], space_below[0]
            
    
    def _handle_lines(self, indent=2):
        '''handles lines around cells
        
        Parameters
        ----------
        indent : int
            length of indent        
        
        '''
        cells = [c for c in self if not c.mergedrow]
        narrow = np.any([c.narrow is not None for c in cells])
        lines = [c.lines for c in cells]
        if (not narrow) & (len(list(set(lines))) == 1):
            if lines[0] is None:
                return ''
            
            return '\n' + ' '*indent + '\\hline '*lines[0]
        
        tex = []
        for c in cells:
            loc = c.loc[1]
            cols = c.columns
            sides = '({})'.format(c.narrow if c.narrow is not None else '')
            hlines = 0 if c.lines is None else c.lines
            
            linetex = []
            for i in xrange(hlines):
                linetex.append('\\cmidrule{}{{{}-{}}}'.format(sides,loc+1,loc+cols))
            
            if len(linetex) > 0:
                tex.append('\\morecmidrules'.join(linetex))
        
        if len(tex) == 0:
            return ''
        return '\n' + indent*' ' + ' '.join(tex)
        
    def as_tex(self, indent=2):
        '''creates tex string for the row
        '''

        
        underlining_tex = self._handle_lines(indent)
        
        row = [cell.as_tex() for cell in self.content if not cell.mergedrow]
        
        row = ' '*indent + ' & '.join(row)
        
        space_above, space_below = self._handle_rowspace()        
        if space_above is not None:
            space_above = '[{}]'.format(space_above)
            row = '{}\\\\{}\n{}'.format(' '*indent, space_above, row)
        space_below = '' if space_below is None else '[{}]'.format(space_below)
        row += ' \\\\{} {} \n'.format(space_below, underlining_tex)
                
        return row
   
class TabularColumn(Tabular1D):
    '''tabular for a row

    '''
    def __init__(self, content):
        Tabular1D.__init__(self, content)
        self.orientation = 1
        self.colfragment = False

    def merge(self, force=False):
        '''merges the row
        
        Parameters
        ----------
        force : bool
            if True, forces merge over non-null cells, purges these cells
        '''

        if self.content[0].mergedrow | self.content[0].mergedcol:
            raise MergeError('attempting merge cells that are already merged')
        if force:
            for c in self[1:]:
                c.set_content('')
        if not np.all([c.isnull for c in self[1:]]):
            raise MergeError('cannot multirow merge on nonnull cells')
        self.content[0]._set_rows(len(self.content))
        self[1:].set_mergedcol()
        

class Tabular(Tabular2D):
    '''end-user class for LateX tabular environment
    '''
    
    def __init__(self, content):
        Tabular2D.__init__(self, content)
        self.rowfragment = False
        self.colfragment = False
        self.tab_alignment = 'c'*self.content.shape[1]
        self.indent = 2
        self.depth = 1
        self.environments = []
        self.tab_type = 'tabu'
        self.notes = []
        self.notesize = 'scriptsize'

    
    def set_indent(self, indent):
        '''sets indentation for presentation of output
        
        Parameters
        ----------
        indent : str
            number of spaces to insert at indentation level
        '''
        if not isinstance(indent, int):
            raise ValueError('received {} for indent instead of int'.format(type(indent)))
        
        self.indent = indent
    
    def add_environment(self, env, post='', prepend=False):
        '''adds an environment around tabular
        
        Parameters
        ----------
        env : str
            name of latex environment, e.g. 'center'
        post : str
            text to add after the initializion of environment
        '''
        
        self.depth += 1
        
        if prepend:
            self.environments.insert(0,(env,post))
        else:
            self.environments.append((env,post))

    def _handle_environments(self, val):
        '''handles environments

        Parameters
        ----------
        val : str
            value to wrap in environment
        '''
        
        if len(self.environments) == 0:
            return val
        
        for i,info in enumerate(self.environments):
            env, post = info
            space = ' '*(self.depth - 2 -i)*self.indent
            val = '{}\\begin{{{}}}{}\n\n{}\n\n{}\\end{{{}}}'.format(space, \
                    env, post, val, space,  env)
        
        return val
        
    def _build_rows(self):
        '''builds the tex string of the rows
        '''
        
        rows = [self[i,:].as_tex(self.depth*self.indent) for i in xrange(len(self.content))]
        
        return '\n'.join(rows)
    
    def set_tab_alignment(self, tabular):
        '''sets default alignment of tabular
        
        Parameters
        ----------
        tabular : str
            must have alignment character for each column in table
            ex. 'cc', 'p{3cm}ll'
        '''
        
        self.tab_alignment = tabular
        
    def _set_header(self):
        '''sets look of the header
        '''
        space = ' '*(self.depth-1)*self.indent
        tab = '{}\\begin{{{}}}\n'.format(space, 'ThreePartTable')
        tab += '{}\\begin{{{}}}{{{}}}'.format(space, \
                                    self.tab_type, self.tab_alignment)

        return tab + '\n\n'
        
    def _set_footer(self):
        '''sets look of the footer
        '''
        space = ' '*(self.depth-1)*self.indent
        end = '\n{}\\end{{{}}}'.format(space, self.tab_type)
        
        spc = ' '*(self.depth)*self.indent
        
        if len(self.notes) > 0:
            notes = []
            for note in self.notes:
                notes.append('{}\\item {}'.format(spc, note))
            notes = '\n'.join(notes)
            end = '{}\n{}\\begin{{tablenotes}}\n{}\\{}\n{}\n{}\\end{{tablenotes}}'.format(\
            end, spc, spc, self.notesize, notes, spc)
            
        end += '\n{}\\end{{{}}}'.format(space, 'ThreePartTable')
        
        return end
    
    def _set_tab_type(self, type_):
        '''sets tabular type
        
        Parameters
        ----------
        type_ : str
            tabular type (e.g. 'tabu', 'tabular', 'longtabu')
        '''
        if type_ not in ['tabu', 'tabular', 'longtabu']:
            raise ValueError('{} not a valid tabular type'.format(type_))
        self.tab_type = type_
    
    def as_tex(self):
        '''creates tex string for the row
        '''
            
        
        header = self._set_header()
        footer = self._set_footer()
        rows = self._build_rows()
        
        tabular = header + rows + footer
        
        string = self._handle_environments(tabular)
        
        return string
    
    def add_note(self, notes, fontsize='scriptsize'):
        '''sets the footnotes for the table
        
        Parameters
        ----------
        notes : str
            notes to put in table
        fontsize : str
            LateX fontsize, e.g. 'tiny', 'large'
        '''
        
        sizes = ['tiny', 'scriptsize', 'footnotesize', 'small', 
        'normalsize', 'large', 'Large', 'LARGE', 'huge', 'Huge']

        if (fontsize not in sizes):
            raise ValueError('{} not a valid fontsize'.format(fontsize))
            
        self.notes.append(notes)
        self.notesize = fontsize
        
    
    def write(self, filename):
        '''write table to file
        
        Parameters
        ----------
        filename : str
            name of file
        '''
        if not isinstance(filename, str):
            raise ValueError('filename must be a str')
        
        if filename[-4:] != '.tex':
            filename = filename + '.tex'
        
        texfile = open(filename, 'wb')
        texfile.write(self.as_tex())
        texfile.close()
        
class Table(Tabular):
    '''class for LateX tables
    '''
    
    def __init__(self, content):
        Tabular.__init__(self, content)
        self.caption = 'Table 1'
        self.label = 'table1'
        self.loc = 'c'
    
    def set_location(self, loc='c'):
        '''horizontal location (justification) of table
        
        Parameters
        ----------
        loc : str
            'c' for center, 'l' for left and 'r' for right
        '''
        if loc not in ['c', 'l', 'r']:
            raise ValueError('must specify c, l, or r; received {}'.format(loc))
        self.loc = loc
    
    def set_caption(self, caption):
        '''sets caption for the table
        
        Parameters
        ----------
        caption : str
            caption of the table
        '''
        self.caption = caption
        
    def set_label(self, label):
        '''sets label for the table
        
        Parameters
        ----------
        label : str
            label for the table
        '''
        self.label = label

    def as_tex(self):
        '''creates tex string for the row
        '''
        
        for env in self.environments:
            if 'table' == env[0]:
                self.environments.remove(env)
                self.depth -= 1
            
        # Justification
        if self.loc == 'c':
            just = 'centering'
        elif self.loc == 'r':
            just = 'raggedleft'
        elif self.loc == 'l':
            just = 'raggedright'
        
        post = '{}\\{}'.format(' '*(self.depth - 1)*self.indent, just)
        label = ' \\label{{{}}}'.format(self.label)
        post += '\n{}\\captionsetup{{singlelinecheck=false,justification={}}}'.format(\
                ' '*(self.depth - 1)*self.indent, just)
        post += '\n{}\\caption{{{}}}'.format(\
        ' '*(self.depth - 1)*self.indent, \
                    self.caption + label)
        
         
        self.add_environment('table', post, prepend=True)
       
        header = self._set_header()
        footer = self._set_footer()
        rows = self._build_rows()
        
        tabular = header + rows + footer
        
        string = self._handle_environments(tabular)

        return string

class LongTable(Tabular):
    '''class for LateX longtables
    '''
    
    def __init__(self, content):
        Tabular.__init__(self, content)
        self._set_tab_type('longtabu')
        self.repeats = 1
        self.caption = 'Table 1'
        self.label = 'table1'
        self.loc = 'c'
    
    def set_location(self, loc='c'):
        '''horizontal location (justification) of table
        
        Parameters
        ----------
        loc : str
            'c' for center, 'l' for left and 'r' for right
        '''
        if loc not in ['c', 'l', 'r']:
            raise ValueError('must specify c, l, or r; received {}'.format(loc))
        self.loc = loc
        
    def set_caption(self, caption):
        '''sets caption for the table
        
        Parameters
        ----------
        caption : str
            caption of the table
        '''
        self.caption = caption
        
    def set_label(self, label):
        '''sets label for the table
        
        Parameters
        ----------
        label : str
            label for the table
        '''
        self.label = label
    
    def set_repeats(self, repeats):
        '''sets number of rows to repeat
        
        Parameters
        ----------
        repeats : int
            number of rows to repeat on each page
        '''
        self.repeats = repeats

    def _build_rows(self):
        '''builds the tex string of the rows
        '''
        space = ' '*(self.depth)*self.indent
        rows = [self[i,:].as_tex(self.depth*self.indent) for i in xrange(len(self.content))]

        # Justification
        if self.loc == 'c':
            just = 'centering'
        elif self.loc == 'r':
            just = 'raggedleft'
        elif self.loc == 'l':
            just = 'raggedright'
        
        caption = '{}\\{} \\\\'.format(space, just)
        caption += '\n{}\\captionsetup{{singlelinecheck=false,justification={}}}'.format(\
                space, just)
                
        label = ' \\label{{{}}}'.format(self.label)
        caption += '\n{}\\caption{{{}}} \\\\\n'.format(space, self.caption + label)
                    
        firsthead = caption
        headrows = rows[:self.repeats]
        firsthead += '\n'.join(headrows) + '\n{}\\endfirsthead\n\n'.format(space)
        head = '{}\\mc{{{}}}{{c}}{{{}}} \\\\\n'.format(space, self.shape[1], \
            '\\tablename\\ \\thetable\\ -- \\emph{Continued from previous page}')
        head += '\n'.join(headrows) + '\n{}\\endhead\n\n'.format(space)
        foot = '{}\\mc{{{}}}{{r}}{{{}}} \\\\\n'.format(space, self.shape[1], \
            '\\emph{Continued on next page}')
        foot += '\n{}\\endfoot\n{}\\endlastfoot\n\n'.format(space, space)
        
        return firsthead + head + foot + '\n'.join(rows[self.repeats:])
    


if __name__ == '__main__':
    
    np.random.seed(1234)
    a = TabularCell(1.003, (0,0))
    print(a.as_tex())
    a.set_alignment('c')
    print(a.as_tex())
    a.set_bold()
    a.set_emph()
    a.set_rotation(85)
    print(a.as_tex())
    a.set_fontsize('Large')
    print(a.as_tex())
    b = TabularCell('jake&dan$$ \\$ $ $', (0,0))
    print(b.as_tex())

    
    table = Tabular(np.array([[1,2,3],[4,5,6],[7,8,9]]))
    print('table[:],', type(table[:]))
    print('table[0,1],', type(table[0,1]))
    print('table[:],', type(table[:]))
    print('table[:,0],', type(table[:,0]))
    print('table[:,0][1:],', type(table[:,0][1:]))
    print('table[:,0][1],', type(table[:,0][1]))
    print('table[0,:],', type(table[0,:]))
    print('table[0],', type(table[0]))
    print('table[0,],', type(table[0,]))
    print('table[:,0][0],', type(table[:,0][0]))
    print('table[:,0][:2],', type(table[:,0][:2]))
    print('table[[0,1],:],', type(table[[0,1],:]))
    print('table[:,[0,1]],', type(table[:,[0,1]]))
    print('table[[0,1,2],:],', type(table[[0,1,2],:]))
    print('table[:,[0,1,2]],', type(table[:,[0,1,2]]))
    print('table[1:2,0],', type(table[1:2,0]))
    print('table[1:2,0:1],', type(table[1:2,0]))  
    print('table[1:2,0:1],', table[1:2,0].content)
    print('True,False:', table[:2].colfragment, table[:2].rowfragment)
    print(table[:,:2].shape)
    print('False,True:', table[:,:2].colfragment, table[:,:2].rowfragment)

    
    table = Table(np.array([['Variable','Mean','Std.'],['Health',5,6],['',8, '']]))
    
    print([c.content for c in table.flatten()])
    print([c.content for c in table[:,0]])
    print([c.isnull for c in table[:,0]])
    print([c.content for c in table[:,0]])
    
    table.set_bold()
    table[0].set_emph()    
    table[1:,0].merge()
    table[0].set_lines(2)
    table[0].set_alignment('l')
    table[1:].set_alignment('r')
    table[1,0].set_lines(3)
    table[2].set_fontsize('tiny')
    table[2,1:].merge()
    table[2,1:].set_alignment('c')
    table[0,1].set_fontsize('Huge')
    table[2].set_space_above(2)
    table[2].set_space_below(1)
    table[2].set_color('gray')
    table[2,0].set_alignment('c|')
    table.add_note('''\\textbf{Notes:} These are some notes about the table which are very detailed and should extend across the table.''')
    table.add_note('2nd Note')      
    print(table.as_tex())
    
#    ripped = parse_tex(table.as_tex())
#    print(ripped)
#    print(type(table[1,:]))
#    header = np.array(['One', 'Two', 'Three', 'Four', 'Five']).reshape(1,5)
#    
#    data = np.vstack((header, np.random.randn(100,5).astype(object)))
#    table = LongTable(data)
#    
#    
#    table.set_bold()
#    table[0].set_lines('=')
#    table[2].set_fontsize('Large')
#    table.set_location('l')
#    table[1:,0].set_digits(4)
#    table[1:,1].set_stars()
#    table[1:,2].set_formatter(format_int)
#    table.add_note('''\\textbf{Notes:} These are some notes about the table which are very detailed and should extend across the table.''')  
#    print(table.as_tex())
    