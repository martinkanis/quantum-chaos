"""What each part of the drawn chip says about itself on hover (Plotly hover templates over customdata).

Lines stay short, because on a narrow screen the chip scrolls sideways and a wide label would be cut off.
"""

INPUT_HOVER = "<b>Vstup %{customdata[0]}</b><br>Začátek světlovodu na hraně čipu.<br>%{customdata[1]}"
WAVEGUIDE_HOVER = (
    "<b>Světlovod %{customdata[0]}</b><br>Tenký proužek křemíku nebo nitridu<br>"
    "křemíku, drží světlo jako optické vlákno.<br>%{customdata[1]}"
)
EXTERNAL_SHIFTER_HOVER = (
    "<b>Fázový posouvač φ%{customdata[0]} = %{customdata[1]} rad</b><br>"
    "Kus světlovodu se změněným indexem lomu,<br>nejčastěji ho ohřívá malé topné tělísko.<br>"
    "Zpozdí světlo v horním vstupu MZI proti<br>dolnímu. Dělicí poměr nemění, rozhoduje ale,<br>"
    "jak se složí světlo z obou vstupů."
)
INTERNAL_SHIFTER_HOVER = (
    "<b>Fázový posouvač θ%{customdata[0]} = %{customdata[1]} rad</b><br>"
    "Sedí mezi oběma děliči MZI a určuje,<br>kam světlo odejde: θ = 0 všechno křížem<br>"
    "do sousedního světlovodu, π/2 napůl, π rovně."
)
COUPLER_HOVER = (
    "<b>%{customdata[1]}. dělič MZI %{customdata[0]}</b><br>"
    "Směrový vazební člen: dva světlovody vedou<br>těsně vedle sebe a světlo z jednoho postupně<br>"
    "přetéká do druhého. Do sousedního světlovodu<br>pošle %{customdata[2]} světla (ideál 50 %)."
)
MZI_HOVER = (
    "<b>MZI %{customdata[0]}</b>: Machův–Zehnderův interferometr<br>"
    "na světlovodech %{customdata[1]} a %{customdata[2]}. Dělič, posouvač θ<br>"
    "a druhý dělič dohromady tvoří dělič<br>s nastavitelným poměrem.<br>"
    "θ = %{customdata[3]} rad, φ = %{customdata[4]} rad: ze světlovodu %{customdata[1]}<br>"
    "přejde vedle %{customdata[5]} světla."
)
LASER_DETECTOR_HOVER = (
    "<b>Detektor %{customdata[0]}</b><br>Fotodioda na konci světlovodu změří,<br>"
    "kolik světla dopadlo: %{customdata[1]}."
)
PHOTON_DETECTOR_HOVER = (
    "<b>Detektor %{customdata[0]}</b><br>Počítá jednotlivé fotony. Simulátor<br>"
    "předpokládá detektor, který rozliší i jejich<br>počet (0, 1, 2, …); bez toho by hodnotu<br>"
    "výstřelu S! nešlo určit.<br>Průměrně sem dorazí %{customdata[1]} fotonu."
)
