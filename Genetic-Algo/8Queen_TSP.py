

import sys
sys.setrecursionlimit(10**8)
from collections import defaultdict
import matplotlib.pyplot as plt
import bisect
import random
import copy


# Question 1 


class Eight_Queen_Problem:
    def __init__(self):
        self.grid_size = 8             # Grid Size can be changed Here !! 
        self.population_size = 50    # Population Size can be changed Here !!
        self.best_fitness = 0
        self.generation_count = 1
        # self.repeatCount = 0
        # self.repeatCount1 = 0
        self.generation_fitness = []
        self.ini_population = self.genereate_initial_population()
        self.genetic_algorithm(self.ini_population)

        

    
    def genetic_algorithm(self,population):
        while(True):
            new_population = []
            fitness_of_new_pop = 0
            current_population = population
            for iter in range(len(current_population)):
                parents = self.get_parent(current_population)
                child = self.get_child(parents)
                probability_to_mutate = random.randint(1,100)
                if(probability_to_mutate < 70 or self.best_fitness==28):
                    child = self.mutate_child(child)
                child_fitness = self.get_Fitness(child)
                fitness_of_new_pop = max(fitness_of_new_pop,child_fitness)
                new_population.append(child)
            self.generation_fitness.append(fitness_of_new_pop)
            if(fitness_of_new_pop > self.best_fitness): self.best_fitness = fitness_of_new_pop
            if(self.best_fitness == 29):
                print() ; print()
                print("Found Maximum Fitness !!") ; print()
                print("Generation",self.generation_count,"=>",fitness_of_new_pop) ; self.generation_count+=1
                print(); print()
                x = [i for i in range(1,self.generation_count)]
                y = self.generation_fitness
                plt.plot(x,y)
                plt.xlabel("Generations")
                plt.ylabel("Fitness")
                plt.title("Improved Algorithm !")
                plt.show()
                return
            else:
                print("Generation",self.generation_count,"=>",fitness_of_new_pop) ; 
                self.generation_count+=1
                population = new_population
        
    
    def mutate_child(self,child):
        bestchild = child
        bestFitness = self.get_Fitness(child)
        neighbours = []
        for index in range(self.grid_size):
            for row in range(1,self.grid_size+1):
                tempChild = child[::]
                tempChild[index] = row
                neighbours.append(tempChild)
                fitness = self.get_Fitness(tempChild)
                if(fitness > bestFitness):
                    bestFitness = fitness
                    bestchild = tempChild

        # for index1 in range(self.grid_size):
        #     for index2 in range(self.grid_size):
        #         tempChild = child[::]
        #         tempChild[index1] = child[index2]
        #         tempChild[index2] = child[index1]
        #         neighbours.append(tempChild)
        #         fitness = self.get_Fitness(tempChild)
        #         if(fitness > bestFitness):
        #             bestFitness = fitness
        #             bestchild = tempChild
        # parents = self.get_parent(neighbours)
        # bestchild = parents[0]
        if(bestchild == child):
            # if(self.generation_count%2==0):
                # random.seed(69)
            index1 = random.randint(0,self.grid_size-1)
            index2 = random.randint(0,self.grid_size-1)
            bestchild[index1] = random.randint(1,self.grid_size) 
            bestchild[index2] = random.randint(1,self.grid_size)
        return bestchild

    def get_child(self,parents):
        bestchild = [] ; parent1 = parents[0] ; parent2 = parents[1]
        bestFitness = 0
        neighbours = []
        for index in range(0,self.grid_size):
            child= parent1[0:index]
            child+=parent2[index::]
            neighbours.append(child)
            fitness = self.get_Fitness(child)
            if(fitness > bestFitness): bestchild = child ; bestFitness = fitness
        # bestchild = self.get_parent(neighbours)[0]
        if(bestchild == parent1 or bestchild == parent2):
            index = random.randint(0,self.grid_size-1)
            bestchild = parent1[:index] + parent2[index::]
            

        # if(self.get_Fitness(bestchild) == self.best_fitness):
        #     self.repeatCount1+=1
        # if(self.repeatCount1 >=1):
        #     index = random.randint(0,self.grid_size-1)
        #     bestchild = parent1[:index] + parent2[index::]

        return bestchild
        

    def get_parent(self,population):
        fitness_Arr = list(map(lambda x: self.get_Fitness(x), population))
        probability_Arr = list(map(lambda x: x/29 , fitness_Arr))
        freq_Arr = list(map(lambda x: int(x*100) , probability_Arr))
        total_Numbers = sum(freq_Arr)
        index1 = random.randint(0,total_Numbers-1)
        index2 = random.randint(0,total_Numbers-1)
        while(index2==index1): index2 = random.randint(0,total_Numbers-1)
        freq_Arr_prefixsum = [freq_Arr[0]]*(len(freq_Arr))
        for i in range(1,len(freq_Arr)):
            freq_Arr_prefixsum[i] = freq_Arr_prefixsum[i-1] + freq_Arr[i]
        parent1 = population[bisect.bisect_left(freq_Arr_prefixsum,index1,0,len(freq_Arr_prefixsum))]
        parent2 = population[bisect.bisect_left(freq_Arr_prefixsum,index2,0,len(freq_Arr_prefixsum))]
        return [parent1,parent2]
        


    def genereate_initial_population(self):
        state = [1 for i in range(self.grid_size)]
        population = [state for i in range(self.grid_size)]
        return population


    def get_Fitness(self,state):

        """
            Fitness -> 1 + Number of Queens in Non Attacking Position
            Maximum Fitness -> When All queens are safe from each other
            We have 8 Queens -> Each Queen is safe from 7 Queens -> 
            Therefore (8*7)/2 States where Fitness is max (A -> B & B -> A are treated Same)
            Max Fitness = 1 + (8*7)/2 = 29

            State contains -> 3,2,1 Here 1st Col contains Queen at 3rd Row
            Total Collisions = (Row_Collides) + (Col_Collides) + (Left_Diag_Collides) + (Right_Diag_Collides)
            Fitness = 29 - Total Collisions
        """
        Row_Collides = 0 ; Col_Collides = 0 ; Left_Diag_Collides = 0 ; Right_Diag_Collides = 0

        # Making Grid

        n = len(state)
        grid = [ [0 for i in range(n)] for j in range(n) ]
        col = 1
        for row in state:
            grid[row-1][col-1] = 1
            col+=1 

        # Calculating Row Collides 

        for row in range(n):
            collisions = 0
            for col in range(n):
                if(grid[row][col] == 1): collisions+=1
            Row_Collides+= (collisions*(collisions-1))//2
        

        # Calculating Left_Diag_Collides
        for start in range(1,n):
            row = start ; col = 0 ; collisions = 0
            while(row>=0):
                if(grid[row][col] == 1): collisions+=1
                col+=1; row-=1
            Left_Diag_Collides+= (collisions*(collisions-1))//2
        
        for start in range(n-2,0,-1):
            row = start; col = n-1 ; collisions = 0
            while(row<=n-1):
                if(grid[row][col] == 1): collisions+=1
                col-=1; row+=1
            Left_Diag_Collides+= (collisions*(collisions-1))//2

        
        # Calculating Right_Diag_Collides
        for start in range(n-2,-1,-1):
            row = start ; col = 0 ; collisions = 0
            while(row<=n-1):
                if(grid[row][col] == 1): collisions+=1
                col+=1; row+=1
            Right_Diag_Collides+= (collisions*(collisions-1))//2
        
        for start in range(1,n-1):
            row = start ; col = n-1 ; collisions = 0
            while(row>=0):
                if(grid[row][col] == 1): collisions+=1
                col-=1; row-=1
            Right_Diag_Collides+= (collisions*(collisions-1))//2
        
        return 29-(Row_Collides + Col_Collides + Left_Diag_Collides + Right_Diag_Collides)
        


    

# Question 2


class Travelling_Salesmen_Problem:
    def __init__(self):
        self.population_size = 20
        self.generations = 0
        self.generation_fitness = []
        self.repeatCOUNT = 0
        self.bestchild = ['-1' for i in range(self.population_size)]
        self.bestFITNESS = -1
        self.cityGrid = self.get_city_grid()
        self.INIpopulation = self.genereate_initial_population()
        self.genetic_algorithm()

    def genereate_initial_population(self):
        state = []
        for i in range(65,79):
            state.append(chr(i))
        return [state for i in range(self.population_size)]

    def shuffle_population(self,population):
        newPop = copy.deepcopy(population)
        for child in newPop:
            random.shuffle(child)
        return newPop



    def get_city_grid(self):
        inf = 1e3
        grid_size = 14
        grid = [[inf for i in range(14)] for j in range(14)]
        # As per Given Distances in the Question Changing Indices
        grid[0][0]=0;grid[0][6]=0.15;grid[0][9]=0.2;grid[0][11]=0.12
        grid[1][1]=0;grid[1][7]=0.19;grid[1][8]=0.4;grid[1][-1]=0.13
        grid[2][2]=0;grid[2][3]=0.6;grid[2][4]=0.22;grid[2][5]=0.4;grid[2][8]=0.2
        grid[3][2]=0.6;grid[3][3]=0;grid[3][5]=0.21;grid[3][10]=0.3
        grid[4][2]=0.22;grid[4][4]=0;grid[4][8]=0.18
        grid[5][2]=0.4;grid[5][3]=0.21;grid[5][5]=0;grid[5][10]=0.37;grid[5][11]=0.6;grid[5][12]=0.26;grid[5][13]=0.9
        grid[6][0]=0.15;grid[6][6]=0;grid[6][10]=0.55;grid[6][11]=0.18
        grid[7][1]=0.19;grid[7][7]=0;grid[7][9]=0.56;grid[7][13]=0.17
        grid[8][1]=0.4;grid[8][2]=0.2;grid[8][4]=0.18;grid[8][8]=0;grid[8][13]=0.6
        grid[9][0]=0.2;grid[9][7]=0.56;grid[9][9]=0;grid[9][11]=0.16;grid[9][13]=0.5
        grid[10][3]=0.3;grid[10][5]=0.37;grid[10][6]=0.55;grid[10][10]=0;grid[10][12]=0.24
        grid[11][0]=0.12;grid[11][5]=0.6;grid[11][6]=0.18;grid[11][9]=0.16;grid[11][11]=0;grid[11][12]=0.4
        grid[12][5]=0.26;grid[12][10]=0.24;grid[12][11]=0.4;grid[12][12]=0
        grid[13][1]=0.13;grid[13][5]=0.9;grid[13][7]=0.17;grid[13][8]=0.6;grid[13][9]=0.5;grid[13][13]=0
        return grid

    def get_Fitness(self,state):
        dist = 0
        for iter in range(0,len(state)-1):
            dist+=self.cityGrid[ord(state[iter])-65][ord(state[iter+1])-65]
        dist+=self.cityGrid[ord(state[-1])-65][ord(state[0])-65]
        return 1/dist


    def get_parent(self,population):
        fitness = list(map(lambda x : self.get_Fitness(x),population))
        TotalFitness = sum(fitness)
        probability_Arr = [i/TotalFitness for i in fitness]
        parents = []
        parents.append(random.choices(population,weights = probability_Arr)[0])
        parents.append(random.choices(population,weights = probability_Arr)[0])
        return parents

    def child_generate(self,parents,index,length):
        parent1 = parents[0] ; parent2 = parents[1]
        parent1PART = parent1[index:index+length]
        child = [None for i in range(len(parent1))]
        child[index:index+length] = parent1PART[::]
        for city in parent2:
            if(city not in parent1PART):
                for check in range(len(child)):
                    if(child[check]==None):
                        child[check] = city
                        break
        return child
    
    def get_child(self,parents):
        parent1 = parents[0]
        bestCHILD = parent1[::]
        bestFITNESS = self.get_Fitness(bestCHILD)
        # HILL CLIMB 
        for index in range(len(parent1)):
            for length in range(len(parent1)-index-1):
                child = self.child_generate(parents[::],index,length)
                child_fitness = self.get_Fitness(child[::])
                if(child_fitness >= bestFITNESS):
                    bestCHILD = child[::]
                    bestFITNESS = child_fitness
        if(bestCHILD == parents[0] or abs(bestFITNESS - self.get_Fitness(parent1)<0.1)):
            index = random.randint(0,len(parent1)-1)
            length = random.randint(0,len(parent1)-index-1)
            bestCHILD = self.child_generate(parents[::],index,length)
        return bestCHILD

    def mutate_child(self,child):
        baseCHILD = child[::]
        bestCHILD = child[::]
        bestFITNESS = self.get_Fitness(bestCHILD)

        for index1 in range(len(child)-1):
            for index2 in range(index1+1,len(child)):
                tempCHILD = baseCHILD[::]
                tempCHILD[index1],tempCHILD[index2] = tempCHILD[index2],tempCHILD[index1]
                child_fitness = self.get_Fitness(tempCHILD[::])
                if(child_fitness >= bestFITNESS):
                    bestCHILD = tempCHILD[::]
                    bestFITNESS = child_fitness

        if(bestCHILD == child or abs(bestFITNESS - self.get_Fitness(baseCHILD)<0.1)):
            index1 = random.randint(0,len(child)-1)
            index2 = random.randint(0,len(child)-1)
            bestCHILD[index1],bestCHILD[index2] = bestCHILD[index2],bestCHILD[index1]
        return bestCHILD
    
    def genetic_algorithm(self):
        population = self.INIpopulation
        probability_to_mutate = 25
        while(True):
            if(self.repeatCOUNT > 50):
                population = self.shuffle_population(population)
                self.repeatCOUNT = 0
            new_population = []
            current_fitness = -1
            current_bestCHILD = []
            for iter in range(self.population_size):
                parents = self.get_parent(population)
                child = self.get_child(parents)
                if(self.generations>3 and self.generation_fitness[-1] == self.generation_fitness[-2]):
                    probability_to_mutate+=2
                    if(probability_to_mutate>80):
                        probability_to_mutate = 25
                if(probability_to_mutate > random.randint(1,100)):
                    child = self.mutate_child(child[::])[::]
                new_population.append(child)
                fitness = self.get_Fitness(child)
                if(fitness > current_fitness):
                    current_fitness = fitness
                    current_bestCHILD = child[::]
                if(fitness > self.bestFITNESS):
                    self.bestchild = child
                    self.bestFITNESS = fitness
                    print(*self.bestchild)
                    print("New Best Fitness Found",self.bestFITNESS)
                    self.repeatCOUNT = 0
            if(self.generations>15 and current_fitness == self.generation_fitness[-1]):
                self.repeatCOUNT+=1
            self.generation_fitness.append(current_fitness)
            print(self.generations, "=> Best Fitness", current_fitness)
            population = new_population[::]
            self.generations+=1

            # Print GRAPH 
            if(self.generations>500):
                print() ; print()
                print(); print()
                print("Best Fitness Found is :- " , self.bestFITNESS, " In 500 Generations")
                x = [i for i in range(1,self.generations+1)]
                y = list(map(lambda x: x ,self.generation_fitness))
                plt.plot(x,y)
                plt.xlabel("Generations")
                plt.ylabel("Fitness")
                plt.title("Improved Algorithm !")
                plt.show()
                return
            





if __name__ == '__main__':
    print(),print()
    print("Choose the Algorithm ...")
    print("------")
    print("Genetic Algorithm [ 8_Queen_Problem ] => Press '1'")
    print("Genetic Algorithm [ Travelling Salesmen Problem ] => Press '2'")
    OptionChoosen = int(input())
    if(OptionChoosen == 1):
        Eight_Queen_Problem()
    elif(OptionChoosen == 2):
        Travelling_Salesmen_Problem()
    else:
        print("Wrong Option !!")

