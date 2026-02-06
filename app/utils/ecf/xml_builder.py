import xml.etree.ElementTree as ET
from datetime import datetime

class ECFBuilder:
    def __init__(self, invoice_data):
        """
        invoice_data: dictionary with all necessary info for the ECF.
        """
        self.data = invoice_data
        self.root = ET.Element("ECF", {
            "xmlns": "http://dgii.gov.do/sicfe/v1",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://dgii.gov.do/sicfe/v1 eCF.xsd"
        })

    def build_encabezado(self):
        encabezado = ET.SubElement(self.root, "Encabezado")
        
        # IdDoc
        iddoc = ET.SubElement(encabezado, "IdDoc")
        ET.SubElement(iddoc, "TipoeCF").text = self.data.get("tipo_ecf")
        ET.SubElement(iddoc, "eCF").text = self.data.get("ncf")
        ET.SubElement(iddoc, "FechaEmision").text = self.data.get("fecha_emision", datetime.now().strftime("%d-%m-%Y"))
        ET.SubElement(iddoc, "IndicadorMontoGravado").text = str(self.data.get("indicador_monto_gravado", 1))
        
        # Emisor
        emisor = ET.SubElement(encabezado, "Emisor")
        ET.SubElement(emisor, "RNCEmisor").text = self.data.get("rnc_emisor")
        ET.SubElement(emisor, "RazonSocialEmisor").text = self.data.get("razon_social_emisor")
        ET.SubElement(emisor, "NombreComercial").text = self.data.get("nombre_comercial")
        ET.SubElement(emisor, "ActividadEconomica").text = self.data.get("actividad_economica")
        ET.SubElement(emisor, "CorreoEmisor").text = self.data.get("correo_emisor")
        
        # Receptor
        receptor = ET.SubElement(encabezado, "Receptor")
        ET.SubElement(receptor, "RNCReceptor").text = self.data.get("rnc_receptor")
        ET.SubElement(receptor, "RazonSocialReceptor").text = self.data.get("razon_social_receptor")
        
        # Totales
        totales = ET.SubElement(encabezado, "Totales")
        ET.SubElement(totales, "MontoTotal").text = f"{self.data.get('monto_total'):.2f}"
        
        return encabezado

    def build_detalles(self):
        for item in self.data.get("items", []):
            detalle = ET.SubElement(self.root, "Detalles")
            ET.SubElement(detalle, "NumeroLinea").text = str(item.get("linea"))
            ET.SubElement(detalle, "NombreItem").text = item.get("nombre")
            ET.SubElement(detalle, "CantidadItem").text = f"{item.get('cantidad'):.2f}"
            ET.SubElement(detalle, "PrecioUnitarioItem").text = f"{item.get('precio'):.2f}"
            ET.SubElement(detalle, "MontoItem").text = f"{item.get('monto'):.2f}"

    def get_xml_string(self):
        self.build_encabezado()
        self.build_detalles()
        return ET.tostring(self.root, encoding="utf-8", xml_declaration=True).decode("utf-8")
