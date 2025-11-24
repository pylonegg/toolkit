import os, time, csv, logging
from pylonegg.azure.client import blob_service_client
from pylonegg.config import load_config

# --- Reconcile Blobs --------------------

def reconcile_blobs(src_container, dst_container, src_prefix="", dst_prefix="", output_dir="./ClientBin/PyAzCopy/reconcile.csv"):
    logging.info(f"Starting reconciliation between '{src_prefix}' and '{dst_prefix}'")

    # --- List source and destination blobs ---
    src_blobs = {blob.name for blob in src_container.list_blobs(name_starts_with=src_prefix)}
    dst_blobs = {blob.name for blob in dst_container.list_blobs(name_starts_with=dst_prefix)}

    # --- Normalize destination names to source pattern ---
    normalized_dst = {
        blob.replace(dst_prefix, src_prefix, 1) if blob.startswith(dst_prefix) else blob
        for blob in dst_blobs
    }

    # --- Find missing blobs ---
    missing_blobs = sorted(src_blobs - normalized_dst)

    total_src = len(src_blobs)
    total_dst = len(dst_blobs)
    missing_count = len(missing_blobs)

    logging.info(f"Source blobs: {total_src:,}")
    logging.info(f"Destination blobs: {total_dst:,}")
    logging.info(f"Missing blobs: {missing_count:,}")

    return missing_blobs


# --- Reconcile Blobs --------------------

def stream_copy(blob_name, dst_blob_name, src_container, dst_container):
    """Copy a single blob from src to dst via streaming."""
    start_time = time.time()
    try:
        src_blob = src_container.get_blob_client(blob_name)
        tmp_blob_name = dst_blob_name + ".tmp"

        dst_blob_tmp = dst_container.get_blob_client(tmp_blob_name)
        dst_blob_final = dst_container.get_blob_client(dst_blob_name)

        # Skip if final blob already exists
        if dst_blob_final.exists():
            logging.info(f"SKIPPED | {blob_name} already exists in destination")
            return "skipped"

        # Stream download and upload directly between accounts
        stream = src_blob.download_blob()
        dst_blob_tmp.upload_blob(stream, overwrite=True)

        # Rename tmp blob to final blob (atomic)
        dst_blob_final.start_copy_from_url(dst_blob_tmp.url)
        dst_blob_tmp.delete_blob()

        elapsed = time.time() - start_time
        logging.info(f"SUCCESS | {blob_name} | {elapsed:.2f}s")
        return "copied"

    except Exception as e:
        logging.error(f"ERROR | {blob_name} | {e}")
        return "error"



def copy_storage():
    config = load_config()
    print(config)
    SRC_ACCOUNT_NAME = config.get('SRC_ACCOUNT_NAME')
    DST_ACCOUNT_NAME = config.get('DST_ACCOUNT_NAME')
    SRC_ACCOUNT_KEY = config.get('SRC_ACCOUNT_KEY')
    DST_ACCOUNT_KEY = config.get('DST_ACCOUNT_KEY')
    SRC_CONTAINER_NAME = config.get('SRC_CONTAINER_NAME')
    DST_CONTAINER_NAME = config.get('DST_CONTAINER_NAME')
    SRC_FOLDER_PREFIX = config.get('SRC_FOLDER_PREFIX')
    DST_FOLDER_PREFIX = config.get('DST_FOLDER_PREFIX')

    SRC_CONNECTION_STRING = ("DefaultEndpointsProtocol=https;"f"AccountName={SRC_ACCOUNT_NAME};"f"AccountKey={SRC_ACCOUNT_KEY}""EndpointSuffix=core.windows.net")
    DST_CONNECTION_STRING = ("DefaultEndpointsProtocol=https;"f"AccountName={DST_ACCOUNT_NAME};"f"AccountKey={DST_ACCOUNT_KEY}""EndpointSuffix=core.windows.net")
    start = time.time()
    src_client = blob_service_client((SRC_CONNECTION_STRING), "SOURCE")
    src_container = src_client.get_container_client(SRC_CONTAINER_NAME)

    dst_client = blob_service_client((DST_CONNECTION_STRING), "DESTINATION")
    dst_container = dst_client.get_container_client(DST_CONTAINER_NAME)

    # --- reconcile ---------------
    blob_list = reconcile_blobs(src_container, dst_container, SRC_FOLDER_PREFIX, DST_FOLDER_PREFIX)
    for blob_name in blob_list:
        if blob_name.endswith('.parquet'):
            dst_blob_name = blob_name.replace(SRC_FOLDER_PREFIX, DST_FOLDER_PREFIX, 1)
            stream_copy(blob_name, dst_blob_name, src_container, dst_container)

    logging.info(f"All done in {time.time() - start:.2f}s")