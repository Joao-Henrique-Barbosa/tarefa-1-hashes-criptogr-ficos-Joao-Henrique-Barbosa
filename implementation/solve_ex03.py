import random
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, 'functions'))
from hash0 import xor32_hash

"""
ESTUDO DE CASO: ATAQUE DE PRIMEIRA PRÉ-IMAGEM (INVERSÃO DE HASH)
---------------------------------------------------------------
Uma função de hash segura deve ser unidirecional (one-way), ou seja, deve ser
computacionalmente impossível reverter o digest para a entrada original.

VULNERABILIDADE EXPLORADA:
A função xor32_hash é vulnerável à inversão total. O digest de 32 bits é composto por
4 bytes independentes, cada um resultando do XOR de um subconjunto de caracteres.
Para inverter o hash 'T', decompomos em bytes alvos (T_0, T_1, T_2, T_3).

ALGORITMO DE INVERSÃO:
Podemos gerar uma string de 8 caracteres que satisfaça o hash de forma trivial:
- Escolhemos 4 caracteres aleatórios (c0, c1, c2, c3).
- Resolvemos as equações XOR para os próximos 4 caracteres (c4, c5, c6, c7):
  c4 = c0 ^ T_0
  c5 = c1 ^ T_1
  c6 = c2 ^ T_2
  c7 = c3 ^ T_3
Se o resultado de 'ci ^ Ti' for um caractere imprimível, encontramos a pré-imagem.
"""

def solve_first_preimage_random(target_hex: str, length=8):
    target_int = int(target_hex, 16)
    # Extração dos 4 bytes alvos do digest hexadecimal
    target_bytes = [(target_int >> (i * 8)) & 0xFF for i in range(4)]
    
    while True:
        # Iniciamos com uma semente aleatória de 4 caracteres (primeiro bloco)
        candidate = [random.randint(33, 126) for _ in range(length)]
        xor_sum = [0] * 4
        
        # Acumulamos o XOR de todos os caracteres EXCETO os do último bloco de 4
        for i in range(length - 4):
            xor_sum[i % 4] ^= candidate[i]
            
        # Para cada 'slot' de 8 bits, calculamos o caractere de ajuste necessário
        # para que o XOR final de cada slot coincida com o byte alvo correspondente.
        valid = True
        for i in range(length - 4, length):
            # Resolvemos: xor_acumulado ^ caractere_ajuste = alvo
            # Portanto: caractere_ajuste = xor_acumulado ^ alvo
            needed = xor_sum[i % 4] ^ target_bytes[i % 4]
            
            # Verificamos se o ajuste gerou um caractere ASCII imprimível
            if 33 <= needed <= 126:
                candidate[i] = needed
            else:
                valid = False # Se o ajuste for inválido, tentamos uma nova semente
                break
        
        if valid:
            res = "".join(chr(c) for c in candidate)
            # Confirmação final usando a função de hash fornecida
            if xor32_hash(res).lower() == target_hex.lower():
                return res

if __name__ == "__main__":
    target_hash = "1b575451"
    result = solve_first_preimage_random(target_hash)
    print(f"Pré-imagem para {target_hash}: {result}")
    
    # Automatização da persistência da solução encontrada
    base_path = os.path.join(BASE_DIR, 'solutions', 'exercise03')
    with open(f"{base_path}.txt", 'w') as f:
        f.write(result)
    with open(f"{base_path}.sh", 'w', newline='\n') as f:
        f.write(f"#!/bin/bash\npython3 ../implementation/solve_ex03.py\n")
