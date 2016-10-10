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
        diags = [self.matrix[::-1,:].diagonal(i) for i in range(-self.matrix.shape[0]+1,self.matrix.shape[1])]
        diags.extend(self.matrix.diagonal(i) for i in range(self.matrix.shape[1]-1,-self.matrix.shape[0],-1))
        diags = [d for d in [n.tolist() for n in diags] if len(d) > 1]
        for l in diags:
            self.less_than_equal_one(list(l))
        
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
    
    def run_minisat(self,input_file,outputfile):
        os.system("minisat "+input_file+" "+outputfile)
        
    
if __name__ == '__main__':
    prob = NQueens(4)
    prob.row_constraint_init()
    prob.column_constraint_init()
    prob.diagonal_constraint_init()
    prob.write_sat_input()
    prob.run_minisat("input.in", "output.out")