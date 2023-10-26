from pydicom.dataset import Dataset
from pynetdicom import debug_logger
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.presentation import QueryRetrievePresentationContexts
from pynetdicom.sop_class import uid_to_sop_class


debug_logger()


def cfind_query() -> list[Dataset]:
    images: list[Dataset] = []
    dataset = Dataset()

    dataset.SOPClassesInStudy = ''
    dataset.PatientID = 'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f'
    dataset.StudyInstanceUID = ''
    dataset.QueryRetrieveLevel = 'STUDY'
    # identifier.QueryRetrieveLevel = 'PATIENT'
    # identifier.PatientName = 'Anonymous'
    # identifier.PatientBirthDate = "19610709"
    # identifier.Modality = 'MG'
    print(dataset)

    ae = AE()
    ae.requested_contexts = QueryRetrievePresentationContexts

    assoc = ae.associate('localhost', 4242)

    if assoc.is_established:
        for (status, ds) in assoc.send_c_find(dataset, "1.2.840.10008.5.1.4.1.2.2.1"):
            if status:
                print('C-FIND query status: 0x{0:04X}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()
   
    return images


if __name__ == '__main__':
    cfind_query()