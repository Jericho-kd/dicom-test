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


# modality = Modality('', 4242, "ORTHANC")
# with Association(modality, QueryRetrievePresentationContexts, "PYNETDICOM") as assoc:
#     for (status, ds) in assoc.send_c_find(dataset, "1.2.840.10008.5.1.4.1.2.1.1"):
#         if status.Status == 0x0000:
#             print('C-FIND query status: 0x{0:04X}'.format(status.Status))
#         else:
#             print('Connection timed out, was aborted or received invalid response')