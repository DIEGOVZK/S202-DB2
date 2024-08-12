class Professor:
    def __init__(self, nome):
        self.nome = nome

    def ministrar_aula(self, assunto):
        return f'O professor {self.nome} está ministrando uma aula sobre {assunto}'

class Aluno:
    def __init__(self, nome):
        self.nome = nome

    def presenca(self):
        return f'O aluno {self.nome} está presente.'

class Aula:
    def __init__(self, professor, assunto):
        self.professor = professor
        self.assunto = assunto
        self.alunos = []

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)
    
    def listar_presenca(self):
        return f'''Presença na aula sobre {self.assunto}, ministrada pelo professor {self.professor.nome}:
{'\n'.join([aluno.presenca() for aluno in self.alunos])}'''

# Teste fornecido no enunciado
professor = Professor("Lucas")
aluno1 = Aluno("Maria")
aluno2 = Aluno("Pedro")
aula = Aula(professor, "Programação Orientada a Objetos")
aula.adicionar_aluno(aluno1)
aula.adicionar_aluno(aluno2)
print(aula.listar_presenca())

# Saída ao executar script
'''
Presença na aula sobre Programação Orientada a Objetos, ministrada pelo professor Lucas:
O aluno Maria está presente.
O aluno Pedro está presente.
'''