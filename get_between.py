
from fileinput import close

def get_between(txt:str, open_char:str="'", close_char:str="'", start:int=1 ):
    """Parse all content in supplied text that appears between the open and close characters, exclusively.
    If txt is empty, or open_char is not found, returns ('', -1, -1).  If the close_char is never found, 
    returns the txt from the starting positon through the end of the txt.

    Args:
        txt (str): String text to parse out subset.
        open_char (str, optional): Character defining the opening of the subset. Defaults to "'".
        close_char (str, optional): Character defining the close of the subset. Defaults to "'".
        start (int, optional): Position in txt to start searching. Defaults to 1.

    Returns:
        tuple: (subset:str, starting position of subset:int, ending position of subset:int)
    """
    sp = txt.find(open_char, start)
    ep = sp+1
    if sp == -1 or open_char=='' or close_char=='': return ('',-1,-1) # if not found, or empty

    if open_char == close_char:  # quote like things
        while ep <= len(txt):
            ep1 = txt.find(close_char, ep)
            ep = len(txt)+1 if ep1 == -1 else ep1+1 
            if txt[ep1:ep1+1] == close_char and close_char not in [txt[ep1-1:ep1], txt[ep1+1:ep1+2]]:
                break 
    else: # paren-like things
        i = 0
        for c in txt[sp:]:
            if c == open_char: i+=1
            if c == close_char: i -=1
            if i == 0: break
            ep +=1
    sp +=1
    ep -=1
    return (txt[sp:ep].replace(open_char*2, open_char) if open_char == close_char else txt[sp:ep], sp, ep)
