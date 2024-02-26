"""pyslackdesc - simple script to generate Slackware's slack-desc files."""

import sys
from .functions import (arguments, text_wrapper, text_validator,
                        user_input, header, handy_ruler,
                        path_validator, write_file)


def main():
    """Execute program."""
    args = arguments()

    # Gathering information and storing in dictionary
    program = dict()
    if (len(sys.argv) == 1) or args.interactive:
        # interactive mode: to override or not to override?
        path = path_validator(args.output)

        program['name'] = user_input('Program name (single word): ',
                                     one_word=True)
        program['short_desc'] = user_input('Short description (one line): ',
                                           one_line=True,
                                           pkg_name=program['name'])
        program['desc'] = user_input('Description (up to six lines): ',
                                     six_lines=True, pkg_name=program['name'])
        program['url'] = user_input('Program homepage URL: ',
                                    one_word=True, one_line=True,
                                    pkg_name=program['name'])
    else:
        # cli mode: to override!
        if args.name and args.short and args.description and args.url:
            try:
                path = path_validator(args.output, override=True)
                # Validate and set name
                text_validator(' '.join(args.name))
                program['name'] = ' '.join(args.name)
                # Validate and set short description
                text_validator(' '.join(args.short), pkg_name=program['name'])
                program['short_desc'] = ' '.join(args.short)
                # Validate and set long description
                text_validator(' '.join(args.description), six_lines=True,
                               pkg_name=program['name'])
                program['desc'] = ' '.join(args.description)
                # Validate and set URL
                text_validator(' '.join(args.url), one_word=True,
                               one_line=True, pkg_name=program['name'])
                program['url'] = ' '.join(args.url)
            except ValueError as error:
                print(error)
        else:
            sys.exit('Missing argument(s). Use --help for help.')
    # common part
    program['header'] = header()
    program['ruler'] = handy_ruler(program['name'])
    program['empty'] = ''

    # warping some values
    for key in ('short_desc', 'desc', 'url', 'empty'):
        program[key] = text_wrapper(program[key], program['name'], ': ')

    # there is 6 lines for a 'desc' insert missing lines
    if len(program['desc']) < 6:
        for _ in range(6 - len(program['desc'])):
            program['desc'].extend(program['empty'])

    # writting file
    for key in ('header', 'ruler', 'short_desc', 'empty',
                'desc', 'empty', 'url', 'empty'):
        for text in program[key]:
            write_file(text, path)

    # verbose option
    if args.verbose:
        print('\nContent of {}:\n'.format(path))
        with open(path, mode="r") as f:
            print(f.read(), end='')
