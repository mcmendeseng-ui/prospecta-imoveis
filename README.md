# Circula

Demonstração independente de destinação externa de materiais, sem vínculo empresarial.

O site público contém apenas exemplos e imagens ilustrativas. Dados reais não estão no repositório. Carregar estoque local lê um JSON selecionado só na memória do navegador, sem envio ou sincronização. Salvar baixa um arquivo local; carregar recupera esse arquivo. Não é uma área autenticada. Usar em dispositivo confiável e manter as cópias privadas.

Painel financeiro no topo e valores por item: receita, custos, tributos por rota e área. Venda, doação e sucata têm configurações fiscais independentes. Tributos podem ser informados como total ou base × carga efetiva manual; nenhuma alíquota ou classificação é presumida. A conta não valida o enquadramento tributário.

Sucata: peso da carga × cotação por kg. Peso, logística ou cotação pendentes não viram zero; resultado conhecido é parcial. Quantidades de bases distintas não devem ser somadas. Preço de varejo não é retorno de sucata. Agrupamentos pela descrição exigem confirmar composição e destinatário. Fotos são referências ilustrativas, não fotos do estoque.

Piso liberado: diferença de posições inteiramente esvaziadas × base da posição. Dimensões ausentes ficam a medir. Prateleira é superfície, não piso. Não somar corredores ou posições compartilhadas. Venda de sucata também libera espaço. Custo evitado só deve ser declarado quando houver despesa efetivamente reduzida.

Comparação de usados exige fonte, data recente e modelo/condição comparáveis informados; não há pesquisa de preço automática. Compradores têm fontes públicas e interesse ainda a confirmar. Busca, filtros e paginação suportam o arquivo local. Os dados carregados continuam apenas na sessão até serem salvos pelo usuário.

Verificações JavaScript cobrem cálculos, troca fiscal por rota, falta de dados, paginação e estoque completo no arquivo local separado. Renderização do navegador não verificada nesta sessão.
