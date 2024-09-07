from itertools import product
from dataclasses import dataclass
import numpy as np

@dataclass
class Slot:
    color: int
    sym  : int

@dataclass
class Register:
    sl0: Slot
    sl1: Slot
    sl2: Slot


COLORS = set(range(3))
SYMBOLS = set(range(4))

COLOR = 0
SYM = 3

registers = np.array([Register(Slot(c0, s0), Slot(c1, s1), Slot(c2, s2)) for c0, c1, c2, s0, s1, s2 in product(COLORS, COLORS, COLORS, SYMBOLS, SYMBOLS, SYMBOLS)])

def slots_of(reg):
    return[reg.sl0, reg.sl1, reg.sl2]

def num_slot_with_cond(reg, slot_func):
    ret = 0
    for slot in slots_of(reg):
        if slot_func(slot): ret += 1
    return ret

def slot_is_cs(color, sym):
    return lambda slot: slot.color == color and slot.sym == sym
def slot_is_c(color):
    return lambda slot: slot.color == color
def slot_is_s( sym):
    return lambda slot: slot.sym == sym

def reg_same_color(reg):
    slot_colors = {slot.color for slot in slots_of(reg)}
    return len(slot_colors) == 1

def reg_same_sym(reg):
    slot_syms = {slot.sym for slot in slots_of(reg)}
    return len(slot_syms) == 1

# [3, 7, 2, 8, 4, 5, 0, 1, 9, 6]

def cond0(reg):
    # There is a single Silly Sausage
    if num_slot_with_cond(reg, slot_is_cs(COLOR, SYM)) == 1: return True
    else: return False

def cond1(reg):
    # There is a single Sassy Sally, unless the slot in the same position 2 stages ago was Soggy.
    #less likely than cond 0
    return cond0(reg)

def cond2(reg):
    # There are 2 or more Soggy Stevens.
    if num_slot_with_cond(reg, slot_is_cs(COLOR, SYM)) >= 2: 
        return True
    else: return False
    
def cond3(reg):
    # There are 3 Simons, unless any of them are Sassy.
    if num_slot_with_cond(reg, slot_is_s(SYM)) ==3 and num_slot_with_cond(reg, slot_is_c(COLOR)) ==0: 
        return True
    else: return False

def cond4(reg):
    #There is a Sausage adjacent to a Sally, unless every adjacent Sally is Soggy.
    #first slot is Sauasge
    if reg.sl0.sym == SYM and reg.sl1.sym == SYM and reg.sl1.color is not COLOR:
        return True
    #third slot is Sausage
    if reg.sl2.sym == SYM and reg.sl1.sym == SYM and reg.sl1.color is not COLOR:
        return True 
    #second slot is Sausage
    if reg.sl1.sym == SYM and (reg.sl0.sym == SYM or reg.sl2.sym == SYM):
        sallys = [slot for slot in slots_of(reg) if slot.sym == SYM]
        for sally in sallys:
            if sally.color is not COLOR:
                return True
    return False

def cond5(reg):
    # There are exactly 2 Silly slots, unless they are both Steven.
    if num_slot_with_cond(reg, slot_is_c(COLOR)) ==2:
        silly_slots = [slot for slot in slots_of(reg) if slot.color is COLOR]
        if silly_slots[0].sym is SYM and silly_slots[1].sym is SYM:  return False
        else: return True
    return False

def cond6(reg):
    # There is a single Soggy slot, unless the previous stage had any number of Sausage slots.
    #less likely due to unless
    if num_slot_with_cond(reg, slot_is_c(COLOR)) ==1:
        return True
    return False

def cond7(reg):
    # All 3 slots are the same symbol and colour, unless there has been a Soggy Sausage in any previous stage.
    #less likely
    if reg_same_color(reg) and reg_same_sym(reg): return True
    return False

def cond8(reg):
    # All 3 slots are the same colour, unless any of them are Sally or there was a Silly Steven in the last stage.
    #less likely
    if reg_same_color(reg):
        if num_slot_with_cond(reg, slot_is_s(SYM)) ==0:
            return True
    return False

def cond9(reg):
    # There are any number of Silly Simons, unless there has been a Sassy Sausage in any previous stage.
    #less liekly
    if num_slot_with_cond(reg, slot_is_cs(COLOR, SYM)) > 0:
        return True
    else:
        return False

conds = [cond0, cond1, cond2, cond3, cond4, cond5, cond6, cond7, cond8, cond9]

sums = []
for idx, cond in enumerate(conds):
    bool_arr = [cond(reg) for reg in registers]
    sums.append(sum(bool_arr))
    print(f"cond {idx}: {sums[-1]} / {len(bool_arr)}")

sums_e = list(enumerate(sums))
sums_e.sort(key = lambda x: x[1])
print([idx for idx, _ in sums_e])
