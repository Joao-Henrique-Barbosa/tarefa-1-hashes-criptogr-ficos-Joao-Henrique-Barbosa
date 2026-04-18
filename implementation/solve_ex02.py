import random
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, 'functions'))
from hash0 import xor32_hash

"""
ESTUDO DE CASO: ATAQUE DE SEGUNDA PRÉ-IMAGEM (XOR-HASH)
------------------------------------------------------
O ataque de segunda pré-imagem consiste em, dada uma entrada X, encontrar X' tal que
H(X) == H(X') e X != X'. 

DIFERENÇA PARA COLISÃO:
No ataque de colisão, temos a liberdade de escolher X e X'. Aqui, um dos lados está
fixo. Para quebrar a segunda pré-imagem de funções lineares, aplicamos 'diferenciais'
neutros. 

TEORIA DO DIFERENCIAL:
Ao escolhermos duas posições 'i' e 'j' que mapeiam para o mesmo shift (ex: 0 e 4),
qualquer mudança Delta aplicada a ambas é cancelada pela operação XOR:
XOR_Novo = (s_i ^ Delta) ^ (s_j ^ Delta) ^ ... = (s_i ^ s_j) ^ (Delta ^ Delta) ^ ...
Como Delta ^ Delta é 0, o hash final permanece inalterado.
"""

def solve_second_preimage_robust(original_s: str):
    target_hash = xor32_hash(original_s)
    s_list = list(original_s)
    n = len(s_list)
    
    # Tentamos encontrar um par de caracteres para aplicar a mutação diferencial
    for _ in range(1000):
        # Selecionamos dois índices aleatórios que compartilham o mesmo bloco/shift
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        
        if i != j and i % 4 == j % 4:
            # Selecionamos um diferencial de bit (Delta)
            delta = random.randint(1, 255)
            
            # Aplicamos o Delta a ambos os caracteres
            new_ci = ord(s_list[i]) ^ delta
            new_cj = ord(s_list[j]) ^ delta
            
            # Validamos se os novos valores são caracteres ASCII válidos (imprimíveis)
            if 33 <= new_ci <= 126 and 33 <= new_cj <= 126:
                temp_s = list(s_list)
                temp_s[i] = chr(new_ci)
                temp_s[j] = chr(new_cj)
                res = "".join(temp_s)
                
                # Verificação final para garantir que o hash se manteve (integridade)
                if res != original_s and xor32_hash(res) == target_hash:
                    return res
                    
    return "Falha ao encontrar mutação no range ASCII"

if __name__ == "__main__":
    target = "bitcoin0"
    result = solve_second_preimage_robust(target)
    print(f"Segunda Pré-imagem para '{target}': {result}")
    
    # Sincronização automatizada da solução para submissão
    base_path = os.path.join(BASE_DIR, 'solutions', 'exercise02')
    with open(f"{base_path}.txt", 'w') as f:
        f.write(result)
    with open(f"{base_path}.sh", 'w', newline='\n') as f:
        f.write(f"#!/bin/bash\npython3 ../implementation/solve_ex02.py\n")
