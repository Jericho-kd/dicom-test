from pydicom.dataset import Dataset
from pynetdicom import evt
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.events import EventHandlerType
from pynetdicom.presentation import AllStoragePresentationContexts


def handle_store(event):
    """Handle a C-STORE request event."""
    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds: Dataset = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    # Save the dataset using the SOP Instance UID as the filename
    # ds.save_as(ds.SOPInstanceUID, write_like_original=False)
    ds.save_as(ds.StudyInstanceUID, write_like_original=False)


    # Return a 'Success' status
    return 0x0000

handlers: list[EventHandlerType] = [(evt.EVT_C_STORE, handle_store)]

# Initialise the Application Entity
ae = AE(ae_title="SCP_STORAGE")

# Support presentation contexts for all storage SOP Classes
ae.add_requested_context("1.2.840.10008.5.1.4.1.2.1.3")
ae.supported_contexts = AllStoragePresentationContexts[:50]
# ae.add_supported_context("1.2.840.10008.5.1.4.1.2.1.2")


# Start listening for incoming association requests
ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)