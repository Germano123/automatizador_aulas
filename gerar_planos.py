#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de planos de aula - Desenhista Grafico e Excel Avancado
Estrutura: dados/<Curso>/<Unidade> (XXh)/aulas.csv
Colunas: tipo de aula;conteudo previsto;licao de casa;observacao;status;erro
Regras: tipo in {Teorica, Pratica, Laboratorio}, 4h/dia, obs = Dia X, hora Y/4.
Carga exata mantida (ultimo dia parcial quando necessario).
"""
import os
import csv

BASE = r"C:\Users\Germano\Documents\projects\sideprojects\automatizador_planos\dados"

HEADER = ["tipo de aula", "conteúdo previsto", "lição de casa", "observação", "status", "erro"]

LICOES_CICLO = [
    "Realizar a atividade proposta e salvar a versão produzida.",
    "Continuar a prática e aperfeiçoar o produto iniciado.",
    "Revisar o produto e corrigir problemas identificados.",
    "Finalizar o produto e preparar a versão para apresentação.",
]

def tipos_para_dia(d, lab_days, parcial=False):
    if parcial:
        return ["Laboratório", "Laboratório"]
    if d in lab_days:
        return ["Teórica", "Prática", "Prática", "Laboratório"]
    return ["Teórica", "Teórica", "Prática", "Prática"]

def gerar_csv(curso, unidade_nome, total_horas, modulos, lab_days):
    """
    modulos: lista de (titulo_modulo, [4 detalhes])
    total_horas deve ser igual a soma das aulas geradas a partir de modulos
    (para dia parcial, o ultimo modulo tem apenas 2 detalhes)
    """
    pasta_unidade = os.path.join(BASE, curso, f"{unidade_nome} ({total_horas}h)")
    os.makedirs(pasta_unidade, exist_ok=True)
    caminho = os.path.join(pasta_unidade, "aulas.csv")

    linhas = []
    dia = 1
    # Agrupar modulos em dias de 4 aulas
    idx = 0
    total_aulas = total_horas
    # modulos ja vem em dias (4 detalhes cada), exceto ultimo que pode ter 2
    for titulo, detalhes in modulos:
        eh_parcial = len(detalhes) == 2
        tipos = tipos_para_dia(dia, lab_days, parcial=eh_parcial)
        for h, detalhe in enumerate(detalhes, start=1):
            tipo = tipos[h-1]
            conteudo = f"Dia {dia} — {titulo}: {detalhe}."
            # liciao ciclica por hora (1..4), para dia parcial usa as duas primeiras
            licao = LICOES_CICLO[h-1]
            desc_obs = detalhe[0].upper() + detalhe[1:]
            obs = f"Dia {dia}, hora {h}/4. {desc_obs}."
            linhas.append([tipo, conteudo, licao, obs, "preenchida", ""])
        dia += 1

    assert len(linhas) == total_aulas, f"{curso} / {unidade_nome}: esperado {total_aulas}, gerado {len(linhas)}"
    # validacoes
    for i, l in enumerate(linhas, start=1):
        assert l[0] in ("Teórica", "Prática", "Laboratório"), f"tipo invalido: {l[0]}"
        # observacao deve conter Dia x hora y/4
        assert f"Dia " in l[3] and f"hora " in l[3] and "/4" in l[3], f"observacao invalida linha {i}: {l[3]}"
        assert l[4] == "preenchida"

    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\n")
        w.writerow(HEADER)
        w.writerows(linhas)
    print(f"OK {len(linhas):3d} aulas -> {caminho}")
    return caminho

# ------------------------------------------------------------
# 1) DESENHISTA GRAFICO - Criacao e editoracao de multimidia (30h)
# ------------------------------------------------------------
multimidia = [
    ("Fundamentos de multimídia", [
        "conceito e tipos de multimídia: texto, imagem, áudio, vídeo e animação",
        "elementos e integração de mídias em um produto digital",
        "formatos digitais e compatibilidade com a web",
        "direitos autorais, licenças de uso e bancos de mídia livre",
    ]),
    ("Imagem digital", [
        "pixel, resolução, densidade e dimensões de imagem",
        "formatos JPG, PNG, GIF, WEBP e SVG e quando usar cada um",
        "modos de cor RGB e CMYK e preparação para tela e impressão",
        "organização de arquivos, nomeação e backup de acervo de imagens",
    ]),
    ("Edição de imagem I", [
        "interface e ferramentas básicas de editor de imagem (Photoshop ou GIMP)",
        "seleção, recorte, redimensionamento e alinhamento de elementos",
        "camadas, máscaras e transparência na composição visual",
        "correção de imperfeições e restauração básica de imagem",
    ]),
    ("Edição de imagem II", [
        "tratamento de cor, brilho, contraste e saturação",
        "filtros, texturas e efeitos para composição gráfica",
        "tipografia aplicada sobre imagem e equilíbrio visual",
        "exportação de imagem para web e impressão com qualidade",
    ]),
    ("Edição de áudio", [
        "conceito de som digital, frequência, amostragem e formatos MP3 e WAV",
        "gravação de narração e ruídos com microfone e ambiente adequado",
        "edição no Audacity: cortes, volume, ruído e normalização",
        "criação de trilha sonora, mixagem e exportação para produto multimídia",
    ]),
    ("Edição de vídeo", [
        "planejamento de roteiro, captação e organização de takes",
        "interface de editor de vídeo, linha do tempo e importação de mídias",
        "cortes, transições, textos e ajustes de cor em vídeo curto",
        "áudio do vídeo, legendas, exportação e publicação online",
    ]),
    ("Animação e integração multimídia", [
        "animação quadro a quadro, GIF animado e principais tipos de movimento",
        "ferramentas online de animação e criação de peças para redes sociais",
        "integração de texto, imagem, áudio, vídeo e animação em uma peça multimídia",
        "testes de compatibilidade, acessibilidade e otimização do peso do arquivo",
    ]),
    ("Projeto integrador", [
        "desenvolvimento e revisão da peça multimídia final em laboratório",
        "apresentação, avaliação coletiva e exportação da versão final",
    ]),
]

# ------------------------------------------------------------
# 2) DESENHISTA GRAFICO - Estruturacao de interface web (80h)
# ------------------------------------------------------------
estruturacao = [
    ("Introdução à Web", [
        "evolução da web e papel dos navegadores",
        "protocolo HTTP e HTTPS e funcionamento de cliente e servidor",
        "domínios, hospedagem e endereço URL",
        "ambiente de trabalho, editor de código e servidor local",
    ]),
    ("HTML5 e estrutura básica", [
        "documento HTML5, DOCTYPE, head e metadados essenciais",
        "estrutura básica head, body e hierarquia de elementos",
        "comentários, indentação e validação de código",
        "criação da primeira página web completa",
    ]),
    ("Texto e semântica HTML", [
        "títulos, parágrafos, quebra de linha e linha horizontal",
        "ênfase, importância, abreviações, citações e código inline",
        "uso correto de headings e ordem hierárquica",
        "formatação de texto para leitura e SEO",
    ]),
    ("Listas, links e navegação", [
        "listas ordenadas, não ordenadas e de definição",
        "links absolutos, relativos e âncoras internas",
        "menu de navegação básico em HTML",
        "navegação entre páginas de um mesmo site",
    ]),
    ("Imagens e mídias", [
        "inserção de imagens, atributo alt e dimensões",
        "figuras e legendas semânticas com figure e figcaption",
        "formatos de imagem para web e boas práticas de nomeação",
        "inserção de áudio e vídeo em HTML5",
    ]),
    ("Tabelas HTML", [
        "construção de tabelas, linhas, cabeçalhos e células",
        "agrupamento de linhas e colunas com thead, tbody e tfoot",
        "células mescladas com colspan e rowspan",
        "tabela acessível com caption e escopo",
    ]),
    ("Formulários HTML", [
        "estrutura de formulários, método e ação",
        "campos de texto, senha, e-mail, data e número",
        "campos de escolha, lista suspensa, textarea e upload",
        "botões, rótulos, validação nativa e acessibilidade",
    ]),
    ("HTML semântico e acessibilidade", [
        "elementos estruturais header, footer, nav, main, article, section e aside",
        "hierarquia semântica e uso de landmarks",
        "noções de acessibilidade, ARIA e navegação por teclado",
        "SEO básico: títulos, meta description e conteúdo semântico",
    ]),
    ("CSS — introdução", [
        "conceito de CSS, estilos inline, internos e externos",
        "seletores de elemento, classe, ID e universais",
        "cores, fundos e fontes no CSS",
        "especificidade e cascata",
    ]),
    ("Box Model", [
        "margens, bordas, preenchimentos e conteúdo",
        "propriedades de largura, altura e box-sizing",
        "bordas arredondadas, sombras e controle de overflow",
        "organização de espaçamentos com consistência visual",
    ]),
    ("Layout Flexbox", [
        "conceito de container e itens flexíveis",
        "direção, alinhamento e distribuição com justify e align",
        "crescimento, encolhimento e base flexível",
        "layouts flexíveis para menus e cartões",
    ]),
    ("Layout Grid e posicionamento", [
        "conceito de grade, linhas, colunas e áreas",
        "posicionamento estático, relativo, absoluto e fixo",
        "criação de layouts de página com Grid",
        "alinhamento, sobreposição e controle de z-index",
    ]),
    ("Componentes visuais", [
        "tipografia web: tamanhos, pesos e espaçamentos",
        "botões, links estilizados, listas e menus horizontais",
        "cartões, divisores e elementos de destaque",
        "estados hover, focus, active e transições simples",
    ]),
    ("CSS responsivo", [
        "conceito de design responsivo e mobile first",
        "media queries e pontos de quebra (breakpoints)",
        "imagens e layouts fluidos para telas pequenas",
        "testes em diferentes larguras de tela",
    ]),
    ("Boas práticas HTML e CSS", [
        "organização de arquivos CSS e convenções de nomes",
        "reset e normalização, compatibilidade entre navegadores",
        "validação HTML e CSS e correção de erros",
        "desempenho: peso de páginas, cache e minificação",
    ]),
    ("Página completa I — estrutura", [
        "planejamento da estrutura de uma página institucional",
        "criação do HTML completo de cabeçalho, navegação e conteúdo",
        "inclusão de textos, imagens, links e formulários",
        "revisão semântica e acessibilidade do HTML",
    ]),
    ("Página completa II — estilização", [
        "estilização da página com CSS externo",
        "layout responsivo com Flexbox e Grid",
        "refinamento tipográfico, de cores e espaçamentos",
        "estados interativos e acabamento visual",
    ]),
    ("Otimização web", [
        "otimização de imagens para web sem perda excessiva de qualidade",
        "carregamento eficiente de fontes e recursos",
        "acessibilidade final: contraste, foco e leitura de tela",
        "revisão de boas práticas e SEO básico",
    ]),
    ("Laboratório — revisão e testes", [
        "testes em navegadores diferentes e em dispositivos",
        "correção de layout, links quebrados e formulários",
        "validação final do código e checklist de qualidade",
        "preparação do projeto estrutural para apresentação",
    ]),
    ("Projeto estrutural — apresentação", [
        "apresentação da página desenvolvida em laboratório",
        "demonstração de estrutura semântica e responsividade",
        "avaliação coletiva e feedback técnico",
        "exportação e publicação do projeto em hospedagem gratuita",
    ]),
]

# ------------------------------------------------------------
# 3) DESENHISTA GRAFICO - Fundamentos de Web design (80h)
# ------------------------------------------------------------
fundamentos_web = [
    ("Fundamentos de design", [
        "elementos visuais: linha, forma, cor, textura e espaço",
        "princípios de design: equilíbrio, contraste, repetição e proximidade",
        "percepção visual e leitura da imagem",
        "análise de referências visuais e repertório",
    ]),
    ("Teoria da cor", [
        "psicologia e significado das cores",
        "modelo RGB, HSL e paleta cromática",
        "contraste, harmonia e combinações de cores",
        "acessibilidade de contraste para web",
    ]),
    ("Tipografia web", [
        "anatomia da letra e famílias tipográficas",
        "hierarquia tipográfica: títulos, subtítulos e corpo de texto",
        "legibilidade, espaçamento entre linhas e colunas",
        "uso de fontes web e Google Fonts",
    ]),
    ("Composição e grade", [
        "alinhamento, proximidade e repetição em layouts",
        "espaço em branco e respiro visual",
        "grade de colunas e sistemas de retícula",
        "equilíbrio entre texto, imagem e elementos gráficos",
    ]),
    ("Identidade visual para web", [
        "conceito de identidade visual e consistência",
        "elementos de marca: logo, cores e tipografia aplicada a telas",
        "criação de paleta e guias básicos de uso",
        "aplicação da identidade em cabeçalho e rodapé",
    ]),
    ("Pesquisa e referência visual", [
        "pesquisa de concorrentes e referências de design",
        "moodboard e coleção de referências visuais",
        "definição de público, objetivo e mensagem da interface",
        "direcionamento criativo e conceito visual",
    ]),
    ("UX — experiência do usuário", [
        "conceito de experiência do usuário e jornada do usuário",
        "personas e necessidades do público-alvo",
        "arquitetura da informação, organização e rotulagem",
        "fluxos de navegação e caminhos do usuário",
    ]),
    ("Usabilidade", [
        "heurísticas de usabilidade de Nielsen",
        "prevenção de erros e mensagens de feedback",
        "testes de usabilidade e observação de tarefas",
        "melhorias iterativas a partir de testes",
    ]),
    ("Wireframe", [
        "conceito de wireframe e fidelidade de protótipos",
        "wireframes de baixa fidelidade em papel ou digital",
        "estrutura de páginas e componentes principais",
        "testes de navegação no wireframe",
    ]),
    ("UI — componentes de interface", [
        "componentes de interface: botões, campos e menus",
        "ícones, estados e feedback visual interativo",
        "hierarquia visual e ponto focal",
        "consistência entre telas e componentes",
    ]),
    ("Figma I — ferramentas", [
        "interface, ferramentas e organização de arquivos no Figma",
        "criação de frames, bibliotecas e estilos",
        "auto layout e componentes reutilizáveis",
        "organização de telas e nomenclatura de camadas",
    ]),
    ("Protótipo interativo", [
        "criação de protótipo navegável no Figma",
        "transições, animações e simulação de fluxo",
        "compartilhamento do protótipo para testes",
        "validação do fluxo com usuários simulados",
    ]),
    ("Design responsivo", [
        "design responsivo e adaptação para mobile",
        "breakpoints, grids flexíveis e conteúdo prioritário",
        "design de menus e navegação em telas pequenas",
        "testes de layout em múltiplos dispositivos",
    ]),
    ("Design para conversão", [
        "princípios de design para conversão e confiança",
        "CTAs, hierarquia de informação e escaneabilidade",
        "prova social, depoimentos e elementos de credibilidade",
        "equilíbrio entre estética e objetivo comercial",
    ]),
    ("Acessibilidade visual", [
        "design inclusivo e acessibilidade digital",
        "contraste, tamanho de fonte e navegação por teclado",
        "descrição alternativa e linguagem clara",
        "testes de acessibilidade e ajustes finais",
    ]),
    ("Linguagem visual web", [
        "tendências de linguagem visual web e leitura crítica",
        "minimalismo, dark mode e interfaces modernas",
        "uso de fotografia, ilustração e ícones em interfaces",
        "evolução do design web e boas práticas atuais",
    ]),
    ("Sistema de design", [
        "conceito de design system e tokens de design",
        "biblioteca de cores, tipografia e componentes",
        "documentação de padrões visuais",
        "manutenção e escalabilidade do sistema",
    ]),
    ("Documentação e handoff", [
        "preparação de arquivos para desenvolvimento",
        "especificações de medidas, cores e exportação de assets",
        "organização de telas e anotações para desenvolvedores",
        "revisão final do design antes da implementação",
    ]),
    ("Laboratório — projeto de design", [
        "desenvolvimento do projeto de interface no Figma",
        "refinamento visual, protótipo e testes",
        "ajustes de usabilidade e acessibilidade",
        "preparação da apresentação do projeto",
    ]),
    ("Apresentação e avaliação", [
        "apresentação do projeto de design em laboratório",
        "demonstração do protótipo navegável e decisões de design",
        "avaliação coletiva e feedback dos pares",
        "entrega final dos arquivos de design organizados",
    ]),
]

# ------------------------------------------------------------
# 4) DESENHISTA GRAFICO - Projeto de interface web (50h)
# ------------------------------------------------------------
projeto_interface = [
    ("Briefing do projeto", [
        "briefing do cliente e definição do problema",
        "objetivos, metas e público da interface",
        "escopo, prazos e entregas do projeto",
        "alinhamento de expectativas e critérios de sucesso",
    ]),
    ("Pesquisa e requisitos", [
        "pesquisa de mercado e análise de concorrentes",
        "levantamento de requisitos funcionais e de conteúdo",
        "definição de funcionalidades prioritárias (MVP)",
        "documento de requisitos e aprovações",
    ]),
    ("Arquitetura da informação", [
        "sitemap e estrutura de páginas",
        "organização de conteúdos e navegação principal",
        "taxonomia, rótulos e glossário de termos",
        "validação da arquitetura com testes simples",
    ]),
    ("Wireframes e fluxos", [
        "wireframes de baixa fidelidade das telas principais",
        "fluxos de usuário e cenários de uso",
        "testes e ajustes de navegação no wireframe",
        "apresentação intermediária do conceito",
    ]),
    ("Design visual UI", [
        "design system do projeto: cores, tipografia e componentes",
        "telas em alta fidelidade no Figma",
        "refinamento de hierarquia visual e identidade",
        "revisão e aprovação do design visual",
    ]),
    ("Protótipo navegável", [
        "prototipação interativa das telas",
        "simulação de fluxos completos de uso",
        "testes de usabilidade com usuários",
        "ajustes de design a partir dos testes",
    ]),
    ("Implementação — estrutura HTML", [
        "estruturação HTML das páginas do projeto",
        "codificação semântica e acessível",
        "inclusão de conteúdo: textos, imagens e formulários",
        "revisão do código e validação HTML",
    ]),
    ("Implementação — estilização CSS", [
        "layout CSS com Flexbox e Grid",
        "responsividade e adaptação mobile",
        "componentes visuais e estados interativos",
        "refinamento tipográfico e de cores",
    ]),
    ("Interatividade e refinamentos", [
        "refinamentos de CSS e transições",
        "menu responsivo e navegação mobile",
        "tratamento de formulários e feedback",
        "otimização de imagens e desempenho",
    ]),
    ("Testes e acessibilidade", [
        "testes em navegadores e dispositivos",
        "testes de acessibilidade e correção de contraste e foco",
        "validação de links, formulários e conteúdos",
        "checklist de qualidade e usabilidade",
    ]),
    ("Revisão final", [
        "revisão geral do projeto e correção de detalhes",
        "documentação do projeto e guia de uso",
        "preparação de arquivos e backup do código fonte",
        "simulação da apresentação final",
    ]),
    ("Laboratório — consolidação", [
        "consolidação do projeto em ambiente de laboratório",
        "demonstração de fluxos, responsividade e acessibilidade",
        "revisão coletiva e ajustes finais urgentes",
        "preparação final para apresentação",
    ]),
    ("Apresentação final", [
        "apresentação do projeto final em laboratório",
        "demonstração da interface implementada e do protótipo",
    ]),
]

# ------------------------------------------------------------
# 5) EXCEL AVANCADO - Excel avancado (110h)
# ------------------------------------------------------------
excel_avancado = [
    ("Interface e otimização", [
        "formatação avançada de células, estilos e temas",
        "barra de ferramentas, guia personalizada e atalhos de teclado",
        "proteção e desbloqueio de células",
        "modelos de pasta de trabalho e configurações",
    ]),
    ("Referências e intervalos", [
        "referências relativas, absolutas e mistas",
        "nomeação de intervalos e uso em fórmulas",
        "referências entre planilhas e pastas",
        "uso de intervalos nomeados em validações e tabelas dinâmicas",
    ]),
    ("Matemática e estatística", [
        "SOMA, SOMASE, SOMASES e PRODUTO",
        "MÉDIA, MÉDIASE, MAIOR, MENOR e percentis",
        "CONTAR, CONTARVALORES e CONT.SE",
        "funções de arredondamento e conversão numérica",
    ]),
    ("Funções condicionais", [
        "SE e aninhamento de condições",
        "E, OU e NÃO em fórmulas compostas",
        "SEERRO, SE.NULO e tratamento de erros",
        "exercícios de classificação e enquadramento",
    ]),
    ("Texto e data", [
        "funções de texto DIREITA, ESQUERDA e EXTRAIR",
        "CONCATENAR, TEXTO e conversão de formatos",
        "funções de data HOJE, DATA, DATEDIF e EDATE",
        "tratamento de datas e cálculo de prazos",
    ]),
    ("Funções de busca", [
        "PROCV básico e avançado com intervalos",
        "XLOOKUP e vantagens sobre PROCV",
        "ÍNDICE e CORRESP para busca bidimensional",
        "EQUIV e buscas aproximadas",
    ]),
    ("Funções lógicas e de informação", [
        "funções lógicas avançadas combinadas com SE",
        "ÉNUMERO, ÉTEXTO e ISNÚMERO",
        "MAIUSCULA, MINUSCULA e limpeza de dados",
        "auditoria de fórmulas e rastreamento de precedentes",
    ]),
    ("Validação e proteção de dados", [
        "validação de dados: listas e critérios personalizados",
        "mensagens de entrada e alerta de erro",
        "proteção de planilha e pasta com senha",
        "desbloqueio de células e validação de consistência",
    ]),
    ("Formatação condicional avançada", [
        "regras com condições e fórmulas personalizadas",
        "barras de dados, escalas de cores e ícones",
        "formatação condicional com funções",
        "destaque de duplicadas e valores extremos",
    ]),
    ("Tabela dinâmica I", [
        "criação de tabela dinâmica a partir de intervalos",
        "campos, valores, filtros e layout de tabela dinâmica",
        "agrupamento por data e por valores",
        "atualização e formatação de tabelas dinâmicas",
    ]),
    ("Tabela dinâmica II", [
        "tabelas dinâmicas com múltiplos campos",
        "segmentação de dados e filtros interativos",
        "gráficos dinâmicos vinculados a tabelas",
        "tabelas dinâmicas em dashboards",
    ]),
    ("Gráficos avançados", [
        "escolha do tipo de gráfico adequado",
        "gráficos combinados, dispersão e funil",
        "personalização de eixos, rótulos e séries",
        "gráficos dinâmicos e formatação profissional",
    ]),
    ("Tratamento de dados", [
        "classificação e filtros avançados",
        "remover duplicadas e texto para colunas",
        "preenchimento relâmpago e limpeza de dados",
        "consolidação de dados de várias listas",
    ]),
    ("Power Query I", [
        "introdução ao Power Query e fontes de dados",
        "importação de arquivos CSV, Excel e pastas",
        "consultas, etapas e visualização de dados",
        "tipos de dados e tratamento de erros",
    ]),
    ("Power Query II", [
        "transformações: divisão, mescla e anexação",
        "agrupamento, pivot e desmembramento de colunas",
        "consultas combinadas e carregamento para planilha",
        "atualização automática de consultas",
    ]),
    ("Dashboard I — planejamento", [
        "conceito de dashboard e definição de KPIs",
        "planejamento de layout e hierarquia informacional",
        "preparação de dados e tabelas de apoio",
        "criação de indicadores com fórmulas",
    ]),
    ("Dashboard II — construção", [
        "integração de tabelas dinâmicas e gráficos",
        "segmentação e controles interativos",
        "formatação profissional e identidade visual",
        "testes e ajustes de legibilidade do painel",
    ]),
    ("Auditoria e erros", [
        "principais erros de fórmula e suas causas",
        "auditoria e depuração de fórmulas passo a passo",
        "tratamento de erros com SEERRO e validações",
        "boas práticas de construção de planilhas",
    ]),
    ("Tabelas do Excel", [
        "criação e formatação de tabelas estruturadas",
        "referências estruturadas e fórmulas da tabela",
        "segmentação e filtros de tabela",
        "conversão de intervalos em tabelas e vice-versa",
    ]),
    ("Listas e bancos de dados", [
        "filtros avançados com critérios complexos",
        "extração de dados únicos e listas",
        "funções de banco de dados e subtotais",
        "relatórios a partir de listas filtradas",
    ]),
    ("Macros I — gravação", [
        "introdução a macros e segurança de macros",
        "gravação e execução de macro simples",
        "atribuição de macros a botões e atalhos",
        "edição de macro gravada no Editor VBA",
    ]),
    ("VBA I — fundamentos", [
        "lógica de programação, variáveis e tipos de dados",
        "condicionais e operadores em VBA",
        "procedimentos Sub e Function",
        "caixas de entrada e saída de dados",
    ]),
    ("VBA II — automação", [
        "loops For, While e Do While",
        "automação de formatação e relatórios",
        "uso de objetos, planilhas e intervalos",
        "tratamento de erros em VBA",
    ]),
    ("Automação de relatórios", [
        "automação de emissão de relatórios periódicos",
        "geração automática de gráficos e PDFs",
        "macros para consolidação de arquivos",
        "rotina de atualização e agendamento",
    ]),
    ("Integração e compartilhamento", [
        "importação e exportação de dados externos",
        "compartilhamento e coautoria no Excel online",
        "proteção de dados e controle de versão",
        "backups e boas práticas de arquivamento",
    ]),
    ("Produtividade e boas práticas", [
        "atalhos, preenchimento e técnicas de produtividade",
        "auditoria de planilhas críticas e documentação",
        "padronização de modelos e estilos",
        "estudo de casos de planilhas reais",
    ]),
    ("Projeto final I — construção", [
        "planejamento do projeto final de planilha automatizada",
        "construção da base de dados e das fórmulas",
        "criação de tabelas dinâmicas e dashboard",
        "automação com macros e testes",
    ]),
    ("Projeto final II — apresentação", [
        "revisão, otimização e apresentação do projeto em laboratório",
        "demonstração das automações e dos relatórios gerados",
    ]),
]

# ------------------------------------------------------------
# Execucao
# ------------------------------------------------------------
if __name__ == "__main__":
    print(f"Base: {BASE}")
    # Desenhista Grafico
    gerar_csv("Desenhista Gráfico", "Criação e editoração de multimídia", 30, multimidia, {8})
    gerar_csv("Desenhista Gráfico", "Estruturação de interface web", 80, estruturacao, {19, 20})
    gerar_csv("Desenhista Gráfico", "Fundamentos de Web design", 80, fundamentos_web, {19, 20})
    gerar_csv("Desenhista Gráfico", "Projeto de interface web", 50, projeto_interface, {12, 13})
    # Excel Avancado
    gerar_csv("Excel Avançado", "Excel avançado", 110, excel_avancado, {17, 23, 24, 27, 28})
    print("Concluido.")
