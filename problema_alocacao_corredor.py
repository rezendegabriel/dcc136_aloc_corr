# -*- coding: utf-8 -*-

"""
Problema de Alocação de Corredor
Inteligência Computacional - DCC136

Discente: Gabriel Rezende
           
Docente: Luciana Brugiolo Gonçalvez
"""

#%% BIBLIOTECAS

from random import SystemRandom

import numpy as np
import time

random = SystemRandom()

#%% FUNÇÕES ESTRUTURAIS

#recalcula custo e atualiza arranjo
def recalcula_arranjo(solucao_it, num_fac,
                      num_fac_arranjo_sup, num_fac_arranjo_inf,
                      comps, centros, matriz_trafs):
    
    custo_total_it = 0 #custo total
    
    pos = [0]*num_fac #posições das facilidades
    
    #comprimentos de cada arranjo do corredor
    comp_arranjo_sup = 0
    comp_arranjo_inf = 0
    
    #atualizações no arranjo superior
    for i in range(num_fac_arranjo_sup):
        fac_i = solucao_it[i]
        
        pos[fac_i] = comp_arranjo_sup+centros[fac_i] #atualização da posição
        
        comp_arranjo_sup += comps[fac_i] #atualização do comprimento
    
    #atualizações no arranjo inferior
    for i in range(num_fac_arranjo_inf):
        fac_i = solucao_it[(num_fac-1)-i]
        
        pos[fac_i] = comp_arranjo_inf+centros[fac_i] #atualização da posição
        
        comp_arranjo_inf += comps[fac_i] #atualização do comprimento
        
    #recalcula custo do arranjo superior com arranjo superior
    for i in range(num_fac_arranjo_sup):
        fac_i = solucao_it[i]

        n = i+1
        while n < num_fac_arranjo_sup:
            fac_n = solucao_it[n]
            
            custo_total_it += abs(pos[fac_i]-pos[fac_n])*matriz_trafs[fac_i][fac_n]
            
            n+=1
            
        #recalcula custo do arranjo superior com arranjo inferior
        for j in range(num_fac_arranjo_inf):
            fac_j = solucao_it[(num_fac-1)-j]
            
            custo_total_it += abs(pos[fac_i]-pos[fac_j])*matriz_trafs[fac_i][fac_j]
    
    #recalcula custo do arranjo inferior com arranjo inferior
    for j in range(num_fac_arranjo_inf):
        fac_j = solucao_it[(num_fac-1)-j]
        
        n = j+1
        while n < num_fac_arranjo_inf:
            fac_n = solucao_it[(num_fac-1)-n]
            
            custo_total_it += abs(pos[fac_j]-pos[fac_n])*matriz_trafs[fac_j][fac_n]
            
            n+=1
            
    return custo_total_it  

#seleciona vizinho aleatoriamente na vizinhança k
def seleciona_vizinho(k, solucao_it, num_fac, num_fac_arranjo_sup, num_fac_arranjo_inf):
    #troca aleatória no arranjo superior
    if k == 1:
        i = random.randint(0, num_fac_arranjo_sup-1)
        n = i
    
        while i == n:
            n = random.randint(0, num_fac_arranjo_sup-1)
            
        fac_i = solucao_it[i]
        solucao_it[i] = solucao_it[n]
        solucao_it[n] = fac_i

    #troca aleatória no arranjo inferior
    elif k == 2:
        j = random.randint(num_fac_arranjo_inf, num_fac-1)
        n = j
        
        while j == n:
            n = random.randint(num_fac_arranjo_inf, num_fac-1)
            
        fac_j = solucao_it[j]
        solucao_it[j] = solucao_it[n]
        solucao_it[n] = fac_j
    
    #troca aleatória entre os arranjos
    else:
        i = random.randint(0, num_fac_arranjo_sup-1)
        j = random.randint(num_fac_arranjo_inf, num_fac-1)
        
        fac_j = solucao_it[j]
        solucao_it[j] = solucao_it[i]
        solucao_it[i] = fac_j

#%% VND

def vnd(solucao_it, custo_total_it, k_vns, r_vnd, num_fac,
        num_fac_arranjo_sup, num_fac_arranjo_inf,
        comps, centros, matriz_trafs):
    
    solucao_m = solucao_it.copy()
    custo_total_m = custo_total_it
    
    k_vnd = 1
    while k_vnd <= r_vnd:
        #seleciona vizinho aleatoriamente na vizinhança k
        seleciona_vizinho(k_vns, solucao_it, num_fac, num_fac_arranjo_sup, num_fac_arranjo_inf)
        
        #recalcula custo
        custo_total_it = recalcula_arranjo(solucao_it, num_fac,
                                           num_fac_arranjo_sup, num_fac_arranjo_inf,
                                           comps, centros, matriz_trafs)
        
        #verifica se houve melhora na solução
        if custo_total_it < custo_total_m:
            custo_total_m = custo_total_it
            solucao_m = solucao_it.copy()
            
            k_vnd = 1
        else:
            k_vnd += 1
            
    return solucao_m, custo_total_m

#%% VNS

def vns(solucao_it, custo_total_it, r_vns, r_vnd, num_fac,
        num_fac_arranjo_sup, num_fac_arranjo_inf,
        comps, centros, matriz_trafs):
    
    solucao_m = solucao_it.copy()
    custo_total_m = custo_total_it
     
    k_vns = 1
    while k_vns <= r_vns:
        #seleciona vizinho aleatoriamente na vizinhança k
        seleciona_vizinho(k_vns, solucao_it, num_fac, num_fac_arranjo_sup, num_fac_arranjo_inf)
        
        #recalcula custo
        custo_total_it = recalcula_arranjo(solucao_it, num_fac,
                                           num_fac_arranjo_sup, num_fac_arranjo_inf,
                                           comps, centros, matriz_trafs)
        
        #VND
        solucao_vnd, custo_total_vnd = vnd(solucao_it, custo_total_it, k_vns, r_vnd, num_fac,
                                           num_fac_arranjo_sup, num_fac_arranjo_inf,
                                           comps, centros, matriz_trafs)
        
        #verifica se houve melhora na solução
        if custo_total_vnd < custo_total_m:
            custo_total_m = custo_total_vnd
            solucao_m = solucao_vnd.copy()
            
            k_vns = 1
        else:
            k_vns += 1
                
    return solucao_m, custo_total_m

#%% GRASP + VNS(VND)

def grasp_vns_vnd(alpha, max_it, r_vns, r_vnd, num_fac, facs, comps, centros, matriz_trafs, matriz_dec):
    solucao = [] #soluções comparativas para cada repetição do GRASP
    custo_total = 0 #custos comparativos para cada repetição do GRASP
    
    #fase de construção
    for it in range(max_it):
        facs_it = facs.copy() #controle de facilidades a serem inseridas a cada repetição do GRASP
        
        matriz_dec_it = np.zeros((num_fac, num_fac))
        
        #controle do critério de inserção a cada repetição do GRASP
        for i in range(num_fac):
            for j in range(num_fac):
                matriz_dec_it[i][j] = matriz_dec[i][j]
        
        solucao_it = [-1]*num_fac #arranjo da solução
        
        pos = [0]*num_fac #posições das facilidades
    
        custo_total_it = 0 #custo da solução
        
        lc = [] #lista de candidatos
        
        lrc = [] #lista restrita de candidatos
        
        #comprimentos de cada arranjo do corredor
        comp_arranjo_sup = 0
        comp_arranjo_inf = 0
        
        #número de facilidades em cada arranjo
        num_fac_arranjo_sup = 0
        num_fac_arranjo_inf = 0
        
        #ordenação da lista de candidatos
        for i in range(num_fac**2):
            lc.append(np.argmax(matriz_dec_it))
            
            matriz_dec_it[int(lc[i]/num_fac)][lc[i]%num_fac] = -1
            
        #1ª inserção (arranjo superior)
        lrc = lc[:(int(len(lc)*alpha))] #atualiza a lista restrita de candidatos
        
        id_cand = random.choice(lrc) #seleciona, aleatoriamente, o candidato que irá entrar na solução
            
        fac_sup = int(id_cand/num_fac) #localiza a facilidade correspondente
        
        #atualiza a lista de candidatos
        for i in range(num_fac):    
            lc.remove(fac_sup*num_fac+i)
            
        pos[fac_sup] = centros[fac_sup] #atualiza a posição da facilidade
        
        comp_arranjo_sup += comps[fac_sup] #atualiza comprimento do arranjo superior
        
        solucao_it[num_fac_arranjo_sup] = fac_sup #insere na solução (arranjo superior)
        
        num_fac_arranjo_sup += 1 #atualiza o número de facilidades no arranjo superior
        
        facs_it.remove(fac_sup) #atualiza as facilidades a serem inseridas
        
        #2ª inserção (arranjo inferior)
        lrc = lc[:(int(len(lc)*alpha))] #atualiza a lista restrita de candidatos
        
        id_cand = random.choice(lrc) #seleciona, aleatoriamente, o candidato que irá entrar na solução
            
        fac_inf = int(id_cand/num_fac) #localiza a facilidade correspondente
        
        #atualiza a lista de candidatos
        for i in range(num_fac):    
            lc.remove(fac_inf*num_fac+i)
            
        pos[fac_inf] = centros[fac_inf] #atualiza a posição da facilidade
        
        comp_arranjo_inf += comps[fac_inf] #atualiza comprimento do arranjo inferior
        
        num_fac_arranjo_inf += 1 #atualiza o número de facilidades no arranjo inferior
        
        solucao_it[num_fac-num_fac_arranjo_inf] = fac_inf #insere na solução (arranjo inferior)
        
        facs_it.remove(fac_inf) #atualiza as facilidades a serem inseridas
        
        custo_total_it += abs(pos[fac_sup]-pos[fac_inf])*matriz_trafs[fac_sup][fac_inf]
        
        #demais inserções
        while len(facs_it) > 0:
            lrc = lc[:(int(len(lc)*alpha))] #atualiza a lista restrita de candidatos
            
            id_cand = random.choice(lrc) #seleciona, aleatoriamente, o candidato que irá entrar na solução
            
            fac = int(id_cand/num_fac) #localiza a facilidade correspondente
            
            #atualiza a lista de candidatos
            for i in range(num_fac):    
                lc.remove(fac*num_fac+i)
            
            #inserção no arranjo inferior
            if comp_arranjo_inf < comp_arranjo_sup:
                pos[fac] = comp_arranjo_inf+centros[fac] #atualiza a posição da facilidade
                
                comp_arranjo_inf += comps[fac] #atualiza comprimento do arranjo inferior
                
                #atualiza o custo total com o arranjo superior
                for i in range(num_fac_arranjo_sup):
                    fac_sup = solucao_it[i]
                    
                    custo_total_it += abs(pos[fac]-pos[fac_sup])*matriz_trafs[fac][fac_sup] #calcula o custo total
                    
                #atualiza o custo total com o arranjo inferior
                for i in range(num_fac_arranjo_inf):
                    fac_inf = solucao_it[(num_fac-1)-i]
                    
                    custo_total_it += abs(pos[fac]-pos[fac_inf])*matriz_trafs[fac][fac_inf] #calcula o custo total
                
                num_fac_arranjo_inf += 1 #atualiza o número de facilidades no arranjo inferior
                
                solucao_it[num_fac-num_fac_arranjo_inf] = fac #insere na solução (arranjo inferior)
                
                facs_it.remove(fac) #atualiza as facilidades a serem inseridas
            #inserção no arranjo superior
            elif comp_arranjo_sup < comp_arranjo_inf:
                pos[fac] = comp_arranjo_sup+centros[fac] #atualiza a posição da facilidade
                
                comp_arranjo_sup += comps[fac] #atualiza comprimento do arranjo superior
                
                #atualiza o custo total com o arranjo superior
                for i in range(num_fac_arranjo_sup):
                    fac_sup = solucao_it[i]
                    
                    custo_total_it += abs(pos[fac]-pos[fac_sup])*matriz_trafs[fac][fac_sup] #calcula o custo total
                    
                #atualiza o custo total com o arranjo inferior
                for i in range(num_fac_arranjo_inf):
                    fac_inf = solucao_it[(num_fac-1)-i]
                    
                    custo_total_it += abs(pos[fac]-pos[fac_inf])*matriz_trafs[fac][fac_inf] #calcula o custo total
                    
                solucao_it[num_fac_arranjo_sup] = fac #insere na solução (arranjo superior)
                
                num_fac_arranjo_sup += 1 #atualiza o número de facilidades no arranjo superior
                    
                facs_it.remove(fac) #atualiza as facilidades a serem inseridas
            else:
                #simula a inserção em ambos os arranjos
                pos_fac_inf = comp_arranjo_inf+centros[fac] #atualiza a posição da facilidade
                pos_fac_sup = comp_arranjo_sup+centros[fac] #atualiza a posição da facilidade
                
                custo_total_temp_inf = 0
                custo_total_temp_sup = 0

                #simula os custos totais com o arranjo superior
                for i in range(num_fac_arranjo_sup):
                    fac_sup = solucao_it[i]
                    
                    #calcula o custo total em ambos
                    custo_total_temp_inf += abs(pos_fac_inf-pos[fac_sup])*matriz_trafs[fac][fac_sup]
                    custo_total_temp_sup += abs(pos_fac_sup-pos[fac_sup])*matriz_trafs[fac][fac_sup] 
                    
                #simula os custos totais com o arranjo inferior
                for i in range(num_fac_arranjo_inf):
                    fac_inf = solucao_it[(num_fac-1)-i]
                    
                    #calcula o custo total em ambos
                    custo_total_temp_inf += abs(pos_fac_inf-pos[fac_inf])*matriz_trafs[fac][fac_inf]
                    custo_total_temp_sup += abs(pos_fac_sup-pos[fac_inf])*matriz_trafs[fac][fac_inf]
                    
                #inserção no arranjo inferior
                if custo_total_temp_inf < custo_total_temp_sup:
                    pos[fac] = pos_fac_inf #atualiza a posição da facilidade
                
                    comp_arranjo_inf += comps[fac] #atualiza comprimento do arranjo inferior
                    
                    custo_total_it += custo_total_temp_inf
                    
                    num_fac_arranjo_inf += 1 #atualiza o número de facilidades no arranjo inferior
                
                    solucao_it[num_fac-num_fac_arranjo_inf] = fac #insere na solução (arranjo inferior)
                
                    facs_it.remove(fac) #atualiza as facilidades a serem inseridas
                    
                #inserção no arranjo superior
                else:
                    pos[fac] = pos_fac_sup #atualiza a posição da facilidade
                
                    comp_arranjo_sup += comps[fac] #atualiza comprimento do arranjo superior
                    
                    custo_total_it += custo_total_temp_sup
                        
                    solucao_it[num_fac_arranjo_sup] = fac #insere na solução (arranjo superior)
                    
                    num_fac_arranjo_sup += 1 #atualiza o número de facilidades no arranjo superior
                        
                    facs_it.remove(fac) #atualiza as facilidades a serem inseridas

        #fase de busca local
        solucao_it, custo_total_it = vns(solucao_it.copy(), custo_total_it, r_vns, r_vnd, num_fac,
                                         num_fac_arranjo_sup, num_fac_arranjo_inf,
                                         comps, centros, matriz_trafs)
                
        if it == 0:
            custo_total = custo_total_it
            solucao = solucao_it.copy()
        else:
            if custo_total_it <= custo_total:
                custo_total = custo_total_it
                solucao = solucao_it.copy()
            
    return custo_total, solucao, num_fac_arranjo_sup, num_fac_arranjo_inf

#%% INSTÂNCIAS

def leitura(arq):
    num_fac = 0 #número de facilidades
    facs = [] #facilidades
    comps = [] #comprimentos das facilidades
    centros = [] #centros das facilidades
    
    i = 1
    for linha in arq:
        if i == 1:
            num_fac = int(linha.split()[0]) #guarda o número de facilidades
            
            #cria o vetor de facilidades
            for j in range(num_fac):
                facs.append(j)
            
        if i == 2:
            comps_str = linha.split()
            
            #cria os vetores de comprimentos e centros
            for comp in comps_str:
                comps.append(int(comp))
                centros.append(int(comp)/2)
                
            break
                
        i+=1
        
    matriz_trafs = np.zeros((num_fac, num_fac))
    matriz_dec = np.zeros((num_fac, num_fac))
    
    i = 0
    for linha in arq:
        trafs_str = linha.split()
        
        for j in range(num_fac):
            matriz_trafs[i][j] = int(trafs_str[j])
            matriz_dec[i][j] = int(trafs_str[j])/comps[i]
            
        i+=1

    arq.close()
    
    return num_fac, facs, comps, centros, matriz_trafs, matriz_dec

#%% INTERFACE

#instâncias
nomes_inst = []

try:
    arq = open("nomes_instancias.txt", 'r', encoding = "utf8") 
except:
    print("\nArquivo inexistente!")
        
for linha in arq:
    nomes_inst.append(linha.split()[0])
    
arq.close()

custos_totais = []
solucoes = []
nums_facs_arranjos_sups = []
nums_facs_arranjos_infs = []
tempos = []

n = 10 #número de execussões

#execussão do algoritmo para cada instância
for i in range(len(nomes_inst)):
    try:
        arq = open("instancias/" + nomes_inst[i] + ".txt", 'r', encoding = "utf8")
    except:
        print("\nInstância " + nomes_inst[i] + " inexistente.")
        
    num_fac, facs, comps, centros, matriz_trafs, matriz_dec = leitura(arq)
        
    arq.close()
    
    for n_i in range(n):
        #GRASP/VNS(VND)
        alpha = .5
        max_it = 1000
        r_vns = 3
        r_vnd = 1
        
        t_i = time.time()
        custo_total, solucao, num_fac_arranjo_sup, num_fac_arranjo_inf = grasp_vns_vnd(alpha, max_it, r_vns, r_vnd, num_fac, facs, comps, centros, matriz_trafs, matriz_dec)
        t_f = time.time()
    
        custos_totais.append(custo_total)
        solucoes.append(solucao)
        nums_facs_arranjos_sups.append(num_fac_arranjo_sup)
        nums_facs_arranjos_infs.append(num_fac_arranjo_inf)
        tempos.append(t_f-t_i)
        
        print(n_i)
        
    #parâmetros de saída
    custo_media = np.mean(custos_totais)
    custo_min = np.min(custos_totais)

    tempo_min = np.min(tempos)
    
    arg_min = np.argmin(custos_totais)
    
    solucao_min = solucoes[arg_min]
    num_fac_arranjo_sup_min = nums_facs_arranjos_sups[arg_min]
    num_fac_arranjo_inf_min = nums_facs_arranjos_infs[arg_min]