"""Texts of the optical bench of laboratory 1: the source, the losses between fibre and chip, and the detectors."""

from __future__ import annotations

from typing import Dict, Tuple

from gbs.bench import DetectorKind, LightSource
from ui.theory_content import Reading, Source, TheoryTopic

BENCH_TITLE = "Pracovní stůl"
BENCH_HINT = (
    "Ztráty a účinnosti jsou náš odhad typických hodnot; zdroje a výklad jsou v kapitole o pracovním stole pod "
    "laboratoří. Jiný kus čipu má jiné výrobní chyby, na ideálním čipu se proto neliší."
)
SOURCE_LABELS: Dict[LightSource, Tuple[str, str]] = {
    LightSource.LASER: ("Laser", "spojité světlo, na programování a kalibraci"),
    LightSource.PHOTONS: ("Jednotlivé fotony", "ohlášené z páru, cvakají po jednom"),
}
DETECTOR_LABELS: Dict[DetectorKind, Tuple[str, str]] = {
    DetectorKind.PHOTODIODE: ("Fotodioda", "měří výkon světla, jen s laserem"),
    DetectorKind.APD: ("InGaAs APD", "počítá fotony, menší účinnost"),
    DetectorKind.SNSPD: ("SNSPD", "počítá fotony, vysoká účinnost, chlazení na pár kelvinů"),
}
DEFAULT_COUPLING_LOSS_DB = 1.5
DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM = 1.0
LOSS_STEP_DB = 0.1
DEFAULT_CHIP_UNIT = 1
MAX_CHIP_UNIT = 9999
PHOTON_SHOT_OPTIONS = (100, 1_000, 10_000)
DEFAULT_PHOTON_SHOTS = 1_000
LASER_READOUT_HINT = (
    "Na výstupu čipu = |U_ij|² pro vstup zdroje (to ukazuje i čip). Změří fotodioda = navíc ztráty obou přechodů "
    "vlákno–čip, útlum světlovodů a účinnost fotodiody."
)
PHOTON_READOUT_HINT = (
    "Pravděpodobnost, že detektor při jednom fotonu cvakne: |U_ij|², ztráty, účinnost detektoru a temné impulzy. "
    "Vystřel fotony a porovnej, kolikrát detektory opravdu cvaknou."
)
COUNTS_HINT = (
    "Sloupce = cvaknutí detektorů, kosočtverce = průměr, který se dá čekat. Rozdíl je statistický šum: s víc fotony "
    "se relativně zmenšuje."
)

REDDY_2020 = Source(
    "Reddy, D. V., Nerem, R. R., Nam, S. W., Mirin, R. P., Verma, V. B.: *Superconducting nanowire single-photon "
    "detectors with 98% system detection efficiency at 1550 nm*. Optica 7, 1649 (2020), "
    "[doi:10.1364/OPTICA.400751](https://doi.org/10.1364/OPTICA.400751)"
)
HADFIELD_2009 = Source(
    "Hadfield, R. H.: *Single-photon detectors for optical quantum information applications*. Nature Photonics 3, "
    "696–705 (2009), [doi:10.1038/nphoton.2009.230](https://doi.org/10.1038/nphoton.2009.230)"
)
EISAMAN_2011 = Source(
    "Eisaman, M. D., Fan, J., Migdall, A., Polyakov, S. V.: *Invited Review Article: Single-photon sources and "
    "detectors*. Review of Scientific Instruments 82, 071101 (2011), "
    "[doi:10.1063/1.3610677](https://doi.org/10.1063/1.3610677)"
)

BENCH_TOPIC = TheoryTopic(
    anchor="cip-pracovni-stul",
    title="Pracovní stůl: zdroj, ztráty a detektory",
    in_short=(
        r"Čip sám světlo neztrácí, ale cesta k němu a od něj ano: na přechodech mezi vláknem a čipem, ve světlovodech "
        r"a v detektorech. Laser s fotodiodou proto změří jen část světla. Jednotlivý foton skončí v jediném "
        r"detektoru s pravděpodobností $|U_{ij}|^2$ a rozdělení se ukáže až z četností mnoha fotonů."
    ),
    explanation=r"""
**Zdroj.** Laser svítí spojitě, takže se na výstupech objeví podíly výkonu $|U_{ij}|^2$ naráz. Jednotlivé fotony
simulátor bere jako *ohlášené*: zdroj vyrábí páry fotonů (spontánní parametrická sestupná konverze) a detekce
jednoho z páru ohlásí, že druhý právě letí do čipu. Simulátor počítá s dokonalým ohlášením, tedy vždy s právě
jedním fotonem. Ten se na děliči nerozdělí, skončí v jediném detektoru, v detektoru $i$ s pravděpodobností
$|U_{ij}|^2$.

**Ztráty.** Světlo do čipu vstupuje z optického vlákna a zase do vlákna vystupuje. Na každém přechodu se část
ztratí a ve světlovodech se světlo cestou tlumí. Propustnost stolu je

$$
T = 10^{-(2a + bL)/10},
$$

kde $a$ je ztráta jednoho přechodu v dB, $b$ útlum světlovodů v dB/cm a $L$ délka čipu; sloupec MZI bereme asi
1 mm dlouhý. Výchozí hodnoty 1,5 dB na přechod a 1 dB/cm jsou náš řádový odhad, skutečné čipy se liší podle
materiálu a druhu vazby. Čip se 4 světlovody tak ztratí 3,4 dB a propustí asi 46 % světla. Simulátor bere ztráty
pro všechny dráhy stejné, takže tvar rozdělení nemění, jen ho zmenší. Na skutečném čipu se ztráty mezi drahami
liší a matici čipu tím mírně zkreslí.

**Detektory.** Fotodioda měří výkon. Její kvantová účinnost, tedy podíl fotonů, které dají elektron, je u nás
80 %; s výchozími ztrátami tak fotodioda změří asi 37 % světla laseru. Jednotlivé fotony zaznamená jen detektor,
který je umí počítat. InGaAs lavinová fotodioda (APD) v Geigerově režimu má u nás účinnost 20 % a temný impulz
s pravděpodobností $10^{-4}$ na jedno detekční okno, supravodivý nanodrátkový detektor (SNSPD) účinnost 90 %
a temné impulzy $10^{-6}$. Všechny tyto hodnoty jsou náš odhad typických čísel na vlnové délce 1550 nm; jak se
detektory liší a proč, srovnávají přehledy Hadfielda a Eisamana a kol. SNSPD musí být chlazený na několik kelvinů
a nejlepší dosáhly účinnosti 98 % na 1550 nm (Reddy a kol.).

**Čítače.** Ze $N$ fotonů dá detektor s pravděpodobností cvaknutí $p$ průměrně $Np$ cvaknutí s rozptylem
$Np(1-p)$, protože počet cvaknutí má binomické rozdělení. Relativní chyba odhadu $p$ je proto asi
$\sqrt{(1-p)/(Np)}$ a klesá jen s odmocninou počtu fotonů. Účinný detektor se vyplatí: se SNSPD stačí na stejnou
přesnost zhruba 4,5krát méně fotonů než s APD.
""",
    further_reading=(
        Reading(HADFIELD_2009, "přehled detektorů jednotlivých fotonů pro kvantové informace"),
        Reading(EISAMAN_2011, "přehled zdrojů i detektorů jednotlivých fotonů"),
        Reading(REDDY_2020, "SNSPD s účinností 98 % na vlnové délce 1550 nm"),
    ),
)
