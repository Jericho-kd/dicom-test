from pydicom import dcmread
from pydicom.dataset import Dataset
from pynetdicom import debug_logger, evt
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.presentation import QueryRetrievePresentationContexts, AllStoragePresentationContexts, StoragePresentationContexts
from pynetdicom.sop_class import uid_to_sop_class

from config import STORAGE_NAME


def cfind_query() -> str:
    StudyInstanceUID = ''
    dataset = Dataset()

    # parameters for PATIENT level
    dataset.PatientID = ''
    dataset.PatientBirthDate = ''
    dataset.PatientSex = ''
    # dataset.QueryRetrieveLevel = 'PATIENT'

    # parameters for STUDY level
    dataset.StudyDescription = ''
    dataset.StudyDate = ''
    dataset.StudyInstanceUID = ''
    # dataset.QueryRetrieveLevel = 'STUDY'

    # parameters for SERIES level
    dataset.SeriesInstanceUID = ''
    dataset.BodyPartExamined = ''
    dataset.Modality = 'MG'
    dataset.SeriesDescription = ''
    dataset.QueryRetrieveLevel = 'SERIES'

    # dataset.ImageDescription = ''
    dataset.SOPInstanceUID = ''
    dataset.SOPClassUID = ''
    # dataset.QueryRetrieveLevel = 'IMAGE'


    ae = AE()
    ae.requested_contexts = QueryRetrievePresentationContexts

    assoc = ae.associate('', 4242, ae_title="ORTHANC")

    if assoc.is_established:
        for (status, ds) in assoc.send_c_find(dataset, "1.2.840.10008.5.1.4.1.2.1.1"):
            if status.Status == 0xFF00:
                print('C-FIND query status: 0x{0:04X}'.format(status.Status))
                StudyInstanceUID = ds.StudyInstanceUID
                break
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()
   
    return StudyInstanceUID


def load_images() -> None:
    dataset = Dataset()

    dataset.StudyInstanceUID = cfind_query()
    dataset.QueryRetrieveLevel = 'STUDY'

    ae = AE()
    ae.add_requested_context("1.2.840.10008.5.1.4.1.2.1.2")

    assoc = ae.associate('localhost', 4242, ae_title="ORTHANC")

    if assoc.is_established:
        for (status, ds) in assoc.send_c_move(dataset, STORAGE_NAME, "1.2.840.10008.5.1.4.1.2.1.2"):
            if status:
                print('C-GET query status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()


def c_store():
    ae = AE()

    # Add a requested presentation context
    ae.requested_contexts = StoragePresentationContexts

    # Read in our DICOM CT dataset
    ds = dcmread('')

    # Associate with peer AE at IP 127.0.0.1 and port 11112
    assoc = ae.associate("", 11112, ae_title=STORAGE_NAME)
    if assoc.is_established:
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        status = assoc.send_c_store(ds)

        # Check the status of the storage request
        if status:
            # If the storage request succeeded this will be 0x0000
            print('C-STORE request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print('Association rejected, aborted or never connected')



if __name__ == '__main__':
    load_images()
    # c_store()
