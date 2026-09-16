#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
#!/usr/bin/env pybricks-micropython
"""
====================================================================
 TESTE BASICO - Seguidor de Linha (sem PID) - VERSAO EV3
====================================================================

IMPORTANTE (erro "Permission denied"):
Depois de salvar este arquivo no EV3, ele precisa de permissao de
execucao. Se voce tem acesso SSH/terminal, rode:

    chmod +x main.py

Se voce so usa o botao "Download and Run" da extensao do VS Code,
normalmente ela mesma aplica essa permissao ao enviar o arquivo -
mas se copiar o arquivo manualmente (drag-and-drop, scp sem -p,
etc.) essa permissao pode se perder. Nesse caso, rode o chmod acima
por SSH, ou reenvie o arquivo usando o botao da extensao em vez de
copiar manualmente.

Portas (ajuste conforme sua fiacao real no EV3):
  Motor esquerdo   -> Porta A
  Motor direito    -> Porta B
  Sensor esquerdo  -> Porta S1
  Sensor direito   -> Porta S2
  Sensor frontal   -> Porta S3  (mais a frente dos outros, antecipa curva)
  Sensor marcacao  -> Porta S4  (lateral, fora da linha)
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Button
from pybricks.tools import wait

# --------------------------------------------------------------
# CONFIGURACAO DE HARDWARE - ajuste as portas conforme sua montagem
# --------------------------------------------------------------
ev3 = EV3Brick()

motor_1 = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_2 = Motor(Port.B, Direction.CLOCKWISE)

sensor_1 = ColorSensor(Port.S1)
sensor_2 = ColorSensor(Port.S2)
sensor_3 = ColorSensor(Port.S3)
sensor_4 = ColorSensor(Port.S4)

# --------------------------------------------------------------
# PARAMETROS - AJUSTE AQUI DEPOIS DE OLHAR OS VALORES NO CONSOLE
# --------------------------------------------------------------
VELOCIDADE = 250        # graus/s - baixa, so para o teste ser seguro
LIMIAR_LINHA = 50       # acima disso = branco (linha) / abaixo = preto (pista)
LIMIAR_MARCACAO = 30    # abaixo disso = marcacao detectada


# --------------------------------------------------------------
# TESTE 1: motores - roda um pouquinho cada um, pra conferir sentido
# --------------------------------------------------------------
def teste_motores():
    ev3.screen.clear()
    ev3.screen.print("Teste motores")
    print("Testando motor esquerdo (deve girar para frente)...")
    motor_1.run_time(VELOCIDADE, 1000)
    wait(300)

    print("Testando motor direito (deve girar para frente)...")
    motor_2.run_time(VELOCIDADE, 1000)
    wait(300)
    print("Teste de motores concluido.")


# --------------------------------------------------------------
# TESTE 2: sensores - mostra as leituras no console por alguns segundos
# --------------------------------------------------------------
def teste_sensores(duracao_s=10):
    ev3.screen.clear()
    ev3.screen.print("Teste sensores")
    print("Lendo sensores por", duracao_s, "segundos...")
    print("Passe cada sensor sobre PRETO e depois BRANCO para ver os valores.")
    n_leituras = duracao_s * 10
    for _ in range(n_leituras):
        e = sensor_1.reflection()
        d = sensor_2.reflection()
        f = sensor_3.reflection()
        m = sensor_4.reflection()
        print("ESQ:", e, " DIR:", d, " FRENTE:", f, " MARCACAO:", m)
        wait(100)
    print("Teste de sensores concluido.")


# --------------------------------------------------------------
# TESTE 3: seguir linha simples (sem PID) - liga/desliga
# --------------------------------------------------------------
def seguir_linha_simples():
    ev3.screen.clear()
    ev3.screen.print("Pressione CENTER")
    print("Pressione o botao central para comecar a seguir a linha.")
    while not (Button.CENTER in ev3.buttons.pressed()):
        wait(10)
    while Button.CENTER in ev3.buttons.pressed():
        wait(10)

    ev3.screen.clear()
    ev3.screen.print("Seguindo linha")
    print("Seguindo linha (bang-bang). Pressione o botao central para parar.")
    while not (Button.CENTER in ev3.buttons.pressed()):
        e = sensor_1.reflection()
        d = sensor_2.reflection()

        esq_na_linha = e > LIMIAR_LINHA
        dir_na_linha = d > LIMIAR_LINHA

        if esq_na_linha and dir_na_linha:
            # os dois veem a linha -> segue reto
            motor_1.run(VELOCIDADE)
            motor_2.run(VELOCIDADE)

        elif esq_na_linha and not dir_na_linha:
            # so o esquerdo ve a linha -> gira para a esquerda
            motor_1.run(0)
            motor_2.run(VELOCIDADE)

        elif dir_na_linha and not esq_na_linha:
            # so o direito ve a linha -> gira para a direita
            motor_1.run(VELOCIDADE)
            motor_2.run(0)

        else:
            # nenhum ve a linha -> perdeu a linha, para
            motor_1.brake()
            motor_2.brake()
            print("Linha perdida!")

        # apenas para acompanhar no console, sem controlar nada ainda
        f = sensor_3.reflection()
        m = sensor_4.reflection()
        if m < LIMIAR_MARCACAO:
            print("Marcacao detectada! (frente=", f, ")")

        wait(10)

    motor_1.brake()
    motor_2.brake()
    print("Parado.")


# --------------------------------------------------------------
# PROGRAMA PRINCIPAL - escolha o que testar
# --------------------------------------------------------------
def main():
    teste_motores()
    wait(500)
    teste_sensores(10)
    wait(500)
    seguir_linha_simples()


if __name__ == "__main__":
    main()