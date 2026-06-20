# Floor Tile Pagination Generator

Gerador de paginação de piso por linha de comando. O programa coleta, de forma
interativa no console, as imagens de cada posição da grade e as medidas físicas
do piso, e compõe uma única imagem PNG com o rejunte proporcional aplicado entre
e ao redor das peças.

> ⚠️ Protótipo. O foco é um resultado funcional e rápido de iterar; não há suíte
> de testes automatizados (veja `.specify/memory/constitution.md`).

## Como funciona

- A imagem da posição `1x1` é a **referência**: o tamanho dela em pixels define o
  tamanho da célula. As demais imagens são redimensionadas para esse tamanho.
- O **ratio** (proporção pixel ↔ medida física) é `pixels da imagem ÷ tamanho
  físico do piso`, calculado por eixo.
- O **rejunte em pixels** é `tamanho do rejunte × ratio`, arredondado.
- O tamanho final por eixo é `n × (célula_px + rejunte_px)`, onde `n` é o número
  de peças naquele eixo. O rejunte é desenhado como o fundo do canvas (entre as
  peças e na borda externa).

### Exemplos

| Unidade | Grade | Piso | Imagem | Rejunte | ratio | rejunte_px | Saída |
|---------|-------|------|--------|---------|-------|-----------|-------|
| mm | 2x2 | 1000×1000 | 150×150 | 1,5 | 0.15 | round(0.225) = 0 | 300×300 |
| cm | 2x2 | 100×100 | 150×150 | 2 | 1.5 | round(3.0) = 3 | 306×306 |

Quando o rejunte arredonda para 0, as peças ficam encostadas (sem espaçamento).

## Requisitos

- Python 3.10+
- Pillow

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

O programa pergunta, em sequência:

1. **Unidade de medida**: `centimeters`, `meters` ou `millimeters`
2. **Tamanho da grade**: `2x2`, `2x3`, `3x2` ou `3x3` (formato `linhas x colunas`)
3. **Caminho da imagem** de cada posição (`png`, `jpg` ou `jpeg`), na ordem de
   leitura (`1x1`, `1x2`, …)
4. **Altura** e **largura** do piso (na unidade escolhida)
5. **Espessura do rejunte** (na unidade escolhida)
6. **Cor do rejunte** em hexadecimal `#RRGGBB` — *solicitada apenas se o rejunte
   for maior que zero*
7. **Caminho do arquivo PNG** de saída

Em seguida é exibido um resumo e pedida a confirmação (`yes`/`no`). Apenas com
`yes` o arquivo é gerado (sobrescreve se já existir); com `no` nada é gravado.

### Exemplo de sessão

```
Floor Tile Pagination Generator
Units: centimeters, meters, millimeters
Grids: 2x2, 2x3, 3x2, 3x3
Images: png, jpg, jpeg

Unit of measure (centimeters/meters/millimeters): centimeters
Grid size (2x2, 2x3, 3x2, 3x3): 2x2
Imagem 1x1 path (png/jpg/jpeg): ./image1.png
Imagem 1x2 path (png/jpg/jpeg): ./image2.png
Imagem 2x1 path (png/jpg/jpeg): ./image3.png
Imagem 2x2 path (png/jpg/jpeg): ./image4.png
Tile height in centimeters: 100
Tile width in centimeters: 100
Grout thickness in centimeters: 2
Grout color (#RRGGBB): #CECECE
Output PNG path: out_cm.png

Summary
...
Generate this layout? (yes/no): yes
Saved to out_cm.png
```

## Validação

Toda entrada inválida é rejeitada com mensagem e re-perguntada (sem encerrar o
programa): grade fora do conjunto permitido, unidade desconhecida, formato de
imagem diferente de png/jpg/jpeg, arquivo inexistente, número inválido e cor fora
do padrão `#RRGGBB`.

## Estrutura

```
main.py            # Fluxo de console: prompts, validação, resumo e confirmação
pagination.py      # Lógica de composição: ratio, rejunte em pixels e montagem (Pillow)
requirements.txt   # Pillow
specs/             # Especificação, plano e tarefas (Spec Kit)
```

## Licença

Veja [LICENSE](./LICENSE).
