from pathlib import Path
from pydicom.dataset import Dataset
from pynetdicom import evt
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.events import EventHandlerType
from pynetdicom.presentation import AllStoragePresentationContexts
from typing import Literal

from config import OUTPUT_FOLDER, STORAGE_NAME, STORAGE_IP


def handle_store(event, storage_dir: str) -> Literal[0]:
    """Handle a C-STORE request event."""

    # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
    ds: Dataset = event.dataset

    # Add the File Meta Information
    ds.file_meta = event.file_meta

    # Create full path to the file
    file_name = Path(storage_dir).joinpath(ds.SOPInstanceUID)

    # Save the dataset using the SOP Instance UID as the filename
    ds.save_as(file_name, write_like_original=False)


    # Return a 'Success' status
    return 0x0000


handlers: list[EventHandlerType] = [(evt.EVT_C_STORE, handle_store, [OUTPUT_FOLDER])]

# Initialise the Application Entity
ae = AE(ae_title=STORAGE_NAME)

# Support presentation contexts for all storage SOP Classes
ae.supported_contexts = AllStoragePresentationContexts[:50]
ae.add_supported_context("1.2.840.10008.5.1.4.1.2.1.2")

# Start listening for incoming association requests
ae.start_server((STORAGE_IP, 11112), evt_handlers=handlers)
