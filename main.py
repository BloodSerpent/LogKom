'''
Created on Oct 10, 2016

@author: ASUS
'''
import os
import numpy as np
class NQueens:
    def __init__(self, n):
        self.n = n
        self.matrix = np.arange(1,self.n**2+1).reshape(self.n,self.n)
        self.rules = []
    
    def row_constraint_init(self):
        '''
            for each row, there is exactly one queen i.e for n = 4
            1 -2 -3 -4 0
            this one is a | b | c | d ....
        '''
        for l in self.matrix:
            l = list(l)
            self.equal_one(l)
            self.less_than_equal_one(l)
        
    
    def column_constraint_init(self):
        '''
            for each row, there is exactly one queen i.e for n = 4
            1 -2 -3 -4 0
            this one is a | b | c | d ....
        '''
        m = self.matrix.transpose()
        for l in m:
            l = list(l)
            self.equal_one(l)
            self.less_than_equal_one(l)
    
    def equal_one(self,literal):
        l = list(literal)
        l.append(0)
        self.rules.append(l)
        
    def less_than_equal_one(self,literal):
        clause = []
        for ii in range(len(literal)-1):
            for jj in range(ii+1,len(literal)):
                clause.append(-literal[ii])
                clause.append(-literal[jj])
                clause.append(0)
                self.rules.append(clause)
                clause = []
    
    
    def diagonal_constraint_init(self):
        diags = self.extract_diagonal(self.matrix)
        for l in diags:
            self.less_than_equal_one(list(l))

    def extract_diagonal(self, matrix):
        diags = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[0]+1,matrix.shape[1])]
        diags.extend(matrix.diagonal(i) for i in range(matrix.shape[1]-1,-matrix.shape[0],-1))
        diags = [d for d in [n.tolist() for n in diags] if len(d) > 1]
        return diags

    def valid_answer(self, answer):
        if self.valid_row(answer):
            if self.valid_column(answer):
                if self.valid_diags(answer):
                    return True
        return False

    def valid_row(self, answer):
        for l in answer:
            l = list(l)
            if sum(l) != 1:
                return False
        return True

    def valid_column(self, answer):
        m = answer.transpose()
        for l in m:
            l = list(l)
            if sum(l) != 1:
                return False
        return True

    def valid_diags(self, answer):
        diags = self.extract_diagonal(answer)
        for l in diags:
            if sum(l) > 1:
                return False
        return True
        
    '''
        header for minisat:
        p num_var num_clause
    '''
    def write_sat_input(self):
        f = open("input.in",'w')
        f.write("p cnf "+str(self.n**2)+" "+str(len(self.rules))+"\n")
        for clause in self.rules:
            strs = ""
            for lit in clause:
                strs = strs+str(lit)+" "
            strs = strs.strip()
            strs = strs + "\n"
            f.write(strs)
        f.close()

    def get_output(self):
        f = open("output.out",'r')
        f.readline()
        s = f.readline().strip().split()
        f.close()
        if len(s) == 0:
            return []
        s.pop(self.n*self.n)
        s = [int(x) for x in s]
        return s
    
    def run_minisat(self,input_file,outputfile):
        os.system("minisat "+input_file+" "+outputfile)
        
    
if __name__ == '__main__':
    prob = NQueens(3)
    prob.row_constraint_init()
    prob.column_constraint_init()
    prob.diagonal_constraint_init()
    prob.write_sat_input()
    prob.run_minisat("input.in", "output.out")
