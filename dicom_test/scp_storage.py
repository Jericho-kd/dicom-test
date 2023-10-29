from pathlib import Path
from pydicom.dataset import Dataset
from pynetdicom import evt
from pynetdicom.ae import ApplicationEntity as AE
from pynetdicom.events import EventHandlerType
from pynetdicom.presentation import AllStoragePresentationContexts
from typing import Literal

from config import OUTPUT_DIR, STORAGE_TITLE, STORAGE_IP


def handle_store(event, storage_dir: Path) -> Literal[0]:
    """Handle a C-STORE request event"""

    ds: Dataset = event.dataset
    ds.file_meta = event.file_meta

    file_name = storage_dir.joinpath('IM' + ds.SOPInstanceUID[-4:]).with_suffix('.dcm')
    ds.save_as(file_name, write_like_original=False)

    return 0x0000


handlers: list[EventHandlerType] = [(evt.EVT_C_STORE, handle_store, [OUTPUT_DIR])]

ae = AE(ae_title=STORAGE_TITLE)

# Support presentation contexts for all storage SOP Classes
ae.supported_contexts = AllStoragePresentationContexts[:50]
ae.add_supported_context("1.2.840.10008.5.1.4.1.2.1.2")

# Start listening for incoming association requests
ae.start_server((STORAGE_IP, 11112), evt_handlers=handlers)
