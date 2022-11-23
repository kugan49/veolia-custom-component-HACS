import operator
import xml.etree.ElementTree as ET
from copy import deepcopy as copy
from datetime import datetime

import requests
import xmltodict


class VeoliaError(Exception):
    pass


class BadCredentialsException(Exception):
    pass


class VeoliaClient:
    """Class to manage the webServices system.
    Keyword arguments :
        none
    Return self
    """

    def __init__(self, email, password, session=None):
        """Initialize the client object."""
        self._email = email
        self._pwd = password
        self.address = "https://www.service.eau.veolia.fr/icl-ws/iclWebService"
        self.headers = {"Content-Type": "application/xml; charset=UTF-8"}
        self.__tokenPassword = None
        self.success = False
        self.attributes = {}
        if session is None:
            self.session = requests.Session()
        else:
            self.session = session
        self.__enveloppe = self.__create_enveloppe()

    def login(self):
        """
        Check if login is right
        """
        try:
            self._get_tokenPassword()
        except Exception:
            raise BadCredentialsException("wrong authentication")
            pass

    def update(self):
        """Return the latest collected datas."""
        if self.__tokenPassword is None:
            self._get_tokenPassword()
        self._fetch_data()
        if not self.success:
            return
        return self.attributes

    def close_session(self):
        """Close current session."""
        self.session.close()
        self.session = None

    def _fetch_data(self):
        """Fetch latest data from Suez."""
        datas = self.__construct_body("getConsommationJournaliere", {"aboNum": self.__aboId}, anonymous=False)

        resp = self.session.post(
            self.address,
            headers=self.headers,
            data=datas,
        )
        if resp.status_code != 200:
            raise Exception(f"POST /_fetch_data/ {resp.status_code}")
        else:
            try:
                result = xmltodict.parse(f"<soap:Envelope{resp.text.split('soap:Envelope')[1]}soap:Envelope>")
                lstindex = result["soap:Envelope"]["soap:Body"]["ns2:getConsommationJournaliereResponse"]["return"]
                self.attributes["attribution"] = "Data provided by https://www.service.eau.veolia.fr/"
                self.attributes["historyConsumption"] = {}
                # sort date desc and append in list of tuple (date,liters)
                lstindex.sort(key=operator.itemgetter("dateReleve"), reverse=True)
                idx = 0
                for val in lstindex:
                    self.attributes["historyConsumption"][idx] = (val["dateReleve"], val["consommation"] * 1000)
                    idx += 1
                self.success = True
            except ValueError:
                raise VeoliaError("Issue with accessing data")
                pass

    def _get_tokenPassword(self):
        """
        Get token password for next actions who needs authentication
        """
        datas = self.__construct_body(
            "getAuthentificationFront",
            {"cptEmail": self._email, "cptPwd": self._pwd},
            anonymous=True,
        )

        resp = self.session.post(
            self.address,
            headers=self.headers,
            data=datas,
        )
        if resp.status_code != 200:
            raise Exception(f"POST /__get_tokenPassword/ {resp.status_code}")
        else:
            result = xmltodict.parse(f"<soap:Envelope{resp.text.split('soap:Envelope')[1]}soap:Envelope>")
            self.__tokenPassword = result["soap:Envelope"]["soap:Body"]["ns2:getAuthentificationFrontResponse"][
                "return"
            ]["espaceClient"]["cptPwd"]
            self.__aboId = result["soap:Envelope"]["soap:Body"]["ns2:getAuthentificationFrontResponse"]["return"][
                "listContrats"
            ]["aboId"]

    def __create_enveloppe(self):
        """
        Returns enveloppe for requests

        Returns:
            xml: enveloppe
        """
        # <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        __enveloppe = ET.Element("soap:Envelope")
        __enveloppe.set("xmlns:soap", "http://schemas.xmlsoap.org/soap/envelope/")
        __enveloppe.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        # <soap:Header>
        __header = ET.SubElement(__enveloppe, "soap:Header")
        # <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
        __security = ET.SubElement(__header, "wsse:Security")
        __security.set(
            "xmlns:wsse", "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
        )
        __security.set(
            "xmlns:wsu", "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
        )
        # <wsse:UsernameToken xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="UsernameToken-aiehdbsf52">
        __usernameToken = ET.SubElement(__security, "wsse:UsernameToken")
        __usernameToken.set(
            "xmlns:wsu", "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
        )
        __usernameToken.set("wsu:Id", "UsernameToken-aiehdbsf52")
        # <wsse:Username>anonyme</wsse:Username>
        __username = ET.SubElement(__usernameToken, "wsse:Username")
        __username.text = "anonyme"
        # <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">PYg6fMplCoo19dZVXkn2</wsse:Password>
        __password = ET.SubElement(__usernameToken, "wsse:Password")
        __password.set(
            "Type", "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText"
        )
        __password.text = "PYg6fMplCoo19dZVXkn2"
        # <wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">1dWl+HzD/sJsWzAcDHQX6Q==</wsse:Nonce>
        __nonce = ET.SubElement(__usernameToken, "wsse:Nonce")
        __nonce.set(
            "EncodingType",
            "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary",
        )
        __nonce.text = "1dWl+HzD/sJsWzAcDHQX6Q=="
        # <wsse:Created>2022-11-22T07:54:00.000Z</wsse:Created>
        __created = ET.SubElement(__usernameToken, "wsse:Created")
        __created.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # <soap:Body>
        ET.SubElement(__enveloppe, "soap:Body")
        return __enveloppe

    def __construct_body(self, action: str, elts: dict, anonymous=True):
        """
        Appends action into a copy of _enveloppe

        Args:
            action (str): Name of action
            elts (dict): elements to insert into action
            anonymous (bool, optional): anonymous authentication. Defaults to True.

        Returns:
            xml: completed enveloppe for requests
        """
        datas = copy(self.__enveloppe)
        _body = datas.find("soap:Body")
        _action = ET.SubElement(_body, f"ns2:{action}")
        _action.set("xmlns:ns2", "http://ws.icl.veolia.com/")
        for k, v in elts.items():
            t = ET.SubElement(_action, k)
            t.text = v

        if not anonymous:
            username_token = datas.find("soap:Header").find("wsse:Security").find("wsse:UsernameToken")
            username_token.find("wsse:Username").text = self._email
            username_token.find("wsse:Password").text = self.__tokenPassword

        return ET.tostring(datas, encoding="UTF-8")


# ============================================================
#    MAIN
# ============================================================
if __name__ == "__main__":
    """Main of interface
    Keyword arguments :
        none
    Return self
    """
    pass
