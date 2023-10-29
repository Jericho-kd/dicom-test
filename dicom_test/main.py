from utils import query_retrieve_c_find, query_retrieve_c_move, c_store_request


if __name__ == '__main__':
    # Retrieve Study Instance UID from C-FIND query
    instance_uid = query_retrieve_c_find()

    # Retrieve images by Study Instance UID from C-MOVE query
    query_retrieve_c_move(instance_uid)

    # Send rotated images to PACS by C-STORE request
    c_store_request()