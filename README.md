# Aventura do Colecionador 🏃‍♂️💨

**"Aventura do Colecionador"** é um jogo de plataforma de corrida infinita desenvolvido com Pygame Zero. No jogo, você controla um herói que deve andar sobre a plataforma, coletar moedas até vencer e desviar de inimigos perigosos. A dificuldade aumenta à medida que você avança, tornando cada vez mais desafiador alcançar o objetivo final de 50 moedas.

### Funcionalidades
* **Controles Simples:** Mova o herói para a esquerda e direita e faça-o pular para coletar moedas.
* **Dificuldade Dinâmica:** A velocidade dos inimigos aumenta a cada 5 moedas coletadas, desafiando o jogador.
* **Animações:** Os personagens e as moedas possuem animações básicas para dar vida ao jogo.
* **Gerenciamento de Estado:** O jogo gerencia diferentes estados (menu, jogando, fim de jogo, vitória) para controlar o fluxo da partida.
* **Sons e Música:** A música de fundo pode ser ativados ou desativados.

## Como Rodar o Jogo

Para rodar "Aventura do Colecionador" na sua máquina, siga os passos abaixo.

### Pré-requisitos
* **Python 3** instalado.
* **Pygame Zero** instalado. Você pode instalá-lo facilmente via pip:
    ```bash
    pip install pgzero
    ```

### Instruções

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/crissilvacs/Jogo-plataforma.git
    ```
2.  **Navegue até a pasta do projeto:**
    ```bash
    cd Jogo-plataforma
    ```
3.  **Execute o jogo:**
    ```bash
    pgzrun game.py ou python game.py
    ```

## Estrutura do Código

O código é organizado usando programação orientada a objetos para separar a lógica dos diferentes componentes do jogo.

* **`GameObject`**: A classe base para todos os objetos do jogo, gerenciando posição e velocidade.
* **`Hero`**: A classe do personagem principal, com lógica de movimento, pulo e colisão.
* **`Enemy`**: A classe dos inimigos, com animação e movimento em linha reta.
* **`Coin`**: A classe das moedas, com animação e comportamento de coleta.
* **Funções Principais**: `update()` e `draw()` são as funções centrais que controlam a lógica e o desenho do jogo a cada quadro.

## Tecnologias Utilizadas
* **Pygame Zero**
* **Python 3**

## Contribuição

Sinta-se à vontade para sugerir melhorias.
