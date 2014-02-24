class MergeError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def texCommands():
    """tex commands required for tables
    
    Returns
    -------
    tex : str
        string to put in header of latex file
    """

    return r'''
\usepackage{booktabs}
\usepackage{makecell}
\usepackage{longtable}
\usepackage{multirow}
\usepackage[normalem]{ulem}
\usepackage{tabu}
\usepackage{caption}
\usepackage{pdflscape}
\usepackage[table]{xcolor}
\usepackage{threeparttablex}

\renewcommand{\rothead}[2][60]{\makebox[9mm][c]{\rotatebox{#1}{\makecell[c]{#2}}}}
\newcommand{\mr}{\multirow}
\newcommand{\mc}{\multicolumn}
'''

#def parse_tex(tex):
#    '''parses a tex string into a Tabular Object
#    
#    Parameters
#    ----------
#    tex: str
#        text containing LateX table
#    '''
#    tab = 'tabu'
#    begin = 13 + len(tab)
#    tabular = tex[tex.index('\\begin{tabu}')+begin:tex.index('\\end{tabu}')]
#    tabular = tabular.replace('\n', '')
#    
#    return tabular