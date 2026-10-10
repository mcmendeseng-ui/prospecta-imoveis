# Circula

Demonstração independente de inteligência de destinação externa de materiais, sem vínculo com organizações. Substitui a antiga página de prospecção de imóveis. O histórico anterior permanece no Git.

## Dados e escopo

Todos os lotes, quantidades, dimensões e preços são fictícios. Imagens ilustrativas geradas por IA. Contatos de possíveis destinos vêm de pesquisa pública de 09/10/2026, com fontes acessíveis na interface. Não representam interesse confirmado ou propostas.

Não há estoque real, identificação empresarial, importação WMS, envio de arquivos, pesquisa autônoma, contatos automáticos ou acesso privado implementado. A seção Estoque e valores é apenas uma simulação pública. Para dados internos, criar backend separado com autenticação e autorização no servidor. Modo vitrine só altera a apresentação e não constitui proteção.

## Cálculos

Venda: quantidade da saída × preço por unidade. Reciclagem: peso da saída × cotação por kg. Doação: receita zero. Custos são logística e preparação; tributos informados em valor total por operação. Pendências não são tratadas como zero. O somatório conhecido é marcado parcial e exclui lotes sem logística ou receita completas. Antes de tributos não é chamado de líquido final. Resultado de caixa não equivale a lucro contábil.

Área liberada: (ceil(estoque/unidades_por_posição) − ceil((estoque−saída)/unidades_por_posição)) × comprimento × largura. Medidas são da posição de armazenamento, incluindo embalagem ou palete. Piso só soma posições exclusivas no chão, sem corredores nem compartilhamento. Prateleira é superfície separada. Faltas de medida permanecem pendentes. Posições exclusivas distintas são uma premissa; em dados reais, validar identificadores de posição para impedir duplicidade. Área concluída depende do status informado, não de evidência externa.

Comparação de preço usado exige fonte, data de até 90 dias e modelo/condição/base compatíveis informados pelo operador. Não é cotação ou validação de mercado automática. Fiscalidade exige enquadramento próprio; nenhuma alíquota genérica é aplicada. A modalidade de frota própria deixa o custo incremental pendente até confirmação.

## Uso

Abrir index.html junto de assets/ ou usar GitHub Pages. Alterações ficam na memória da sessão. Salvar baixa um JSON local; não publica alterações. Restaurar repõe os exemplos. Conferência automática dos cálculos básicos realizada em ambiente JavaScript; renderização de navegador não verificada nesta sessão.
