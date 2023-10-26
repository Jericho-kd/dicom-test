import pydicom
from pydicom.dataset import Dataset
from pynetdicom import debug_logger
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.presentation import QueryRetrievePresentationContexts, AllStoragePresentationContexts
from pynetdicom.sop_class import uid_to_sop_class


debug_logger()


def cfind_query() -> list[Dataset]:
    images: list[Dataset] = []
    dataset = Dataset()

    # parameters for PATIENT level
    # dataset.PatientID = ''
    # dataset.PatientBirthDate = ''
    # dataset.PatientSex = ''
    # dataset.QueryRetrieveLevel = 'PATIENT'

    # parameters for STUDY level
    # dataset.StudyDescription = ''
    # dataset.StudyDate = ''
    # dataset.StudyInstanceUID = ''
    # dataset.QueryRetrieveLevel = 'STUDY'

    # parameters for SERIES level
    dataset.SeriesInstanceUID = ''
    dataset.BodyPartExamined = ''
    dataset.Modality = 'MG'
    dataset.SeriesDescription = ''
    dataset.QueryRetrieveLevel = 'SERIES'

    print(dataset)

    ae = AE()
    ae.requested_contexts = QueryRetrievePresentationContexts

    assoc = ae.associate('localhost', 4242)

    if assoc.is_established:
        for (status, ds) in assoc.send_c_find(dataset, "1.2.840.10008.5.1.4.1.2.2.1"):
            if status.Status == 0xFF00:
                print('C-FIND query status: 0x{0:04X}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()
   
    return images


def load_images():
    ae = AE()
    ae.requested_contexts = AllStoragePresentationContexts[:127]

    assoc = ae.associate('localhost', 4242)

    if assoc.is_established:
        study_instance_uid = "1.2.276.0.7230010.3.1.2.3252257021.10392.1690202165.1214"

        dataset = Dataset()
        dataset.QueryRetrieveLevel = 'STUDY'
        dataset.StudyInstanceUID = study_instance_uid

        for (status, ds) in assoc.send_c_get(dataset, "1.2.840.10008.5.1.4.1.1.1.2.1"):
            if status:
                print('C-GET query status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()


if __name__ == '__main__':
    # cfind_query()
    load_images()