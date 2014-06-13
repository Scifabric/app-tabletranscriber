# -*- coding: utf-8 -*-

priorities_map = { 
                   "0": ("Economia", 1.0),
                   "1": ("População/Demografia", 0.9),
                   "2": ("Violência/Criminalidade", 0.8),
                   "3": ("Outros", 0.7),
                   "4": ("Finanças", 0.6),
                   "5": ("Transporte", 0.5),
                   "6": ("Educação", 0.4),
                   "7": ("Saúde", 0.3),
                   "8": ("Administração Pública", 0.2)
                  }


def get_priority(code):
    try:
        return priorities_map[code][1]
    except Exception, e:
        raise e
    
def get_subject(code):
    try:
        return priorities_map[code][0]
    except Exception, e:
        raise e



def set_priority(code, name, value):
    priorities_map[code] = (name, value)


def get_subject_from_code(code):
    return priorities_map[code][0]        
