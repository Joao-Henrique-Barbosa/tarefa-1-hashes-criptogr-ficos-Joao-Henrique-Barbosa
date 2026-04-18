import random
import string
import sys
import os

# Configuração de ambiente para importação das funções fornecidas
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, 'functions'))
from hash0 import xor32_hash

"""
ESTUDO DE CASO: ATAQUE DE COLISÃO EM HASH BASEADO EM XOR
------------------------------------------------------
Este script demonstra a fragilidade de funções de hash que utilizam o operador XOR
de forma linear. O XOR possui propriedades algébricas que facilitam a criptoanálise:
1. Comutatividade: A ^ B = B ^ A
2. Auto-inversão: A ^ A = 0
3. Elemento Neutro: A ^ 0 = A

A função xor32_hash aplica o XOR em blocos de 4 bytes (32 bits). Isso significa que
caracteres em posições distantes 4 unidades entre si (0, 4, 8...) afetam o mesmo 
byte do digest final. 

ALGORITMO DE ATAQUE:
Exploramos a 'neutralidade diferencial'. Se introduzirmos uma mudança (delta) em um
caractere da posição 'i' e a MESMA mudança no caractere da posição 'j' (onde i e j 
mapeiam para o mesmo shift), as mudanças se anulam no XOR final:
(c_i ^ delta) ^ (c_j ^ delta) == c_i ^ c_j ^ (delta ^ delta) == c_i ^ c_j ^ 0.
"""

def find_collision_random(length=8):
    chars = string.ascii_letters + string.digits
    while True:
        # Geramos uma string base aleatória para provar a generalidade do ataque
        s1 = list(''.join(random.choices(chars, k=length)))
        s2 = list(s1)
        
        # Selecionamos um 'slot' de 8 bits (0, 8, 16 ou 24 bits de deslocamento)
        shift_idx = random.randint(0, 3)
        # Identificamos todos os índices da string que contribuem para este slot
        indices = [idx for idx in range(length) if idx % 4 == shift_idx]
        
        if len(indices) < 2: continue
        
        # Selecionamos dois caracteres para realizar a mutação cancelável
        idx1, idx2 = random.sample(indices, 2)
        
        # Escolhemos um delta aleatório para o XOR
        delta = random.randint(1, 255)
        
        # Aplicamos a mutação via XOR
        new_c1 = ord(s1[idx1]) ^ delta
        new_c2 = ord(s1[idx2]) ^ delta
        
        # Garantimos que os novos caracteres permaneçam no range ASCII imprimível
        if 33 <= new_c1 <= 126 and 33 <= new_c2 <= 126:
            s2[idx1] = chr(new_c1)
            s2[idx2] = chr(new_c2)
            res1, res2 = "".join(s1), "".join(s2)
            
            # Verificação final de integridade da colisão
            if res1 != res2 and xor32_hash(res1) == xor32_hash(res2):
                return res1, res2

if __name__ == "__main__":
    s1, s2 = find_collision_random()
    result = f"{s1},{s2}"
    print(f"Colisão Gerada: {result}")
    
    # Persistência automatizada dos resultados para submissão
    base_path = os.path.join(BASE_DIR, 'solutions', 'exercise01')
    with open(f"{base_path}.txt", 'w') as f:
        f.write(result)
    with open(f"{base_path}.sh", 'w', newline='\n') as f:
        f.write(f"#!/bin/bash\npython3 ../implementation/solve_ex01.py\n")
