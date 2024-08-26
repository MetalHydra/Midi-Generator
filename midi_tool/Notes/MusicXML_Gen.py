import music21
import numpy as np
import xml.etree.ElementTree as ET
from Fretboard.Fretboard import Fretboard
import datetime
import uuid 

class MusicXML_Generator:
    def __init__(self) -> None:
        pass 

    def music21_stream_to_musicxml(self, stream):
        tree = self.empty_musicxml_tree()
        tree.write("./MusicXML/test.xml",xml_declaration=True)
        
    def empty_musicxml_tree(self, title:str="default", composer:str="Me"):
        root_string = f"""<score_partwise version=\"2.0\">
                                <movement-title>{title}</movement-title>
                        <identification>
                            <creator type="composer">Music21</creator>
                                <encoding>
                                    <encoding-date>{str(datetime.date.today())}</encoding-date>
                                    <software>Custom</software>
                                </encoding>
                        </identification>
                        <defaults>
                            <scaling>
                                <millimeters>7</millimeters>
                                <tenths>40</tenths>
                            </scaling>
                        </defaults>
                        </score_partwise>"""
        tree = ET.ElementTree(ET.fromstring(root_string))
        elemList = []

        for elem in tree.iter():
            elemList.append(elem.tag)
        print(elemList)
        return tree



