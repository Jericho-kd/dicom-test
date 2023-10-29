from pydicom import dcmread
from pydicom.dataset import Dataset
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.presentation import QueryRetrievePresentationContexts, StoragePresentationContexts

from config import DICOM_PORT, DICOM_TITLE, OUTPUT_DIR, STORAGE_TITLE
from image_processing import rotate_image_90_degrees


def query_retrieve_c_find() -> str:
    study_instance_uids = []
    dataset = Dataset()

    dataset.StudyInstanceUID = ''
    dataset.Modality = 'MG'
    dataset.QueryRetrieveLevel = 'SERIES'

    ae = AE()
    ae.requested_contexts = QueryRetrievePresentationContexts

    assoc = ae.associate('', DICOM_PORT, ae_title=DICOM_TITLE)

    if assoc.is_established:
        for (status, ds) in assoc.send_c_find(dataset, "1.2.840.10008.5.1.4.1.2.1.1"):
            if status.Status == 0xFF00:
                study_instance_uids.append(ds.StudyInstanceUID)
                print('C-FIND query status: 0x{0:04X}'.format(status.Status))             
            else:
                print('Connection timed out, was aborted or received invalid response')
        assoc.release()
   
    return study_instance_uids[0]


def query_retrieve_c_move(study_uid: str) -> None:
    dataset = Dataset()

    dataset.StudyInstanceUID = study_uid
    dataset.QueryRetrieveLevel = 'STUDY'

    ae = AE()
    ae.add_requested_context("1.2.840.10008.5.1.4.1.2.1.2")

    assoc = ae.associate('localhost', DICOM_PORT, ae_title=DICOM_TITLE)

    if assoc.is_established:
        for (status, ds) in assoc.send_c_move(dataset, STORAGE_TITLE, "1.2.840.10008.5.1.4.1.2.1.2"):
            if status:
                print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')
        assoc.release()


def c_store_request() -> None:
    ae = AE()
    ae.requested_contexts = StoragePresentationContexts

    rotate_image_90_degrees(OUTPUT_DIR)

    # Read in our DICOM CT dataset
    for dcm_file in OUTPUT_DIR.glob("*.dcm"):
        ds = dcmread(dcm_file)

        assoc = ae.associate("", DICOM_PORT, ae_title=DICOM_TITLE)

        if assoc.is_established:
            status = assoc.send_c_store(ds)

            if status:
                print('C-STORE request status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')
            assoc.release()
        else:
            print('Association rejected, aborted or never connected')


# classes for future implementation AE creation as context manager
# from dataclasses import dataclass
# from pynetdicom.ae import ApplicationEntity as AE, ListCXType


# @dataclass
# class Modality:
#     addr: str
#     port: int
#     ae_title: str


# class Association:
#     def __init__(self, modality: Modality, context: ListCXType, ae_title: str):
#         self.modality = modality
#         self.context = context
#         self.ae_title = ae_title

#     def __enter__(self):
#         ae = AE(ae_title=self.ae_title)
#         ae.requested_contexts = self.context
#         self._association = ae.associate(**vars(self.modality))
#         return self._association
    
#     def __exit__(self, *args):
#         self._association.release()
#         self._association = None