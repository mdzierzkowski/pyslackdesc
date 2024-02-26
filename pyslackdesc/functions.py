"""pyslackdesc.functions: functions module within the pyslackdesc package."""
import argparse
import os
import sys
import textwrap
from ._version import __version__


def arguments():
    """Parse arguments.

    Returns
    -------
    argparse.Namespace
        Returns Argparse Namespace.

    """
    parser = argparse.ArgumentParser(prog='pyslackdesc',
                                     description="pyslackdesc - simple, \
                                     interactive script to generate \
                                     Slack-desc files",
                                     epilog="Have fun!")

    parser.add_argument("-i", "--interactive", default=False,
                        help="run script in interactive mode",
                        action="store_true")
    parser.add_argument("-o", "--output", default='slack-desc',
                        metavar='filename',
                        help="output file (default is slack-desc)")
    parser.add_argument("-v", "--verbose", help="show generated file",
                        action="store_true", default=False)
    parser.add_argument("-V", "--version", action='version',
                        version='%(prog)s '
                        '{version}'.format(version=__version__))

    # Add group
    cmd_parser = parser.add_argument_group('commandline mode')
    cmd_parser.add_argument("-n", "--name", nargs=1,
                            metavar='name', type=str,
                            help="program name (single word)")
    cmd_parser.add_argument("-s", "--short", nargs='+',
                            metavar='"short description"', type=str,
                            help="program short description (one line)")
    cmd_parser.add_argument("-d", "--description", nargs='+',
                            metavar='"long description"',
                            help="program long description (up to 6 lines)")
    cmd_parser.add_argument("-u", "--url", nargs=1, metavar='url',
                            help="program URL")
    args = parser.parse_args()

    return args


def text_wrapper(text, prefix, separator=''):
    """Wrap text.

    Parameters:
    ----------
    text : {str}
        Text to be warped
    prefix : {str}
        Defines a name of the program to be used as a prefix
        for every line of text
    separator : {str}, optional
        Defines the text inserted between prefix and text
    Returns
    -------
    list
        Returns a list of strings (lines).

    """
    pkg_prefix = prefix + separator
    # empty lines need a special care
    if text != '':
        text_wrapper = textwrap.TextWrapper(
            width=79,
            initial_indent=pkg_prefix,
            subsequent_indent=pkg_prefix)
        warped_text = textwrap.dedent(text)
        warped_text = text_wrapper.wrap(warped_text)
        return warped_text
    else:
        # single line doesn't need trailing spaces
        warped_text = pkg_prefix.rstrip()
        # ensure to always return list, not string
        return warped_text.split()


def text_validator(text, one_word=False, one_line=False,
                   six_lines=False, pkg_name=None):
    """Validate the text that makes up the slack-desc file.

    Parameters:
    ----------
    text : {str}
        Text for validation
    one_word : {bool}, optional
        Defines if text has to be a single word (the default is False)
    one_line : {bool}, optional
        Defines if text has to be maximally six line long
        (the default is False)
    six_lines : {bool}, optional
        Defines if text has to be maximally six lines long
        (the default is False)
    pkg_name : {str}, optional
        Defines name of program (the default is None)
    Raises
    ------
    ValueError
        Raisers ValueError if text doesn't pass validation.
    Returns
    -------
    bool
        True if text passes validation. Otherwise raises an error.

    """
    if not text:
        raise ValueError("Error: Input can't be empty. Try again.")
    elif one_word:
        if (' ' in text):
            raise ValueError("Error: Use one word. Try again.")
        elif (len(text) > 77):
            raise ValueError("Error: Text is too long. Try again.")
    elif one_line:
        if not pkg_name:
            raise ValueError("Error: unknown program name.")
        elif (len(pkg_name) + len(text) + 2) > 79:
            raise ValueError(
                "Error: Package short description is too long. Try again.")
    elif six_lines:
        if not pkg_name:
            raise ValueError("Error: Unknown program name.")
        elif len(text_wrapper(text, pkg_name, ': ')) > 6:
            raise ValueError(
                "Error: Package description is too long. Try again.")
    else:
        return True


def user_input(question, one_word=False, one_line=False,
               six_lines=False, pkg_name=None):
    """Asks user for input and pass it to validator.

    Parameters:
    ----------
    question : {str}
        Content of the question asked to the user
    one_word : {bool}, optional
        Passed to the validator, defines if user input has to be a single word
        (the default is False)
    one_line : {bool}, optional
        Passed to the validator, defines if user input has to be maximally one
        line long (the default is False)
    six_lines : {bool}, optional
        Passed to the validator, defines if user input has to be maximally six
        lines long  (the default is False)
    pkg_name : {str}, optional
        Passed to the validator, defines name of a program
        (the default is None)
    Returns
    -------
    str
        Returns correct user input.

    """
    var_name = input(question)

    try:
        text_validator(var_name, one_word, one_line, six_lines, pkg_name)
    except ValueError as error:
        print(error)
        return user_input(question, one_word, one_line, six_lines, pkg_name)
    else:
        return var_name


def header():
    """Header of slack-build file.

    Returns
    -------
    list
        Returns a list of lines.

    """
    header = [
        '# HOW TO EDIT THIS FILE:',
        '# The "handy ruler" below makes it easier to edit a package'
        ' description.  Line',
        "# up the first '|' above the ':' following the base package name, "
        "and the '|'",
        '# on the right side marks the last column you can put a character in.'
        '  You must',
        "# make exactly 11 lines for the formatting to be correct.  It's also",
        "# customary to leave one space after the ':'.",
        ""]
    return header


def handy_ruler(pkg_name):
    """Create a handy ruler.

    Parameters:
    ----------
    pkg_name : {str}
        Name of program
    Returns
    -------
    list
        Returns single element list with 'handy ruler'.

    """
    ruler_intend = len(pkg_name) * ' '
    ruler_start = '|-----handy-ruler'  # 17 chars
    ruler_extender = (79 - len(ruler_intend + ruler_start) - 1) * '-'
    ruler_end = '|'
    handy_ruler = ruler_intend + ruler_start + ruler_extender + ruler_end
    # cause .split() removes whitespaces
    handy_ruler = [handy_ruler]
    return handy_ruler


def path_validator(path, override=False):
    """Validate file path. Asks if file exist.

    Parameters:
    ----------
    path : {str}
        Path to the output file
    override : {bool}, optional
        If true output file will be overridded without asking.
        (the default is False, which mean ask about overridding)
    Returns
    -------
    str
        Returns correct absolute path.

    """
    # Validating path
    file_path = os.path.expandvars(path)
    file_path = os.path.expanduser(file_path)
    file_path = os.path.abspath(file_path)
    dir_path = os.path.dirname(file_path)

    # check if file exist
    if not os.path.isdir(dir_path):
        sys.exit("Direcotry not found. Exiting.")
    elif os.path.isfile(file_path):
        if override:
            with open(file_path, mode='w') as f:
                f.truncate(0)
            return file_path
        else:
            ans = input('File exist. Override? [y|n]: ')
            if ans.lower() == 'n':
                sys.exit('Exiting...')
            elif ans.lower() == 'y':
                with open(file_path, mode='w') as f:
                    f.truncate(0)
                return file_path
            else:
                sys.exit('Unknown answer. Exiting...')
    else:
        return file_path


def write_file(text, file_path):
    """Write text to file.

    Parameters:
    ----------
    text : {str}
        Text to be written
    file_path : {str}
        Path to output file
    Returns
    -------
    bool
        Returns True if success.

    """
    with open(file_path, mode='a') as f:
        f.write(text + '\n')
        return True
