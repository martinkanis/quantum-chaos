"""Texts and sources of page 3: what Qpurpose claims, how it probably works and how to read the claims."""

from __future__ import annotations

from typing import Tuple

from ui.theory_content import (
    ANDERSEN_SHAN_ADVANTAGE,
    ANDERSEN_SHAN_EXPECTATIONS,
    DANISH_QUANTUM_USE_CASES,
    HAMILTON,
    OH_CLASSICAL_SIMULATION,
    SDU_QUANTUM_FINANCE,
    Source,
)

QPURPOSE_FINANCE = Source(
    "Qpurpose: [Finance](https://qpurpose.dk/finance) – popis řešení pro banky, bez uvedené metody a bez odkazu "
    "na články"
)
DANISH_QUANTUM_USE_CASES_PAGE = Source(
    "*16 Danish Quantum Use Cases*, prosinec 2024, s. 44 – samostatná stránka s případem Jyske Bank a Qpurpose, "
    "[PDF](https://cdn.brick.site/6a3cd2dd3fd7cabf7b11b3e8/original/16-Danish-Quantum-Use-Cases-December-2024-44-1.pdf)"
)
SHAN_SHAN_HOMEPAGE = Source(
    "Shan Shan: [osobní stránka se seznamem prací](https://sshanshans.github.io/) – obě práce s Andersenem vede "
    "jako preprinty"
)
AARHUS_TALK = Source(
    "Andersen, J. E.: *Gaussian Weighted Integrals, Gaussian Boson Sampling, CV and DV Topological Quantum "
    "Computing and Industrial Applications*. Přednáška, Aarhus University, 15. 9. 2025, "
    "[anotace](https://projects.au.dk/quantum/news-and-events/item/artikel/gaussian-weighted-integrals-gaussian-"
    "boson-sampling-cv-and-dv-topological-quantum-computing-and-industrial-applications-by-professor-joergen-"
    "ellegaard-andersen)"
)
ANGUITA_MONTE_CARLO_ACCELERATOR = Source(
    "Anguita, Roelink, Marzban, Briels, Filippi, Renema: *Experimental demonstration of boson sampling as "
    "a hardware accelerator for Monte Carlo integration*, [arXiv:2509.25404](https://arxiv.org/abs/2509.25404) "
    "(2025)"
)
ZHANG_GBS_MCMC = Source(
    "Zhang, Zhou, Wang, Wang, Yang, Yang, Xue, Li: *Efficient classical sampling from Gaussian boson sampling "
    "distributions on unweighted graphs*. Nature Communications 16, 9335 (2025), "
    "[arXiv:2505.02445](https://arxiv.org/abs/2505.02445), [PubMed](https://pubmed.ncbi.nlm.nih.gov/41125605/)"
)
ANAND_POLYNOMIAL_SIMULATION = Source(
    "Anand, Chen, Cryan, Freifeld, Goldberg, Guo, Zhang: *Simulating Gaussian boson sampling on graphs in "
    "polynomial time*, [arXiv:2511.16558](https://arxiv.org/abs/2511.16558) (2025)"
)
QISKIT_DOCUMENTATION = Source(
    "IBM Quantum: [dokumentace Qiskit](https://quantum.cloud.ibm.com/docs/en/guides) – instalace, obvody "
    "a primitiva Sampler"
)

AUTHOR_PAPERS: Tuple[Source, ...] = (ANDERSEN_SHAN_EXPECTATIONS, ANDERSEN_SHAN_ADVANTAGE)
RELATED_PAPERS: Tuple[Source, ...] = (
    ANGUITA_MONTE_CARLO_ACCELERATOR,
    ZHANG_GBS_MCMC,
    ANAND_POLYNOMIAL_SIMULATION,
    OH_CLASSICAL_SIMULATION,
    HAMILTON,
)
CLAIM_SOURCES: Tuple[Source, ...] = (
    QPURPOSE_FINANCE,
    SDU_QUANTUM_FINANCE,
    DANISH_QUANTUM_USE_CASES,
    DANISH_QUANTUM_USE_CASES_PAGE,
    SHAN_SHAN_HOMEPAGE,
    AARHUS_TALK,
)

LEAD = (
    "Firma Qpurpose tvrdí, že její algoritmus pro Jyske Bank má v některých případech exponenciální výhodu před "
    "Monte Carlem. Tady je rozbor, co za tím nejspíš je, laboratoř, kde si výhodu ověříš na vlastní matici, pět "
    "připravených úloh se simulací a skript pro Qiskit ke stažení."
)

IN_SHORT = (
    "Veřejně je zdokumentovaný jen matematický základ (dva preprinty Andersena a Shan). Samotnou bankovní aplikaci "
    "Qpurpose nikde publikovanou nemá a čísla, která uvádí, nejdou ověřit. Postup níže je náš odhad odvozený "
    "z jejich článků a z tvrzení, že vše zatím běží na klasických počítačích."
)

CLAIMS = r"""
- **Web Qpurpose (finance):** předpověď krátkodobých cen a směru trhu pro více než 300 akcií z živých dat
  a tříletá spolupráce s Jyske Bank. Dál uvádí „exponenciální zrychlení oproti konvenčním metodám“, odchylku
  2 bazické body a pětkrát vyšší přesnost ocenění. Metodu nejmenuje a žádný článek necituje, jen brožuru
  *16 Danish Quantum Use Cases*.
- **Brožura (případ 16, Jyske Bank):** algoritmus zatím běží simulovaný na klasickém počítači a „v určitých
  případech“ má dávat exponenciální zrychlení; jde o gaussovsky vážené integrály.
- **Stránka SDU:** jde o rámec „Gaussian Boson Sampling applied to Gaussian Weighted Integrals“ od
  J. E. Andersena a Shan Shan. Modely jsou „quantum-inspired“ a denně běží jako HPC simulace na tradingovém
  desku banky.
"""

HYPOTHESIS = r"""
1. **Model trhu.** Pohyby cen $N$ akcií se popíšou vícerozměrným normálním rozdělením se střední hodnotou
   a kovariancí odhadnutými z živých dat. To je ve financích standard.
2. **Hledaná veličina jako gaussovský integrál.** Očekávaný pohyb ceny, výplata nebo zisk či ztráta zajištění
   se zapíše jako $\mathbb{E}[f(X)]$, kde $f$ je polynom nebo mocninná řada. Podle Wickovy věty je to
   $\sum_I a_I\,\mathrm{Haf}(B_I)$ – stejně jako u momentu portfolia na 2. stránce.
3. **Odhad místo obyčejného Monte Carla.** Místo scénářů z normálního rozdělení použijí jeden ze dvou odhadů
   z článku: **GBS-I** je vážený výběr, kde se vzory losují úměrně $\mathrm{Haf}^2$, **GBS-P** odmocňuje četnosti
   vzorů – přesně ten odhad, který počítá laboratoř níže. U vhodných úloh mají mnohem menší rozptyl než Monte
   Carlo; teorie říká, že u polynomů velmi vysokého stupně exponenciálně menší.
4. **Proč to už dnes běží na klasickém HPC.** Rozdělení GBS jde pro malé úlohy spočítat přesně (jako tady
   v aplikaci) a pro speciální struktury, hlavně nezáporné matice, ho jde vzorkovat klasicky efektivně: v roce
   2025 vyšly samplery na bázi Markovových řetězců (Zhang a kol., Nature Communications) i polynomiální simulace
   GBS na grafech (Anand a kol.). „Quantum-inspired“ tedy nejspíš znamená klasický vážený výběr s rozdělením
   převzatým z GBS. Ten proti obyčejnému Monte Carlu opravdu zlepšuje přesnost – i bez kvantového hardwaru.
"""

ASSESSMENT = r"""
- **Exponenciální zrychlení** je věta o počtu vzorků: ideální GBS proti obyčejnému Monte Carlu u speciálních
  polynomů vysokého stupně. Není to naměřené zrychlení na bankovních úlohách a počet vzorků není čas.
- **Srovnává se s nejslabším soupeřem.** Chytřejší klasické metody umí rozptyl zmenšit taky. U úlohy 1
  (E[X²⁰]) dá klasický vážený výběr ze širší normální křivky (rozptyl 21 místo 1) rozptyl jednoho vzorku
  asi 2,8 – dokonce méně než GBS-P (10,3). Kvantová výhoda dává smysl jen tam, kde rozdělení GBS nejde
  klasicky napodobit: u velkých matic s mnoha módy, ne u malých úloh z této stránky.
- **Když jde rozdělení GBS vzorkovat klasicky efektivně, kvantová výhoda mizí** a zbývá chytřejší klasický
  vážený výběr. Reálná zařízení navíc ztrácejí fotony a jejich výstup umí klasické algoritmy napodobit
  (Oh a kol., 2024).
- **Odchylka 2 bazické body a pětkrát vyšší přesnost** nejsou nikde doložené: chybí metodika i srovnání. Jde
  o marketingové tvrzení.
"""

LAB_INTRO = r"""
Úloha je spočítat střední hodnotu **monomu** $\mathbb{E}[x_1^{n_1} x_2^{n_2} \cdots x_k^{n_k}]$ pro
$x \sim \mathcal{N}(0, \Sigma)$. Matici $\Sigma$ a exponenty $n_i$ zadáš v tabulce, nebo vybereš jednu z pěti
připravených úloh. Aplikace spočítá přesnou hodnotu (Wickova věta), rozptyl jednoho scénáře klasického Monte
Carla a jednoho výstřelu GBS-P, nasimuluje obě metody a připraví skript pro Qiskit.
"""

MATRIX_HINT = (
    "Řádek tabulky je jedna proměnná: její název, exponent a řádek kovarianční matice Σ (na diagonále jsou rozptyly). "
    "Stačí upravit jednu polovinu matice, zrcadlová buňka se doplní sama. Exponent 0 proměnnou z monomu vyřadí. "
    "Liché exponenty jdou jen s nezápornými prvky matice, jinak by GBS nepoznal znaménko výsledku."
)

TUNING_HINT = (
    "Do zařízení se nahraje matice B = D·Σ·D, kde diagonála D určuje, kolik fotonů v průměru dopadne do kterého "
    "detektoru. Andersen a Shan ladí jen celkový počet fotonů (= stupeň monomu). Naše rozšíření ladí každý mód "
    "zvlášť, aby průměrný počet fotonů odpovídal jeho exponentu – to je nastavení, při kterém cílový vzor padá "
    "nejčastěji."
)

SIMULATION_HINT = (
    "Simulace je klasická: GBS je ideální bezeztrátové zařízení a protože odhad GBS-P potřebuje jen počet výstřelů "
    "s cílovým vzorem, losuje se rovnou z binomického rozdělení. Monte Carlo opravdu generuje gaussovské scénáře. "
    "Obě metody se zopakují 20× pro každý počet vzorků."
)

HEAVY_TAIL_NOTE = (
    "Proč naměřená chyba Monte Carla často vyjde menší než teorie: hodnotu xⁿ vysokého stupně ovládají vzácné "
    "obří scénáře. Ve 20 opakováních se většinou neobjeví, odhady proto vycházejí spíš pod přesnou hodnotou a "
    "chyba se zdá malá – dokud jeden takový scénář nepřijde a odhad nevystřelí nahoru. Teoretická čára ukazuje "
    "průměr přes všechny možnosti, i ty vzácné."
)

QISKIT_TEXT = r"""
Skript emuluje GBS na qubitovém simulátoru Qiskit: každý fotonický mód zakóduje do několika qubitů (binární
číslo = počet fotonů), připraví stlačené vakuum, interferometr rozloží na děliče svazku (Givensovy rotace),
změří všechny qubity a z četnosti cílového vzoru spočítá odhad GBS-P. Pro kontrolu ho porovná s přesnou
hodnotou a s klasickým Monte Carlem se stejným počtem vzorků. Potřebuje Python 3.9+, `pip install "qiskit>=1.0"
numpy`; větší úlohy (20 qubitů) běží desítky sekund. Kvantovou výhodu emulace na qubitech nepřináší – ukazuje
postup a ověřuje vzorce.
"""
