# Dino Challenge Game

## 📌 Visão Geral
Jogo de plataforma 2D desenvolvido em Python com Pygame Zero. Controle um personagem que deve navegar por um cenário, evitar inimigos e alcançar a bandeira no final do nível.

## 🛠️ Requisitos
- Python 3.7+
- Pygame Zero (`pip install pgzero`)
- Arquivos de assets (imagens/sons) na estrutura correta de pastas

## 🎮 Como Jogar
### Controles:
- **← →** - Movimentar para esquerda/direita
- **Espaço** - Pular
- **F5** - Reiniciar jogo
- **ESC** - Sair do jogo

### Objetivo:
- Chegue até a bandeira no final do nível
- Evite os inimigos para não perder vidas
- Você começa com 5 vidas

## 🏗️ Estrutura do Projeto
```
dino-challenge-game/
├── images/          # Sprites e imagens do jogo
├── sounds/          # Efeitos sonoros e músicas
├── fonts/           # Fontes personalizadas
├── main.py          # Código principal do jogo
└── README.md        # Este arquivo
```

## 🧩 Classes Principais
### `Character`
- Classe base para todos os personagens
- Gerencia movimento, física, animação e vida
- Métodos principais:
  - `move_left()`, `move_right()` - Movimento horizontal
  - `jump()` - Pulo do personagem
  - `update_animation()` - Controle das animações

### `Enemy` (herda de `Character`)
- IA básica de movimento aleatório
- Diferentes comportamentos de patrulha

### `Dino` (herda de `Enemy`)
- Inimigo específico com sprites próprios
- Movimento e animações customizadas

### `Stage`
- Gerencia a construção do cenário
- Posiciona inimigos e plataformas
- Controle de conclusão do nível

## ⚙️ Como Executar
1. Instale as dependências:
   ```bash
   pip install pgzero
   ```

2. Execute o jogo:
   ```bash
   python main.py
   ```

## 🖌️ Assets Necessários
O jogo espera encontrar os seguintes arquivos:

### Imagens:
- `p_idle__00[0-1].png` (animação ao ficar parado)
- `p_run__00[0-9].png` (animação de corrida)
- `p_jump__004.png` (pulo)
- `dino_*.png` (sprites do inimigo)
- `ground.png` (chão)
- `flag_finish.png` (bandeira final)

### Sons:
- `background_intro.wav` (música de fundo inicial)
- `game_win.wav` (vitória)
- `damage.wav` (dano)
- `menu_select_sound.wav` (seleção no menu)

## 📝 Personalização
Você pode modificar:
- `self.level` em `Stage` para mudar a dificuldade (tem até o 5 e é bem dificil)
- Valores de gravidade e velocidade no `Character`

## 🐛 Reportar Problemas
Encontrou um bug? Abra uma issue no repositório com:
- Descrição do problema
- Passos para reproduzir
- Screenshots (se possível)

---

Desenvolvido com ❤️ por Índio Medeiros usando Python e Pygame Zero