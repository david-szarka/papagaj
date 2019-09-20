# coding=utf-8
# papagaj
# Copyright (C) 2019 Dávid Szarka
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


def repeatitionCheck(x):
    try:
        repeatition = int(x)
    except:
        repeatition = 1
    return repeatition


def coefficientCheck(x):
    try:
        koeficientspeed = float(x.replace(",", "."))
    except:
        koeficientspeed = 1
    return koeficientspeed


meniItemDict = {
    1:"Record"
    ,2:"Play"
    ,3:"Play Again"
    ,4:"About"
    ,5:"Exit"
}

dataForPlay = {
    'menudict':meniItemDict,
    'sequence': ['repeatition', 'koeficientspeed'],
    'repeatition': {
        'header': "Number of repetitions",
        'text': " =>How many imes you want replay actions, or press enter, default is 1\nEnter real number:",
        'result': 0,
        'checkfunc': repeatitionCheck
    },

    'koeficientspeed': {
        'header': "Speed coefficient",
        'text': " =>Example: 0.5 is 2×faster, or press enter, default is 1.\nEnter speedcoefficient:",
        'result': 0,
        'checkfunc': coefficientCheck
    },
}


