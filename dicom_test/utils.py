from dataclasses import dataclass
from pynetdicom.ae import ApplicationEntity as AE, ListCXType


@dataclass
class Modality:
    addr: str
    port: int
    ae_title: str


class Association:
    def __init__(self, modality: Modality, context: ListCXType, ae_title: str):
        self.modality = modality
        self.context = context
        self.ae_title = ae_title

    def __enter__(self):
        ae = AE(ae_title=self.ae_title)
        ae.requested_contexts = self.context
        self._association = ae.associate(**vars(self.modality))
        return self._association
    
    def __exit__(self, *args):
        self._association.release()
        self._association = None