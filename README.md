# Prospecta — inteligência imobiliária
Painel funcional em português, responsivo e sem dependências de execução. Inclui anúncios públicos localizados e consulta real do IBGE e NASA POWER. Sem dados internos da empresa. Previsão comercial e laudo técnico não são fornecidos automaticamente.

## Funções implementadas
- Filtros por cidade, compra/locação, busca e aderência.
- Preço por m² vs referência comparável, investimento, frota e renda.
- Condição física e ambiental com campos de evidência.
- Comparação entre imóveis e simulação de receita, margem, custos, obras e prazos.
- Fluxo de caixa, retorno desde hoje e valor presente líquido; crescimento de receita em seis meses.
- Importação JSON, fonte HTTPS, exportação e persistência no navegador.
- Monitor agendado no GitHub: novos imóveis e alteração de preço.

## Publicar no GitHub Pages
1. Crie um repositório dedicado e envie este conteúdo à branch `main`.
2. Em Settings > Pages > Build and deployment, selecione GitHub Actions.
3. Execute o fluxo `Publicar painel` ou faça um commit.
4. A coleta pública inicial de Serra/ES já está implementada no fluxo. Para fontes adicionais, configure o secret `PROPERTY_FEEDS` como lista JSON de endereços HTTPS autorizados: `["https://fornecedor.example/imoveis.json"]` (endereço apenas ilustrativo).
5. Execute `Atualizar imóveis públicos`. Depois, o cron consulta aproximadamente a cada seis horas; o GitHub pode atrasar ou suspender execuções conforme suas políticas.

O painel consulta o dataset publicado ao abrir; fontes configuradas no navegador são consultadas a cada cinco minutos somente enquanto aberto. LocalStorage não é um banco corporativo compartilhado. Importações substituem exemplos quando contêm dados reais, mas não removem imóveis ausentes de uma fonte; disponibilidade deve vir no campo status.

## Contrato de dados
JSON: `{"listings": [...]}` ou lista direta. Campos obrigatórios no painel: `id`, `title`, `city`, `type` (Compra/Locação). O monitor exige também `source`. Identificador único por par source/id.

Campos numéricos: area (m²), price (R$ compra ou R$/mês locação), referenceM2 (mesma negociação e base de área), comparables, fleet, income (renda domiciliar R$/mês), health (0–100), works, equipment, projects, releaseDays, buildDays, monthlyRevenue, contributionMargin (0–1), otherMonthlyCosts, contractMonths.

Campos de contexto: state, district, environment, status, sourceDate, url, healthEvidence, marketEvidence, isDemo. Use null para informação desconhecida. Inclua período, geografia, método e fonte no texto das evidências. Não interprete ausência de dados como condição favorável. A condição física precisa de método técnico próprio, não uma nota arbitrária.

## Finanças
Investimento: compra (se aplicável), obras, equipamentos, projetos e aluguel pré-abertura. Abertura = ceil((releaseDays + buildDays)/30), hipótese sequencial simplificada; substituir por caminho crítico em cronograma corporativo. Receita cresce linearmente nos primeiros seis meses após abrir. Custos completos desde a abertura. Payback = primeiro mês de caixa acumulado não negativo desde hoje. VPL usa taxa anual convertida para mensal. Horizonte limitado à ocupação informada e ao horizonte escolhido. Sem valor residual, financiamento, tributos adicionais ou reinvestimentos. Dados incompletos não permitem cálculo confiável. Isto é cenário informado, não modelo de previsão comercial.

## Evolução para operação corporativa
Conectar banco de dados autenticado, histórico de custos e prazo, base comercial, inspeções, contratos e fontes territoriais. Calibrar demanda e receita com unidades reais; registrar validação e incerteza. GitHub Pages hospeda a interface, não banco privado nem credenciais. Não publicar dados internos confidenciais no JSON, commits, logs ou no Pages. Para esses dados, implantar backend autenticado e controles de acesso antes da integração.

A rotina lê um catálogo público limitado da Imobiliária Alex Tongo, sem acesso a contas, e preserva anúncios anteriores quando a fonte muda ou bloqueia a coleta. Não há envio de mensagens ou serviço de IA ativo nesta versão. Os alertas estão no painel. Integração com e-mail/Teams requer configuração e autorização próprias.

## Verificar localmente
`python3 -m http.server 8000` na pasta do projeto. Abra http://localhost:8000.


## Conexões testadas
IBGE: renda per capita de Serra, Censo 2022, 10295/13431 (R$ 1.541,03). NASA: climatologia 2001–2020 no centro municipal aproximado (-20.12,-40.3); não é avaliação de inundação/vento extremo do imóvel. SENATRAN: a fonte retornou HTTP 403 na validação; frota permanece não informada. SGB: consulta técnica manual, não uma integração automática de risco. Dados imobiliários são anunciados, sem confirmação de disponibilidade. Não há dados privados da Autoglass. Áreas propostas são parâmetros ilustrativos editáveis, não dimensões conhecidas das unidades.

## Mapa de oportunidades
Leaflet 1.9.4 e OpenStreetMap. O mapa acompanha filtros e abre a análise do anúncio. Coordenadas aproximadas de bairro são identificadas explicitamente e não representam a localização exata do imóvel. Imóveis importados podem informar latitude, longitude, locationPrecision (property ou neighborhood), locationSource. Registros sem coordenadas permanecem na lista e são contados como não mapeados.
