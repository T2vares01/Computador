import os, sys, unittest
RAIZ=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(RAIZ,"tests")); sys.path.insert(0,os.path.join(RAIZ,"simulador"))
from lib_circ import avaliador
import minicpu4_simulador as sim
# tabela do Logisim (Combinational Analysis): chave = (A, B, P, N)
TABELA={(0,0,0,0):1,(0,0,0,1):0,(0,0,1,0):0,(0,0,1,1):1,(0,1,0,0):0,(0,1,0,1):0,(0,1,1,0):1,(0,1,1,1):0,
        (1,0,0,0):0,(1,0,0,1):0,(1,0,1,0):1,(1,0,1,1):0,(1,1,0,0):0,(1,1,0,1):1,(1,1,1,0):1,(1,1,1,1):1}
CIRC=os.path.join(RAIZ,"circuitos","seletor.circ")
class Testes(unittest.TestCase):
    def test_funcao_da_celula(self):
        for (a,b,p,n),x in TABELA.items(): self.assertEqual(sim.cell(a,b,p,n),x,(a,b,p,n))
    def test_circ_seletor(self):
        ev=avaliador(CIRC,"seletor")
        for (a,b,p,n),x in TABELA.items(): self.assertEqual(ev({"A":a,"B":b,"P":p,"N":n})["X"],x,(a,b,p,n))
    def test_circ_com_not(self):
        ev=avaliador(CIRC,"seletor_com_NOT")
        for (a,b,p,n),x in TABELA.items(): self.assertEqual(ev({"A":a,"B":b,"P":p,"N":n})["X"],1-x,(a,b,p,n))
    def test_computador_contagem_regressiva(self):
        c=sim.CPU(); c.rom=[sim.montar(l) for l in ["LDI 5","SUB 1","JZ 4","JMP 1","HLT","","",""]]; c.reset()
        vistos=[]
        while not c.parado and len(vistos)<50: c.passo(); vistos.append(c.acc)
        self.assertEqual(c.acc,0); self.assertEqual(c.pc,4); self.assertIn(1,vistos)
if __name__=="__main__": unittest.main()
