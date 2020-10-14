# -*- coding: utf-8 -*-

"""
Atividade I - Problema da Organização das Salas
Inteligência Computacional - DCC136

Discentes: Davi Rezende
           Gabriel Rezende
           
Docente: Luciana Brugiolo Gonçalvez
"""

#%% BIBLIOTECAS

import matplotlib.pyplot as plt

import numpy as np

from random import seed
from random import choice #seleciona, aleatoriamente, um elemento de uma lista

import time

seed(1)

#%% NÓ

class Sala:
    def __init__(self, id, comprimento):
        self.id = id
        self.comprimento = comprimento
        self.centro = comprimento/2
        self.posicao = 0
        
    def getId(self):
        return self.id
    
    def getComprimento(self):
        return self.comprimento
    
    def getCentro(self):
        return self.centro
    
    def getPosicao(self):
        return self.posicao
    
    def setId(self, id):
        self.id = id
        
    def setComprimento(self, comprimento):
        self.comprimento = comprimento
        
    def setCentro(self, centro):
        self.centro = centro
        
    def setPosicao(self, posicao):
        self.posicao = posicao
        
#%% ARESTA
        
class Trafego:
    def __init__(self, id, sala_A, sala_B, media_trafego):
        self.id = id
        self.sala_A = sala_A
        self.sala_B = sala_B
        self.media_trafego = media_trafego
        
    def getId(self):
        return self.id
    
    def getSala_A(self):
        return self.sala_A
    
    def getSala_B(self):
        return self.sala_B
    
    def getMediaTrafego(self):
        return self.media_trafego
    
    def setId(self, id):
        self.id = id
        
    def setSala_A(self, sala_A):
        self.sala_A = sala_A
        
    def setSala_B(self, sala_B):
        self.sala_B = sala_B
        
    def setMediaTrafego(self, media_trafego):
        self.media_trafego = media_trafego

#%% GRAFO

class Corredor():
    def __init__(self):
        self.salas = []
        self.trafegos = []
        
    def buscarSala(self, id):
        for i in self.salas:
            if id == i.getId():
                return i
            
    def buscarTrafego(self, id):
        for i in self.trafegos:
            if id == i.getId():
                return i
    
    def criarSala(self, id, comprimento):
        if self.buscarSala(id) is None:
            self.salas.append(Sala(id, comprimento))
            
    def criarTrafego(self, id, sala_A, sala_B, media_trafego):
        if self.buscarTrafego(id) is None:
            self.trafegos.append(Trafego(id, sala_A, sala_B, media_trafego))

    def algoritmoConstrutivo(self, rand):
        #comprimento de cada lado do corredor
        comp_lado_cima = 0
        comp_lado_baixo = 0
        
        #custo
        custo_total = 0
        
        #listas de salas de cada lado
        lado_cima = []
        lado_baixo = []
        
        #arestas que serão ordenadas pelo tráfego
        candidatos = self.trafegos.copy()
        candidatos.sort(key = lambda trafego: trafego.media_trafego, reverse = True)
        
#%% PRIMEIRA ITERAÇÃO

        if rand:
            melhores_candidatos = [] #melhores candidatos a entrarem na solução
            
            #escolha dos melhores candidatos
            maior = candidatos[0].getMediaTrafego()
            for i in candidatos:
                if i.getMediaTrafego() == maior:
                    melhores_candidatos.append(i)
            
            if len(melhores_candidatos) == 1: #caso exista apenas um melhor candidato, não há randomização
                aresta = candidatos.pop(0)
            else: #caso exista mais de um melhor candidato, há randomização
                aresta = choice(melhores_candidatos)
                
                candidatos.remove(aresta)
        else:        
            aresta = candidatos.pop(0)
            
        sala_A = aresta.getSala_A()
        sala_B = aresta.getSala_B()
        
        trafego = aresta.getMediaTrafego()
        
        custo_mesmo_lado = ((sala_A.getComprimento() + sala_B.getComprimento())/2)*trafego
        custo_lado_oposto = abs(sala_A.getCentro() - sala_B.getCentro())*trafego
        
        if custo_mesmo_lado < custo_lado_oposto:
            lado_cima.append(sala_A)
            lado_cima.append(sala_B)
            
            sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())

            comp_lado_cima += sala_A.getComprimento()
            
            sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
            
            comp_lado_cima += sala_B.getComprimento()
            
            custo_total += custo_mesmo_lado
        else:
            lado_cima.append(sala_A)
            lado_baixo.append(sala_B)
            
            sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
            sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
            
            comp_lado_cima += sala_A.getComprimento()
            comp_lado_baixo += sala_B.getComprimento()
            
            custo_total += custo_lado_oposto

#%% DEMAIS ITERAÇÕES

        while len(candidatos) != 0:
            if rand:
                melhores_candidatos = [] #melhores candidatos a entrarem na solução
                
                #escolha dos melhores candidatos
                maior = candidatos[0].getMediaTrafego()
                for i in candidatos:
                    if i.getMediaTrafego() == maior:
                        melhores_candidatos.append(i)
                
                if len(melhores_candidatos) == 1: #caso exista apenas um melhor candidato, não há randomização
                    aresta = candidatos.pop(0)
                else: #caso exista mais de um melhor candidato, há randomização
                    aresta = choice(melhores_candidatos)
                    
                    candidatos.remove(aresta)
            else:        
                aresta = candidatos.pop(0)
            
            sala_A = aresta.getSala_A()
            sala_B = aresta.getSala_B()
        
            trafego = aresta.getMediaTrafego()
            
            pertence_A = False
            pertence_B = False
            
            for i in lado_cima:
                if i == sala_A:
                    pertence_A = True

                if i == sala_B:
                    pertence_B = True
                
            for i in lado_baixo:
                if i == sala_A:
                    pertence_A = True
                    
                if i == sala_B:
                    pertence_B = True
            
            #ambas as salas não pertencem à solução
            if pertence_A == False and pertence_B == False:
                #verifica os tráfegos com a sala_A
                traf_sala_A_cima = []
                traf_sala_A_baixo = []
                
                #verifica os tráfegos com a sala_B
                traf_sala_B_cima = []
                traf_sala_B_baixo = []
                
                for i in lado_cima:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            traf_sala_A_cima.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            traf_sala_B_cima.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                            
                for i in lado_baixo:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            traf_sala_A_baixo.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            traf_sala_B_baixo.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                            
                custos_totais_correntes = []
                
                #1ª posição: supondo sala_A e sala_B, nessa ordem, no lado de cima
                custo_temp = custo_total
                
                sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                sala_B.setPosicao(comp_lado_cima + sala_A.getComprimento() + sala_B.getCentro())
                
                for i in range(len(traf_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_cima[i]
                    
                for i in range(len(traf_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_baixo[i]
                    
                for i in range(len(traf_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_cima[i]
                    
                for i in range(len(traf_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao() - sala_B.getPosicao()))*trafego
                
                custos_totais_correntes.append(custo_temp)
                
                #2ª posição: supondo sala_B e sala_A, nessa ordem, no lado de cima
                custo_temp = custo_total
                
                sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                sala_A.setPosicao(comp_lado_cima + sala_B.getComprimento() + sala_A.getCentro())
                
                for i in range(len(traf_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_cima[i]
                    
                for i in range(len(traf_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_baixo[i]
                    
                for i in range(len(traf_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_cima[i]
                    
                for i in range(len(traf_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao() - sala_B.getPosicao()))*trafego
                
                custos_totais_correntes.append(custo_temp)
                
                #3ª posição: supondo sala_A e sala_B, nessa ordem, no lado de baixo
                custo_temp = custo_total
                
                sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                sala_B.setPosicao(comp_lado_baixo + sala_A.getComprimento() + sala_B.getCentro())

                for i in range(len(traf_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_cima[i]
                    
                for i in range(len(traf_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_baixo[i]
                    
                for i in range(len(traf_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_cima[i]
                    
                for i in range(len(traf_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao() - sala_B.getPosicao()))*trafego
                
                custos_totais_correntes.append(custo_temp)
                
                #4ª posição: supondo sala_B e sala_A, nessa ordem, no lado de baixo
                custo_temp = custo_total
                
                sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                sala_A.setPosicao(comp_lado_baixo + sala_B.getComprimento() + sala_A.getCentro())

                for i in range(len(traf_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_cima[i]
                    
                for i in range(len(traf_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_baixo[i]
                    
                for i in range(len(traf_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_cima[i]
                    
                for i in range(len(traf_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao() - sala_B.getPosicao()))*trafego
                
                custos_totais_correntes.append(custo_temp)
                
                #5ª posição: supondo sala_A em cima e sala_B em baixo:
                custo_temp = custo_total
                    
                sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                
                for i in range(len(traf_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_cima[i]
                    
                for i in range(len(traf_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_baixo[i]
                    
                for i in range(len(traf_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_cima[i]
                    
                for i in range(len(traf_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao() - sala_B.getPosicao()))*trafego
                
                custos_totais_correntes.append(custo_temp)
                
                #6ª posição: supondo sala_B em cima e sala_A em baixo:
                custo_temp = custo_total    
                
                sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                
                for i in range(len(traf_sala_A_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_cima[i]
                    
                for i in range(len(traf_sala_A_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*traf_sala_A_baixo[i]
                    
                for i in range(len(traf_sala_B_cima)):
                    custo_temp += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_cima[i]
                    
                for i in range(len(traf_sala_B_baixo)):
                    custo_temp += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*traf_sala_B_baixo[i]
                    
                custo_temp += (abs(sala_A.getPosicao() - sala_B.getPosicao()))*trafego
                
                custos_totais_correntes.append(custo_temp)
                
                #verifica o menor custo
                index = 0
                menor_custo = custos_totais_correntes[0]
                for i in range(len(custos_totais_correntes)):
                    if custos_totais_correntes[i] < menor_custo:
                        menor_custo = custos_totais_correntes[i]
                        
                        index = i
                
                if index == 0: #1º posicionamento
                    sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_cima + sala_A.getComprimento() + sala_B.getCentro())
                
                    comp_lado_cima += sala_A.getComprimento() + sala_B.getComprimento()
                    
                    lado_cima.append(sala_A)
                    lado_cima.append(sala_B)
                    
                    custo_total = custos_totais_correntes[index]
                elif index == 1: #2º posicionamento
                    sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                    sala_A.setPosicao(comp_lado_cima + sala_B.getComprimento() + sala_A.getCentro())
                    
                    comp_lado_cima += sala_B.getComprimento() + sala_A.getComprimento()
                    
                    lado_cima.append(sala_B)
                    lado_cima.append(sala_A)
                    
                    custo_total = custos_totais_correntes[index]
                elif index == 2: #3º posicionamento
                    sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_baixo + sala_A.getComprimento() + sala_B.getCentro())
                    
                    comp_lado_baixo += sala_A.getComprimento() + sala_B.getComprimento()
                    
                    lado_baixo.append(sala_A)
                    lado_baixo.append(sala_B)
                    
                    custo_total = custos_totais_correntes[index]
                elif index == 3: #4º posicionamento
                    sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                    sala_A.setPosicao(comp_lado_baixo + sala_B.getComprimento() + sala_A.getCentro())
                    
                    comp_lado_baixo += sala_B.getComprimento() + sala_A.getComprimento()
                    
                    lado_baixo.append(sala_B)
                    lado_baixo.append(sala_A)
                    
                    custo_total = custos_totais_correntes[index]
                elif index == 4: #5º posicionamento
                    sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                     
                    comp_lado_cima += sala_A.getComprimento()
                    comp_lado_baixo += sala_B.getComprimento()
                     
                    lado_cima.append(sala_A)
                    lado_baixo.append(sala_B)
                    
                    custo_total = custos_totais_correntes[index]
                else: #6º posicionamento
                    sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                    sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                    
                    comp_lado_cima += sala_B.getComprimento()
                    comp_lado_baixo += sala_A.getComprimento()
                    
                    lado_cima.append(sala_B)
                    lado_baixo.append(sala_A)
                    
                    custo_total = custos_totais_correntes[index]

            #sala_B não pertence à solução
            if pertence_A == True and pertence_B == False:
                #verifica os tréfegos com a sala_B
                trafegos_sala_cima = []
                trafegos_sala_baixo = []
                
                for i in lado_cima:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            trafegos_sala_cima.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                            
                for i in lado_baixo:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_B) or (j.getSala_A() == sala_B and j.getSala_B() == i):
                            trafegos_sala_baixo.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                            
                #supondo sala_B em cima
                sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                
                custo_total_corrente_cima = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_total_corrente_cima += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_total_corrente_cima += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*trafegos_sala_baixo[i]
                    
                #supondo sala_B em baixo
                sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                
                custo_total_corrente_baixo = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_total_corrente_baixo += (abs(lado_cima[i].getPosicao() - sala_B.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_total_corrente_baixo += (abs(lado_baixo[i].getPosicao() - sala_B.getPosicao()))*trafegos_sala_baixo[i]
                
                #adicionado a sala_B na solução
                if custo_total_corrente_cima < custo_total_corrente_baixo:
                    lado_cima.append(sala_B)
                    
                    custo_total = custo_total_corrente_cima
                    
                    sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                    
                    comp_lado_cima += sala_B.getComprimento()
                elif custo_total_corrente_baixo < custo_total_corrente_cima:
                    lado_baixo.append(sala_B)
                    
                    custo_total = custo_total_corrente_baixo
                    
                    sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                    
                    comp_lado_baixo += sala_B.getComprimento()
                else:
                    if comp_lado_baixo <= comp_lado_cima:
                        lado_baixo.append(sala_B)
                    
                        custo_total = custo_total_corrente_baixo
                    
                        sala_B.setPosicao(comp_lado_baixo + sala_B.getCentro())
                    
                        comp_lado_baixo += sala_B.getComprimento()
                    else:
                        lado_cima.append(sala_B)
                    
                        custo_total = custo_total_corrente_cima
                    
                        sala_B.setPosicao(comp_lado_cima + sala_B.getCentro())
                        
                        comp_lado_cima += sala_B.getComprimento()
                        
            #sala_A não pertence à solução
            if pertence_A == False and pertence_B == True:
                #verifica os trafegos com a sala_A
                trafegos_sala_cima = []
                trafegos_sala_baixo = []
                
                for i in lado_cima:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            trafegos_sala_cima.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                            
                for i in lado_baixo:
                    for j in candidatos:
                        if (j.getSala_A() == i and j.getSala_B() == sala_A) or (j.getSala_A() == sala_A and j.getSala_B() == i):
                            trafegos_sala_baixo.append(j.getMediaTrafego())
                            
                            candidatos.remove(j)
                            
                #supondo sala_A em cima
                sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                
                custo_total_corrente_cima = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_total_corrente_cima += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_total_corrente_cima += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*trafegos_sala_baixo[i]
                    
                #supondo sala_A em baixo
                sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                
                custo_total_corrente_baixo = custo_total
                
                for i in range(len(trafegos_sala_cima)):
                    custo_total_corrente_baixo += (abs(lado_cima[i].getPosicao() - sala_A.getPosicao()))*trafegos_sala_cima[i]
                    
                for i in range(len(trafegos_sala_baixo)):
                    custo_total_corrente_baixo += (abs(lado_baixo[i].getPosicao() - sala_A.getPosicao()))*trafegos_sala_baixo[i]
                
                #adicionado a sala_A na solução
                if custo_total_corrente_cima < custo_total_corrente_baixo:
                    lado_cima.append(sala_A)
                    
                    custo_total = custo_total_corrente_cima
                    
                    sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                    
                    comp_lado_cima += sala_A.getComprimento()
                elif custo_total_corrente_baixo <  custo_total_corrente_cima:
                    lado_baixo.append(sala_A)
                    
                    custo_total = custo_total_corrente_baixo
                    
                    sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                    
                    comp_lado_baixo += sala_A.getComprimento()
                else:
                    if comp_lado_baixo <= comp_lado_cima:
                        lado_baixo.append(sala_A)
                    
                        custo_total = custo_total_corrente_baixo
                    
                        sala_A.setPosicao(comp_lado_baixo + sala_A.getCentro())
                    
                        comp_lado_baixo += sala_A.getComprimento()
                    else:
                        lado_cima.append(sala_A)
                    
                        custo_total = custo_total_corrente_cima
                    
                        sala_A.setPosicao(comp_lado_cima + sala_A.getCentro())
                        
                        comp_lado_cima += sala_A.getComprimento()
        
        return lado_cima, lado_baixo, custo_total
    
    def recalculaCusto(self, lado_cima, lado_baixo):
        comp_lado_cima = 0
        comp_lado_baixo = 0
        
        custo_temp = 0

        ts = self.trafegos.copy()

        for i in lado_cima:
            i.setPosicao(comp_lado_cima + i.getCentro())
            
            comp_lado_cima += i.getComprimento()
        for i in lado_baixo:
            i.setPosicao(comp_lado_baixo + i.getCentro())
            
            comp_lado_baixo += i.getComprimento()
        
        #atualiza custo lado_cima com lado_cima
        for i in range(len(lado_cima)):
            n = i+1
            while n < len(lado_cima):
                for t in ts:
                    if(t.getSala_A() == lado_cima[i] and t.getSala_B() == lado_cima[n]) or (t.getSala_A() == lado_cima[n] and t.getSala_B() == lado_cima[i]):
                        custo_temp += abs(lado_cima[i].getPosicao() - lado_cima[n].getPosicao())*t.getMediaTrafego()
                        
                        ts.remove(t)
                        
                        break
                        
                n += 1
            
            #atualiza custo lado_cima com lado_baixo
            for j in range(len(lado_baixo)):
                for t in ts:
                    if(t.getSala_A() == lado_cima[i] and t.getSala_B() == lado_baixo[j]) or (t.getSala_A() == lado_baixo[j] and t.getSala_B() == lado_cima[i]):
                        custo_temp += abs(lado_cima[i].getPosicao() - lado_baixo[j].getPosicao())*t.getMediaTrafego()
                        
                        ts.remove(t)
                        
                        break
        
        #atualiza custo lado_baixo com lado_baixo
        for i in range(len(lado_baixo)):
            n = i+1
            while n < len(lado_baixo):
                for t in ts:
                    if(t.getSala_A() == lado_baixo[i] and t.getSala_B() == lado_baixo[n]) or (t.getSala_A() == lado_baixo[n] and t.getSala_B() == lado_baixo[i]):
                        custo_temp += abs(lado_baixo[i].getPosicao() - lado_baixo[n].getPosicao())*t.getMediaTrafego()
                        
                        ts.remove(t)
                        
                        break
                
                n += 1
                
        return custo_temp
    
    def buscaLocal(self, lado_cima, lado_baixo, custo_total):
        for i in range(len(lado_cima)):
            #movimento: lado_cima com lado_cima
            n = i+1
            while n < (len(lado_cima)):
                sala_n = lado_cima[n]
                
                lado_cima[n] = lado_cima[i]
                lado_cima[i] = sala_n
                
                custo_temp = self.recalculaCusto(lado_cima, lado_baixo)
            
                if custo_temp < custo_total:
                    custo_total = custo_temp
                else:
                    sala_n = lado_cima[n]
                
                    lado_cima[n] = lado_cima[i]
                    lado_cima[i] = sala_n
                
                n += 1
                
            for j in range(len(lado_baixo)):
                #movimento: lado_cima com lado_baixo
                sala_j = lado_baixo[j]
                
                lado_baixo[j] = lado_cima[i]
                lado_cima[i] = sala_j
                
                custo_temp = self.recalculaCusto(lado_cima, lado_baixo)
                
                if custo_temp < custo_total:
                    custo_total = custo_temp
                    
                    
                else:
                    sala_j = lado_baixo[j]
                
                    lado_baixo[j] = lado_cima[i]
                    lado_cima[i] = sala_j
                    
        #movimento: lado_baixo com lado_baixo
        for i in range(len(lado_baixo)):           
            n = i+1
            while n < (len(lado_baixo)):
                sala_n = lado_baixo[n]
                
                lado_baixo[n] = lado_baixo[i]
                lado_baixo[i] = sala_n
                
                custo_temp = self.recalculaCusto(lado_cima, lado_baixo)
                
                if custo_temp < custo_total:
                    custo_total = custo_temp
                else:
                    sala_n = lado_baixo[n]
                
                    lado_baixo[n] = lado_baixo[i]
                    lado_baixo[i] = sala_n
                    
                n += 1
                
        return custo_total
            
#%% LEITURA DAS INSTÂNCIAS
            
def leitura(nome_arquivo, corredor):
    num_salas = 0
    
    i = 1
    for linha in arquivo:
        if i == 1:
            salas = linha.split()
            num_salas = int(salas[0]) #guarda o número de salas
            
        if i == 2:
            comprimentos = linha.split()
            
            for j in range(num_salas):
                corredor.criarSala(j+1, int(comprimentos[j])) #cria os nós
                
            break
                
        i+=1
        
    matriz_trafegos = np.zeros((num_salas, num_salas))
    
    i = 0
    for linha in arquivo:
        trafegos = linha.split()
        
        for j in range(num_salas):
            matriz_trafegos[i][j] = int(trafegos[j])
            
        i+=1

    id = 1
    for i in range(num_salas):        
        for j in range(num_salas):
            if i > j:
                corredor.criarTrafego(id, corredor.buscarSala(i+1), corredor.buscarSala(j+1), int(matriz_trafegos[i][j])) #cria as aresta
            
                id+=1
                    
                        
    arquivo.close()
    
    return True

#%% ESCRITA E IMPRESSÃO DOS RESULTADOS

def impressaoAlgConstr(ns, custos_constr, custos_bl, ts_constr, ts_bl, ts_total):
    #comparação entre os tempos de execução do algoritmo construtivo e a busca local
    plt.figure(figsize = (20, 10))
    
    for i in range(2):
        if i == 0:
            plt.subplot(1, 2, i+1)
            plt.subplots_adjust(wspace = 0.4)
            
            plt.plot(ns, ts_constr, marker = "o", color = "red", label = "ts_constr")
            plt.plot(ns, ts_bl, marker = "o", color = "green", label = "ts_bl")
            plt.xlabel("Nº de salas")
            plt.ylabel("t(s)")
            plt.grid(True)
            plt.legend(loc = "best")
        else:
            plt.subplot(1, 2, i+1)
            
            plt.plot(ns, ts_total, marker = "o", color = "blue", label = "ts_total")
            plt.xlabel("Nº de salas")
            plt.ylabel("t(s)")
            plt.grid(True)
            plt.legend(loc = "best")
            
    plt.suptitle("Tempos de execução")
    plt.show()
    
    #comparação entre os custos do algoritmo construtivo e a busca local
    plt.figure(figsize = (20, 10))
    
    plt.plot(ns, custos_constr, marker = "o", color = "red", label = "custos_constr")
    plt.plot(ns, custos_bl, marker = "o", color = "green", label = "custos_bl")
    plt.xlabel("Nº de salas")
    plt.ylabel("Custo")
    plt.grid(True)
    plt.legend(loc = "best")
    plt.title("Custos")
    plt.show()
    
def impressaoAlgConstrRand(ns, custos_constr_media, custos_bl_media, custos_constr_min, custos_bl_min, ts_constr_media, ts_bl_media, ts_total_media):
    #comparação entre os tempos de execução do algoritmo construtivo e a busca local
    plt.figure(figsize = (20, 10))
    
    for i in range(2):
        if i == 0:
            plt.subplot(1, 2, i+1)
            plt.subplots_adjust(wspace = 0.4)
            
            plt.plot(ns, ts_constr_media, marker = "o", color = "red", label = "ts_constr_media")
            plt.plot(ns, ts_bl_media, marker = "o", color = "green", label = "ts_bl_media")
            plt.xlabel("Nº de salas")
            plt.ylabel("t(s)")
            plt.grid(True)
            plt.legend(loc = "best")
        else:
            plt.subplot(1, 2, i+1)
            
            plt.plot(ns, ts_total_media, marker = "o", color = "blue", label = "ts_total_media")
            plt.xlabel("Nº de salas")
            plt.ylabel("t(s)")
            plt.grid(True)
            plt.legend(loc = "best")
            
    plt.suptitle("Tempos de execução")
    plt.show()
    
    #comparação entre os custos (média e mínimo) do algoritmo construtivo e a busca local
    plt.figure(figsize = (20, 10))
    
    for i in range(2):
        if i == 0:
            plt.subplot(1, 2, i+1)
            plt.subplots_adjust(wspace = 0.4)
            
            plt.plot(ns, custos_constr_media, marker = "o", color = "red", label = "custos_constr_media")
            plt.plot(ns, custos_bl_media, marker = "o", color = "green", label = "custos_bl_media")
            plt.xlabel("Nº de salas")
            plt.ylabel("Custos")
            plt.grid(True)
            plt.legend(loc = "best")
        else:
            plt.subplot(1, 2, i+1)
            
            plt.plot(ns, custos_constr_min, marker = "o", color = "blue", label = "custos_constr_min")
            plt.plot(ns, custos_bl_min, marker = "o", color = "yellow", label = "custos_bl_min")
            plt.xlabel("Nº de salas")
            plt.ylabel("Custos")
            plt.grid(True)
            plt.legend(loc = "best")
            
    plt.suptitle("Custos (média e mínimo)")
    plt.show()

def escritaAlgConstr(num_insts, nomes_arq, ns, custos_constr, custos_bl, ts_constr, ts_bl, ts_total):
    sucesso = True
    try:
        arq = open("resultados_algoritmo_construtivo.txt", "w")
    except:
        print("Arquivo de escrita não encontrado.")
        
        sucesso = False
        
    if sucesso:
        arq.write("instância, n, custo_constr, custo_bl, t_constr, t_bl, t_toal\n")
        
        for i in range(num_insts):    
            arq.write(nomes_arq[i] + ", " + ns[i] + ", " +
                      str(custos_constr[i]) + ", " + str(custos_bl[i]) + ", " + 
                      str(round(ts_constr[i], 3)) + ", " + str(round(ts_bl[i], 3)) + ", " + str(round(ts_total[i], 3)) + "\n")
            
    impressaoAlgConstr(ns, custos_constr, custos_bl, ts_constr, ts_bl, ts_total)
    
    arq.close()
    
def escritaAlgConstrRand(num_insts, nomes_arq, ns, custos_constr_media, custos_bl_media, custos_constr_min, custos_bl_min, ts_constr_media, ts_bl_media, ts_total_media):
    sucesso = True
    try:
        arq = open("resultados_algoritmo_construtivo_randomizado.txt", "w")
    except:
        print("Arquivo de escrita não encontrado.")
        
        sucesso = False
        
    if sucesso:
        arq.write("instância, n, custo_constr_media, custo_bl_media, custo_constr_min, custo_bl_min, t_constr_media, t_bl_media, t_toal_media\n")
        
        for i in range(num_insts):
            arq.write(nomes_arq[i] + ", " + ns[i] + ", " + 
                      str(custos_constr_media[i]) + ", " + str(custos_bl_media[i]) + ", " + str(custos_constr_min[i]) + ", " + str(custos_bl_min[i]) + ", " + 
                      str(round(ts_constr_media[i], 3)) + ", " + str(round(ts_bl_media[i], 3)) + ", " + str(round(ts_total_media[i], 3)) + "\n")
            
    impressaoAlgConstrRand(ns, custos_constr_media, custos_bl_media, custos_constr_min, custos_bl_min, ts_constr_media, ts_bl_media, ts_total_media)
    
    arq.close()
        
#%% INSTÂNCIAS
    
nomes_arq = ["S10", "S11",
             "sko42_01_n", "sko42_02_n", "sko42_03_n", "sko42_04_n", "sko42_05_n",
             "sko49_01_n", "sko49_02_n", "sko49_03_n", "sko49_04_n", "sko49_05_n",
             "sko56_01_n", "sko56_02_n", "sko56_03_n", "sko56_04_n", "sko56_05_n"]

ns = ["10", "11",
      "42_1", "42_2", "42_3", "42_4", "42_5",
      "49_1", "49_2", "49_3", "49_4", "49_5",
      "56_1", "56_2", "56_3", "56_4", "56_5"]

num_insts = len(nomes_arq)

#%% INTERFACE

print("*INTELIGÊNCIA COMPUTACIONAL - PROBLEMA DA ORGANIZAÇÃO DAS SALAS*")

opcao_analise = ""
while opcao_analise != str(3):
    print("\nOPÇÕES DE ANÁLISE:")
    print("(1) ALGORITMO CONSTRUTIVO")
    print("(2) ALGORITMO CONSTRUTIVO RANDOMIZADO")
    print("(3) SAIR")

    teste = True
    while teste:
        opcao_analise = input("Opção: ")
        
        if opcao_analise != "1" and opcao_analise != "2" and opcao_analise != "3":
            print("Digite (1/2/3).")
        else:
            teste = False

    if opcao_analise == "1":
        ts_constr = [] #tempo de execução, de cada instância, do algoritmo construtivo
        ts_bl = [] #tempo de execução, de cada instância, da busca local
        ts_total = [] #soma, de cada instância, dos tempos anteriores
        custos_constr = [] #custo, de cada instância, do algoritmo construtivo
        custos_bl = [] #custo, de cada instância, da busca local
        
        #disposição, de cada instância, da solução do algoritmo construtivo
        disps_cima_constr = []
        disps_baixo_constr = []
        
        #disposição, de cada instância, da solução da busca local
        disps_cima_bl = []
        disps_baixo_bl = []
 
        for i in range(num_insts):
            arquivo_aberto = False
            while arquivo_aberto == False:
                try:
                    arquivo = open("insts/" + nomes_arq[i] + ".txt", 'r', encoding = "utf8")
                    
                    arquivo_aberto = True
                except:
                    print("\nArquivo '" + nomes_arq[i] + "' inexistente!")
                    
                    nomes_arq.remove(nomes_arq[i])
                    ns.remove(ns[i])
                    
                    num_insts -= 1
            
            #instancia a estrutura de grafo
            corredor = Corredor()
            
            if leitura(nomes_arq[i], corredor) == False:
                print("\nErro na leitura do arquivo! Verifique o arquivo de entrada.")
            else:
                print("\nInstância '" + nomes_arq[i] + "' algoritmo construtivo...")
                #execução do algoritmo construtivo
                t_i = time.time()
                lado_cima, lado_baixo, custo_constr = corredor.algoritmoConstrutivo(False)
                t_f = time.time()
                print("Concluído!")
                
                t_constr = t_f-t_i
                
                solucao_cima_constr = []
                solucao_baixo_constr = []
                
                for j in lado_cima:
                    solucao_cima_constr.append(j.getId())
                    
                for j in lado_baixo:
                    solucao_baixo_constr.append(j.getId())
                
                disps_cima_constr.append(solucao_cima_constr)
                disps_baixo_constr.append(solucao_baixo_constr)
                
                print("\nInstância '" + nomes_arq[i] + "' busca local...")
                #execução da busca local
                t_i = time.time()
                custo_bl = corredor.buscaLocal(lado_cima, lado_baixo, custo_constr)
                t_f = time.time()
                print("Concluído!")
                
                t_bl = t_f-t_i
                
                solucao_cima_bl = []
                solucao_baixo_bl = []
                
                for j in lado_cima:
                    solucao_cima_bl.append(j.getId())
                    
                for j in lado_baixo:
                    solucao_baixo_bl.append(j.getId())
                
                disps_cima_bl.append(solucao_cima_bl)
                disps_baixo_bl.append(solucao_baixo_bl)
                
                t_total = t_constr + t_bl    
                
                custos_constr.append(custo_constr)
                custos_bl.append(custo_bl)
                ts_constr.append(t_constr)
                ts_bl.append(t_bl)
                ts_total.append(t_total)
                
            arquivo.close()

        escritaAlgConstr(num_insts, nomes_arq, ns, custos_constr, custos_bl, ts_constr, ts_bl, ts_total)

    elif opcao_analise == "2":
        ts_constr_media = [] #média dos tempos de execução, de cada instância, do algoritmo construtivo randomizado
        ts_bl_media = [] #média dos tempos de execução, de cada instância, da busca local
        ts_total_media = [] #média das somas dos tempos de execução, de cada instância
        
        custos_constr_media = [] #média dos custos, de cada instância, do algoritmo construtivo randomizado
        custos_bl_media = [] #média dos custos, de cada instância, da busca local
        
        custos_constr_min = [] #custo mínimo, de cada instância, do algoritmo construtivo randomizado
        custos_bl_min = [] #custo mínimo, de cada instância, da busca local
        
        #melhor disposição, de cada instância, da solução do algoritmo construtivo randomizado
        disps_cima_constr = []
        disps_baixo_constr = []
        
        #melhor disposição, de cada instância, da solução da busca local
        disps_cima_bl = []
        disps_baixo_bl = []
        
        num_rep = int(input("Número de repetições: "))
        
        for i in range(num_insts):
            arquivo_aberto = False
            while arquivo_aberto == False:
                try:
                    arquivo = open("insts/" + nomes_arq[i] + ".txt", 'r', encoding = "utf8")
                    
                    arquivo_aberto = True
                except:
                    print("\nArquivo '" + nomes_arq[i] + "' inexistente!")
                    
                    nomes_arq.remove(nomes_arq[i])
                    ns.remove(ns[i])
                    
                    num_insts -= 1
            
            #instancia a estrutura de grafo
            corredor = Corredor()
            
            if leitura(nomes_arq[i], corredor) == False:
                print("\nErro na leitura do arquivo! Verifique o arquivo de entrada.")
            else:
                ts_constr = [] #tempos de execução, de cada iteração, do algoritmo construtivo randomizado
                ts_bl = [] #tempo de execução, de cada iteração, da busca local
                ts_total = [] #somas, de cada iteração, dos tempos anteriores
                custos_constr = [] #custos, de cada iteração, do algoritmo construtivo randomizado
                custos_bl = [] #custos, de cada iteração, da busca local
                
                #soluções, de cada iteração, do algoritmo construtivo randomizado
                solucoes_cima_constr = []
                solucoes_baixo_constr = []
                
                #soluções, de cada iteração, da busca local
                solucoes_cima_bl = []
                solucoes_baixo_bl = []
                
                for j in range(num_rep):
                    print("\nInstância '" + nomes_arq[i] + "' | iteração '" + str(j+1) + "' algoritmo construtivo randomizado...")
                    #execução do algoritmo construtivo
                    t_i = time.time()
                    lado_cima_j, lado_baixo_j, custo_constr_j = corredor.algoritmoConstrutivo(True)
                    t_f = time.time()
                    print("Concluído!")
                    
                    ts_constr.append(t_f-t_i)
                    
                    solucao_cima_constr = []
                    solucao_baixo_constr = []
                
                    for k in lado_cima_j:
                        solucao_cima_constr.append(k.getId())
                    
                    for k in lado_baixo_j:
                        solucao_baixo_constr.append(k.getId())
                        
                    solucoes_cima_constr.append(solucao_cima_constr)
                    solucoes_baixo_constr.append(solucoes_baixo_constr)
                    
                    print("\nInstância '" + nomes_arq[i] + "' | iteração '" + str(j+1) + "' busca local...")
                    #execução da busca local
                    t_i = time.time()
                    custo_bl_j = corredor.buscaLocal(lado_cima_j, lado_baixo_j, custo_constr_j)
                    t_f = time.time()
                    print("Concluído!")
                    
                    ts_bl.append(t_f-t_i)
                    
                    solucao_cima_bl = []
                    solucao_baixo_bl = []
                
                    for k in lado_cima_j:
                        solucao_cima_bl.append(k.getId())
                    
                    for k in lado_baixo_j:
                        solucao_baixo_bl.append(k.getId())
                    
                    solucoes_cima_bl.append(solucao_cima_bl)
                    solucoes_baixo_bl.append(solucao_baixo_bl)
                    
                    ts_total.append(ts_bl[j]+ts_constr[j])
                    
                    custos_constr.append(custo_constr_j)
                    custos_bl.append(custo_bl_j)
                
                #calcula média dos custos
                custos_constr_media.append(np.mean(custos_constr))
                custos_bl_media.append(np.mean(custos_bl))
                
                #calcula o custo mínimo
                custos_constr_min.append(np.min(custos_constr))
                custos_bl_min.append(np.min(custos_bl))
                
                j_constr = np.argmin(custos_constr)
                j_bl = np.argmin(custos_bl)
                
                disps_cima_constr.append(solucoes_cima_constr[j_constr])
                disps_baixo_constr.append(solucoes_baixo_constr[j_constr])
                
                disps_cima_bl.append(solucoes_cima_bl[j_bl])
                disps_baixo_bl.append(solucoes_baixo_bl[j_bl])
                
                #calcula a média dos tempos
                ts_constr_media.append(np.mean(ts_constr))
                ts_bl_media.append(np.mean(ts_bl))
                ts_total_media.append(np.mean(ts_total))
                
            arquivo.close()
        
        escritaAlgConstrRand(num_insts, nomes_arq, ns,
                             custos_constr_media, custos_bl_media, custos_constr_min, custos_bl_min,
                             ts_constr_media, ts_bl_media, ts_total_media)
    else:
        print("\nEncerrando aplicação...")