#!/usr/bin/env python3

import sys
import argparse
import colorama
from colorama import Fore, Back, Style

from naming import conventions

def get_major_scale(note):
    structure = [2, 2, 1, 2, 2, 2, 1]

    scale = [note]
    for i in structure:
        note += i
        if note > 12:
            note = note % 12
        scale.append(note)
    return scale


def translate(note, convention='neolatin', alternative="diesis"):
    d = conventions[convention]
    if type(note) == str:
        for k, v in d.items():
            for n in v:
                if note == n:
                    return k
    elif type(note) == int:
        if note > 12:
            note = note % 12
        n = d[note]
        if len(d) == 1:
            return n[0]
        if alternative == 'diesis':
            return n[0]
        elif alternative == 'bemolle':
            return n[1]

def get_triad(major_scale):
    return [
        major_scale[0],
        major_scale[2],
        major_scale[4],
    ]

def print_notes(notes, convention='neolatin'):
    print('\t'.join(
        [translate(note, convention=convention) for note in notes]
    ))


def print_fretboard(fretboard, orientation):
    if orientation == 'vertical':
        topline = '┌' + ('─' * 7 +  '┬') * 5
        midline = '├' + ('─' * 7 +  '┼') * 5
        botline = '└' + ('─' * 7 +  '┴') * 5
        vline = '\t'.join(['|' for i in fretboard['header']])
        print('\t'.join(fretboard['header']))
        print(topline)
        for i, fret in enumerate(fretboard['frets']):
            print(vline)
            print('\t'.join(fret))
            print(vline)
            if i < len(fretboard['frets']) - 1:
                print(midline)
            else:
                print(botline)

    if orientation == 'horizontal':
        topline = '\t┌' + ('─' * 15 +  '┬') * len(fretboard['frets'])
        midline = '\t├' + ('─' * 15 +  '┼') * len(fretboard['frets'])
        botline = '\t└' + ('─' * 15 +  '┴') * len(fretboard['frets'])
        print(topline)
        for i, header in enumerate(fretboard['header']):
            string = []
            string.append(header)
            for frets in fretboard['frets']:
                string.append(frets[i])
            print('\t│\t'.join(string), '\t│')
            # print('\t│\t'.join([' ' for i in string]), '\t│\n')
            if i < len(fretboard['header']) - 1:
                print(midline)
            else:
                print(botline)

def show_chords(note, frets=5, orientation='horizontal', convention='neolatin'):
    strings = [5, 10, 3, 8, 12, 5]

    note = translate(note, convention=convention)
    scale = get_major_scale(note)
    triad = get_triad(scale)

    header = []
    for s in strings:
        if s in triad:
            header.append(
                f'{Fore.BLUE}{translate(s, convention=convention)}{Style.RESET_ALL}'
            )
        else:
            header.append(
                translate(s, convention=convention)
            )
    fretboard =  {
        'header': header,
        'frets': []
    }
    for f in range(1, frets + 1):
        f = f % 12
        fret_notes = []
        for s in strings:
            fret_note = s + f
            if fret_note > 12:
                fret_note = fret_note % 12
            if fret_note in triad:
                fret_notes.append(
                    f"{Fore.BLUE}{translate(fret_note, convention=convention)}{Style.RESET_ALL}"
                )
            else:
                fret_notes.append(
                    translate(fret_note, convention=convention)
                )
        fretboard['frets'].append(fret_notes)
    print_fretboard(fretboard, orientation)


def parse_args():
    parser = argparse.ArgumentParser(description='Show chord of given note')
    parser.add_argument('note', type=str,
            help='Note to show chords of')
    parser.add_argument('convention', type=str,
            nargs= '?', default='neolatin',
            help='Naming convention to print in')
    parser.add_argument('frets', type=int,
            nargs= '?', default=5, 
            help='How many frets to print')
    parser.add_argument('orientation', type=str,
            nargs= '?', default='vertical',
            help='How to print fretboard')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    note = args.note
    frets = args.frets
    orientation = args.orientation
    convention = args.convention
    show_chords(note, frets, orientation, convention)

if __name__ == '__main__':
    main()

