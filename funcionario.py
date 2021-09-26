import threading
from threading import Lock, Thread
from time import sleep

import init
import nadador

class Funcionario(Thread):
    '''
        Funcion devem ser criados periodicamente e realizar as seguintes ações:
        - Limpar os vestiários masculino e feminino.
        - Descansar.

        A sua responsabilidade é implementar os métodos com o comportamento do
        funcionário, respeitando as restrições impostas no enunciado do trabalho.
     
    '''

    # Construtor da classe Funcionario
    def __init__(self, id):
        # Atributos default
        self.id     = id
        self.genero = 'M'
        self.trabalhando = False

        super().__init__(name=("Funcionario " + str(id)))

    # Imprime mensagem de log
    def log(self, mensagem):
        espacos = (16 - len(self.name)) * ' '
        print('['+ self.name + '] ' + espacos + mensagem + '\n', end='')

    # Comportamento do Funcionario
    def run(self):
        '''
            NÃO ALTERE A ORDEM DAS CHAMADAS ABAIXO.

            Você deve implementar os comportamentos dentro dos métodos da classe.
            Observação: Comente no código qual o objetivo de uma dada operação, 
            ou conjunto de operações, para facilitar a correção do trabalho.
        '''
        self.log("Iniciando o expediente")
        self.trabalhando = True     

        while self.trabalhando == True :
            self.limpar_vest_masculino()
            self.limpar_vest_feminino()
            self.descansar()

        self.log("Terminando o expediente")

    # Funcionário limpa o vestiário masculino. O vestiário não precisa estar vazio.
    def limpar_vest_masculino(self):
        # espera até conseguir limpar o vestiáro masculino
        while init.esperando_para_limpar_vestiario_masculino:
            # caso nenhuma ducha esteja ocupada, limpa o vestiário masculino
            if nadador.ducha_masculino._value == init.quant_duchas_por_vestiario:
                self.log("Iniciando limpeza do vestiário masculino")

                # bloqueando as duchas masculinas
                init.limpando_vestiario_masculino = True
                # não está mais esperando
                init.esperando_para_limpar_vestiario_masculino = False
                
                sleep(init.tempo_limpeza_vestiario * init.unidade_de_tempo)
                sleep(init.quant_duchas_por_vestiario * init.tempo_limpeza_ducha * init.unidade_de_tempo)
                
        init.limpando_vestiario_masculino = False
        init.esperando_para_limpar_vestiario_masculino = True
        
        self.log("Concluída a limpeza do vestiário masculino")

    # Funcionário limpa o vestiário feminino. ATENÇÃO: o vestiário precisa estar vazio!!!
    def limpar_vest_feminino(self):
        # espera até conseguir limpar o vestiáro femenino
        while init.esperando_para_limpar_vestiario_feminino:      
            # caso nenhuma ducha esteja ocupada, limpa o vestiário femenino
            if init.vestiario_feminino == 0:
                self.log("Iniciando limpeza do vestiário feminino")
                # bloqueia o vestiário femenino
                init.limpando_vestiario_feminino = True
                # não está mais esperando
                init.esperando_para_limpar_vestiario_feminino = False
                sleep(init.tempo_limpeza_vestiario * init.unidade_de_tempo)
                sleep(init.quant_duchas_por_vestiario * init.tempo_limpeza_ducha * init.unidade_de_tempo)
                
        init.limpando_vestiario_feminino = False
        init.esperando_para_limpar_vestiario_feminino = True
        self.log("Concluída a limpeza do vestiário feminino")
        
    # Funcionário descansa durante um tempo
    def descansar(self):
        self.log("Hora do intervalo de descanso.")
        sleep(init.tempo_descanso * init.unidade_de_tempo)
        self.log("Fim do intervalo de descanso.")
        
        # TODO: rever
        # se não há mais nenhum nadador na academia e não entrará mais ninguém na academia o funcionario para de trabalhar
        if len(threading.enumerate()) == 2 and not init.nadores_entrando:
            self.trabalhando = False



