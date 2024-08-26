
class MXML_Effects:
    def __init__(self) -> None:
        # pm = palm mute
        # fbu = full up bending + hold (2 semitones)
        # hbu = half up bending + hold (1 semitone)
        # fbud = full up bending + release
        # fbud = half up bending + release
        # tr = tremolo
        # TODO Change booleans through string which represents the tag where the element sould be inserted
        # Tuple Boolean Value at position 1 indicates if the element has to appended to a <technical> Tag
        # <hammer-on number="1" type="start">H</hammer-on> <hammer-on number="1" type="stop"/>
        # <pull-off number="1" type="stop"/> <pull-off number="1" type="start">P</pull-off>
        self.mapping = {
            "no":("", False),
            "pm":(["""<play><mute>palm</mute></play>"""], False),
            "fbu":(["""<bend shape=\"curved\"><bend-alter>2</bend-alter></bend>"""],True),
            "fbr":(["""<bend shape=\"curved\"><bend-alter>2</bend-alter></bend>""", """<bend shape="curved"><bend-alter>-2</bend-alter><release offset=\"1\"/></bend>"""],True),
            "hbu":(["""<bend shape=\"curved\"><bend-alter>1</bend-alter></bend>"""],True),
            "hbr":(["""<bend shape=\"curved\"><bend-alter>1</bend-alter></bend>""", """<bend shape="curved"><bend-alter>-1</bend-alter><release offset=\"1\"/></bend>"""],True),
            "ah":(["""<harmonic><artifical/><sounding-pitch/></harmonic>"""],True),
            "nh":(["""<harmonic><natural/></harmonic>"""],True),
            "rht":(["""<tap hand=\"right\" placement=\"above\""""],True),
            "lht":(["""<tap hand=\"left\" placement=\"above\""""],True),
            "up":(["""<up-bow/>"""],True),
            "down":(["""<down-bow/>"""],True),
            "vib":(["""<?GP <root><vibrato type=\"Slight\"/></root>?>"""],False),
            "arp":(["""<notations><arpeggiate number=\"1\"/></notations>"""],False)
            
        }

    def get_musicxml_string(self, effect:str="none") -> str:
        return self.mapping[effect]