from pydicom import dcmread
from pydicom.dataset import Dataset
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.presentation import QueryRetrievePresentationContexts, StoragePresentationContexts

from config import STORAGE_NAME, OUTPUT_DIR
from rotate import image_rotate


def cfind_query() -> str:
    StudyInstanceUID = ''
    dataset = Dataset()

    dataset.StudyInstanceUID = ''
    dataset.Modality = 'MG'
    dataset.QueryRetrieveLevel = 'SERIES'

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
                print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

        assoc.release()

    c_store_query()


def c_store_query() -> None:
    ae = AE()

    # Add a requested presentation context
    ae.requested_contexts = StoragePresentationContexts

    # Rotate images by 90 degrees 
    image_rotate(OUTPUT_DIR)

    # Read in our DICOM CT dataset
    for dcm_file in OUTPUT_DIR.glob("*.dcm"):
        ds = dcmread(dcm_file)

        # Associate with peer AE at port 11112
        assoc = ae.associate("", 4242, ae_title="ORTHANC")
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
