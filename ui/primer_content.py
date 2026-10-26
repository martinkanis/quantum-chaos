"""Czech translation of the primer by Kolarovszki and Zimborás on photonic quantum computing and Gaussian Boson Sampling.

The original lecture notes were written for the workshop „Graph theoretical applications of photonic quantum
computing“ at IT4Innovations in Ostrava, 2–3 September 2025. Each chapter is a module ui/primer_*_content.py with a
PrimerChapter; ui/primer_page.py renders it as one page. Equation numbers, definitions and citation numbers follow
the original, so „(1.2)“ or „[29]“ mean the same as there.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

ORIGINAL_TITLE = "Primer on photonic quantum computing, Gaussian Boson Sampling and its applications"
AUTHORS = "Zoltán Kolarovszki, Zoltán Zimborás"
SERIES_TITLE = "Skripta: fotonické kvantové počítání a Gaussian Boson Sampling"
TRANSLATION_NOTE = (
    f"Překlad skript *{ORIGINAL_TITLE}* ({AUTHORS}), připravených pro workshop „Graph theoretical applications of "
    "photonic quantum computing“ v IT4Innovations v Ostravě 2.–3. 9. 2025. Čísla rovnic, definic, tvrzení i citací "
    "odpovídají originálu. Do češtiny přeložil Claude; zjevné překlepy originálu jsou opravené a poznámky "
    "překladatele jsou označené. Autoři v předmluvě upozorňují, že skripta vznikla rychle a mohou obsahovat chyby."
)


@dataclass(frozen=True)
class PrimerSection:
    anchor: str
    """Unique across the app: „skripta-1-2“ for section 1.2, „skripta-a-3“ for A.3, „skripta-uvod“."""
    number: str
    """„1.2“, „A.3“, or empty for an unnumbered part such as the introduction."""
    title: str
    body: str
    """Markdown with MathJax: display formulas between $$ on lines of their own, numbered by \\tag{1.2}."""


@dataclass(frozen=True)
class PrimerChapter:
    label: str
    """„Kapitola 1“, „Dodatky A a B“."""
    title: str
    intro: str
    """Opening paragraph of the chapter before its first section; may be empty."""
    sections: Tuple[PrimerSection, ...]
    original_pages: str
    """Pages of the original PDF (as printed in it) that the chapter translates."""


BIBLIOGRAPHY: Tuple[str, ...] = (
    "R. P. Feynman: *Simulating physics with computers*. International Journal of Theoretical Physics 21 (1982), "
    "467–488",
    "M. A. Nielsen, I. L. Chuang: *Quantum Computation and Quantum Information: 10th Anniversary Edition*. Cambridge "
    "University Press, 2011, [cambridge.org](https://www.cambridge.org/highereducation/books/quantum-computation-and-"
    "quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE)",
    "A. Smith, M. S. Kim, F. Pollmann, J. Knolle: *Simulating quantum many-body dynamics on a current digital quantum "
    "computer*. npj Quantum Information 5 (2019), [doi:10.1038/s41534-019-0217-0]"
    "(https://doi.org/10.1038/s41534-019-0217-0)",
    "A. Peruzzo, J. McClean, P. Shadbolt, M.-H. Yung, X.-Q. Zhou, P. J. Love, A. Aspuru-Guzik, J. L. O’Brien: "
    "*A variational eigenvalue solver on a photonic quantum processor*. Nature Communications 5 (2014), "
    "[doi:10.1038/ncomms5213](https://doi.org/10.1038/ncomms5213)",
    "J. Huh, G. G. Guerreschi, B. Peropadre, J. R. McClean, A. Aspuru-Guzik: *Boson sampling for molecular vibronic "
    "spectra*. Nature Photonics 9 (2015), 615–620, [doi:10.1038/nphoton.2015.153]"
    "(https://doi.org/10.1038/nphoton.2015.153)",
    "J. Huh, M.-H. Yung: *Vibronic Boson Sampling: Generalized Gaussian Boson Sampling for Molecular Vibronic Spectra "
    "at Finite Temperature*. Scientific Reports 7 (2017), [doi:10.1038/s41598-017-07770-z]"
    "(https://doi.org/10.1038/s41598-017-07770-z)",
    "Y. Cao, J. Romero, J. P. Olson, M. Degroote, P. D. Johnson, M. Kieferová, I. D. Kivlichan, T. Menke, "
    "B. Peropadre, N. P. D. Sawaya, S. Sim, L. Veis, A. Aspuru-Guzik: *Quantum Chemistry in the Age of Quantum "
    "Computing*. Chemical Reviews 119 (2019), 10856–10915, [doi:10.1021/acs.chemrev.8b00803]"
    "(https://doi.org/10.1021/acs.chemrev.8b00803)",
    "J. Biamonte, P. Wittek, N. Pancotti, P. Rebentrost, N. Wiebe, S. Lloyd: *Quantum machine learning*. Nature 549 "
    "(2017), 195–202, [doi:10.1038/nature23474](https://doi.org/10.1038/nature23474)",
    "M. Cerezo, G. Verdon, H.-Y. Huang, L. Cincio, P. J. Coles: *Challenges and opportunities in quantum machine "
    "learning*. Nature Computational Science 2 (2022), 567–576, [Semantic Scholar]"
    "(https://api.semanticscholar.org/CorpusID:252323115)",
    "F. Arute a kol.: *Quantum supremacy using a programmable superconducting processor*. Nature 574 (2019), "
    "505–510, [doi:10.1038/s41586-019-1666-5](https://doi.org/10.1038/s41586-019-1666-5)",
    "A. Javadi-Abhari, M. Treinish, K. Krsulich, C. J. Wood, J. Lishman, J. Gacon, S. Martiel, P. D. Nation, "
    "L. S. Bishop, A. W. Cross, B. R. Johnson, J. M. Gambetta: *Quantum computing with Qiskit*. 2024, "
    "[arXiv:2405.08810](https://arxiv.org/abs/2405.08810)",
    "M. P. da Silva a kol.: *Demonstration of logical qubits and repeated error correction with better-than-physical "
    "error rates*. 2024, [arXiv:2404.02280](https://arxiv.org/abs/2404.02280)",
    "H. Levine a kol.: *Demonstrating a Long-Coherence Dual-Rail Erasure Qubit Using Tunable Transmons*. Physical "
    "Review X 14 (2024), [doi:10.1103/physrevx.14.011051](https://doi.org/10.1103/physrevx.14.011051)",
    "A. Gold, J. Paquette, A. Stockklauser, M. J. Reagor, M. S. Alam, A. Bestwick, N. Didier, A. Nersisyan, F. Oruc, "
    "A. Razavi, B. Scharmann, E. A. Sete, B. Sur, D. Venturelli, C. J. Winkleblack, F. Wudarski, M. Harburn, "
    "C. Rigetti: *Entanglement Across Separate Silicon Dies in a Modular Superconducting Qubit Device*. 2021, "
    "[arXiv:2102.13293](https://arxiv.org/abs/2102.13293)",
    "L. S. Madsen, F. Laudenbach, M. F. Askarani, F. Rortais, T. Vincent, J. F. F. Bulmer, F. M. Miatto, L. Neuhaus, "
    "L. G. Helt, M. J. Collins, A. Lita, T. Gerrits, S. Nam, V. Vaidya, M. M. a kol.: *Quantum computational "
    "advantage with a programmable photonic processor*. Nature 606 (2022), 75–81, "
    "[doi:10.1038/s41586-022-04725-x](https://doi.org/10.1038/s41586-022-04725-x)",
    "S. Bartolucci, P. Birchall, H. Bombín, H. Cable, C. Dawson, M. Gimeno-Segovia, E. Johnston, K. Kieling, "
    "N. Nickerson, M. Pant, F. Pastawski, T. Rudolph, C. Sparrow: *Fusion-based quantum computation*. Nature "
    "Communications 14 (2023), 912, [doi:10.1038/s41467-023-36493-1](https://doi.org/10.1038/s41467-023-36493-1)",
    "L. Henriet, L. Beguin, A. Signoles, T. Lahaye, A. Browaeys, G.-O. Reymond, C. Jurczak: *Quantum computing with "
    "neutral atoms*. Quantum 4 (2020), 327, [doi:10.22331/q-2020-09-21-327](https://doi.org/10.22331/q-2020-09-21-327)",
    "F. H. B. Somhorst, R. van der Meer, M. Correa Anguita, R. Schadow, H. J. Snijders, M. de Goede, B. Kassenberg, "
    "P. Venderbosch, C. Taballione, J. P. Epping, H. H. van den Vlekkert, J. Timmerhuis, J. F. F. Bulmer, J. Lugani, "
    "I. A. Walmsley, P. W. H. Pinkse, J. Eisert, N. Walk, J. J. Renema: *Quantum simulation of thermodynamics in an "
    "integrated quantum photonic processor*. Nature Communications 14 (2023), "
    "[doi:10.1038/s41467-023-38413-9](https://doi.org/10.1038/s41467-023-38413-9)",
    "I. Y. Akhalwaya, A. Connolly, R. Guichard, S. Herbert, C. Kargi, A. Krajenbrink, M. Lubasch, C. M. Keever, "
    "J. Sorci, M. Spranger, I. Williams: *A Modular Engine for Quantum Monte Carlo Integration*. 2023, "
    "[arXiv:2308.06081](https://arxiv.org/abs/2308.06081)",
    "S. J. Evered, D. Bluvstein, M. Kalinowski, S. Ebadi, T. Manovitz, H. Zhou, S. H. Li, A. A. Geim, T. T. Wang, "
    "N. Maskara, H. Levine, G. Semeghini, M. Greiner, V. Vuletić, M. D. Lukin: *High-fidelity parallel entangling "
    "gates on a neutral-atom quantum computer*. Nature 622 (2023), 268–272, "
    "[doi:10.1038/s41586-023-06481-y](https://doi.org/10.1038/s41586-023-06481-y)",
    "S. S. Gill, O. Cetinkaya, S. Marrone, D. Claudino, D. Haunschild, L. Schlote, H. Wu, C. Ottaviani, X. Liu, "
    "S. P. Machupalli, K. Kaur, P. Arora, J. Liu, A. Farouk, H. H. Song, S. Uhlig, K. Ramamohanarao: *Quantum "
    "Computing: Vision and Challenges*. 2024, [arXiv:2403.02240](https://arxiv.org/abs/2403.02240)",
    "J. Preskill: *Quantum Computing in the NISQ era and beyond*. Quantum 2 (2018), 79, "
    "[doi:10.22331/q-2018-08-06-79](https://doi.org/10.22331/q-2018-08-06-79)",
    "R. Acharya a kol.: *Quantum error correction below the surface code threshold*. 2024, "
    "[arXiv:2408.13687](https://arxiv.org/abs/2408.13687)",
    "H.-S. Zhong, H. Wang, Y.-H. Deng, M.-C. Chen, L.-C. Peng, Y.-H. Luo, J. Qin, D. Wu, X. Ding, Y. Hu, P. Hu, "
    "X.-Y. Yang, W.-J. Zhang, H. Li, Y. Li a kol.: *Quantum computational advantage using photons*. Science 370 "
    "(2020), 1460–1463, [doi:10.1126/science.abe8770](https://doi.org/10.1126/science.abe8770)",
    "H.-S. Zhong a kol.: *Phase-Programmable Gaussian Boson Sampling Using Stimulated Squeezed Light*. Physical Review "
    "Letters 127 (2021), [doi:10.1103/physrevlett.127.180502](https://doi.org/10.1103/physrevlett.127.180502)",
    "H. Bombin, C. Dawson, R. V. Mishmash, N. Nickerson, F. Pastawski, S. Roberts: *Logical blocks for fault-tolerant "
    "topological quantum computation*. PRX Quantum 4 (2023), 020303, "
    "[doi:10.1103/PRXQuantum.4.020303](https://doi.org/10.1103/PRXQuantum.4.020303)",
    "J. E. Bourassa, R. N. Alexander, M. Vasmer, A. Patil, I. Tzitrin, T. Matsuura, D. Su, B. Q. Baragiola, S. Guha, "
    "G. Dauphinais a kol.: *Blueprint for a scalable photonic fault-tolerant quantum computer*. Quantum 5 (2021), "
    "392, [doi:10.22331/q-2021-02-04-392](https://doi.org/10.22331/q-2021-02-04-392)",
    "J. Romero, G. Milburn: *Photonic Quantum Computing*. 2024, [arXiv:2404.03367](https://arxiv.org/abs/2404.03367)",
    "S. Aaronson, A. Arkhipov: *The computational complexity of linear optics*. Proceedings of the Forty-Third Annual "
    "ACM Symposium on Theory of Computing (STOC ’11), San Jose, 2011, 333–342, "
    "[doi:10.1145/1993636.1993682](https://doi.org/10.1145/1993636.1993682)",
    "C. S. Hamilton, R. Kruse, L. Sansoni, S. Barkhofen, C. Silberhorn, I. Jex: *Gaussian Boson Sampling*. Physical "
    "Review Letters 119 (2017), 170501, [doi:10.1103/PhysRevLett.119.170501]"
    "(https://doi.org/10.1103/PhysRevLett.119.170501)",
    "J. M. Arrazola, T. R. Bromley: *Using Gaussian Boson Sampling to Find Dense Subgraphs*. Physical Review Letters "
    "121 (2018), 030503, [doi:10.1103/PhysRevLett.121.030503](https://doi.org/10.1103/PhysRevLett.121.030503)",
    "L. Banchi, M. Fingerhuth, T. Babej, C. Ing, J. M. Arrazola: *Molecular docking with Gaussian Boson Sampling*. "
    "Science Advances 6 (2020), [doi:10.1126/sciadv.aax1950](https://doi.org/10.1126/sciadv.aax1950)",
    "G. Adesso, S. Ragy, A. R. Lee: *Continuous Variable Quantum Information: Gaussian States and Beyond*. Open "
    "Systems & Information Dynamics 21 (2014), 1440001, [doi:10.1142/s1230161214400010]"
    "(https://doi.org/10.1142/s1230161214400010)",
    "J. E. Campbell: *On a Law of Combination of Operators bearing on the Theory of Continuous Transformation Groups*. "
    "Proceedings of the London Mathematical Society (1896), 381–390, [Semantic Scholar]"
    "(https://api.semanticscholar.org/CorpusID:120180477)",
    "W. R. Clements, P. C. Humphreys, B. J. Metcalf, W. S. Kolthammer, I. A. Walmsley: *Optimal design for universal "
    "multiport interferometers*. Optica 3 (2016), 1460–1465, [doi:10.1364/OPTICA.3.001460]"
    "(https://doi.org/10.1364/OPTICA.3.001460)",
    "Z.-X. Shang, H.-S. Zhong, Y.-K. Zhang, C.-C. Yu, X. Yuan, C.-Y. Lu, J.-W. Pan, M.-C. Chen: *Boson sampling "
    "enhanced quantum chemistry*. 2024, [arXiv:2403.16698](https://arxiv.org/abs/2403.16698)",
    "C. K. Hong, Z. Y. Ou, L. Mandel: *Measurement of subpicosecond time intervals between two photons by "
    "interference*. Physical Review Letters 59 (1987), 2044–2046, [doi:10.1103/PhysRevLett.59.2044]"
    "(https://doi.org/10.1103/PhysRevLett.59.2044)",
    "A. Serafini: *Gaussian States of Continuous Variable Systems*. CRC Press, Taylor & Francis Group, 2017",
    "B. C. Hall: *Lie Groups, Lie Algebras, and Representations*. Graduate Texts in Mathematics, Springer, Cham 2015, "
    "[doi:10.1007/978-3-319-13467-3](https://doi.org/10.1007/978-3-319-13467-3)",
    "Arvind, B. Dutta, N. Mukunda, R. Simon: *The real symplectic groups in quantum mechanics and optics*. Pramana 45 "
    "(1995), 471–497, [doi:10.1007/bf02848172](https://doi.org/10.1007/bf02848172)",
    "G. Cariolaro, G. Pierobon: *Bloch-Messiah reduction of Gaussian unitaries by Takagi factorization*. Physical "
    "Review A 94 (2016), 062109",
    "R. Kruse, C. S. Hamilton, L. Sansoni, S. Barkhofen, C. Silberhorn, I. Jex: *Detailed study of Gaussian boson "
    "sampling*. Physical Review A 100 (2019), 032326, [doi:10.1103/PhysRevA.100.032326]"
    "(https://doi.org/10.1103/PhysRevA.100.032326)",
    "E. R. Caianiello: *Combinatorics & Renormalization in Quantum Field Theory*. Vol. 38, Benjamin, Reading 1973, "
    "[osti.gov](https://www.osti.gov/biblio/4338754)",
    "U. Feige, D. Peleg, G. Kortsarz: *The Dense k-Subgraph Problem*. Algorithmica 29 (2001), 410–421, "
    "[doi:10.1007/s004530010050](https://doi.org/10.1007/s004530010050)",
    "A. Bhaskara, M. Charikar, E. Chlamtac, U. Feige, A. Vijayaraghavan: *Detecting High Log-Densities – an "
    "O(n^1/4) Approximation for Densest k-Subgraph*. 2010, [arXiv:1001.2891](https://arxiv.org/abs/1001.2891)",
    "M. Aaghabali, S. Akbari, S. Friedland, K. Markstrom, Z. Tajfirouz: *Upper bounds on the number of perfect "
    "matchings and directed 2-factors in graphs with given number of vertices and edges*. 2014, "
    "[arXiv:1310.5634](https://arxiv.org/abs/1310.5634)",
    "M. Houde, W. McCutcheon, N. Quesada: *Matrix decompositions in quantum optics: Takagi/Autonne, "
    "Bloch–Messiah/Euler, Iwasawa, and Williamson*. Canadian Journal of Physics 102 (2024), 497–507, "
    "[doi:10.1139/cjp-2024-0070](https://doi.org/10.1139/cjp-2024-0070)",
    "J. Spanier, K. B. Oldham: *An atlas of functions*. Taylor & Francis/Hemisphere, 1987",
    "V. Fock: *Konfigurationsraum und zweite Quantelung*. Zeitschrift für Physik 75 (1932), 622–647, "
    "[Semantic Scholar](https://api.semanticscholar.org/CorpusID:186238995)",
)
"""The bibliography of the original in its order: citation [n] is BIBLIOGRAPHY[n - 1]."""
